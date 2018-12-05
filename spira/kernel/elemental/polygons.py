import os
import gdspy
import meshio
import pygmsh
import inspect
import pyclipper
import collections

import numpy as np
from numpy.linalg import norm

from spira.kernel.utils import *

from spira.settings import SCALE
from spira.settings import DEVICES

from shapely.geometry import Polygon as ShapelyPolygon

from spira.kernel.parameters.initializer import MetaBase
from spira.kernel.parameters.initializer import BaseElement
from spira.kernel import parameters as param
from copy import copy, deepcopy
from spira.kernel.utils import scale_polygon_up as spu


def _reflect_points(points, p1=(0,0), p2=(1,0)):
    """ Reflects points across the line formed by p1 and p2.  ``points`` may be
    input as either single points [1,2] or array-like[N][2], and will return in kind
    """
    # From http://math.stackexchange.com/questions/11515/point-reflection-across-a-line
    points = np.array(points)
    p1 = np.array(p1)
    p2 = np.array(p2)
    if np.asarray(points).ndim == 1:
        return 2*(p1 + (p2-p1)*np.dot((p2-p1),(points-p1))/norm(p2-p1)**2) - points
    if np.asarray(points).ndim == 2:
        return np.array([2*(p1 + (p2-p1)*np.dot((p2-p1),(p-p1))/norm(p2-p1)**2) - p for p in points])


class SimplyMixin(object):

    def dissect_polygons(self):
        # TODO: DO a check for layer type.
        # Ony certain layers should save negative polygons.
        # Such as the ground layer for moats.
        elems = spira.ElementList()
        for pp in self.polygons:
            layer = deepcopy(self.gdslayer)
            if pyclipper.Orientation(pp) is False:
                layer.datatype = 68
            elems += Polygons(polygons=[pp], gdslayer=layer)
        return elems

    def fast_boolean(self, other, operation):
        mm = gdspy.fast_boolean(self.polygons,
                                other.polygons,
                                operation=operation)
        return spira.Polygons(polygons=mm.polygons,
                              gdslayer=self.gdslayer)

    @property
    def merge(self):
        pcell = False
        poly_list = []
        polygons = self.polygons
        self.polygons = []
        for poly in polygons:
            if pyclipper.Orientation(poly) is False:
                reverse_poly = pyclipper.ReversePath(poly)
                solution = pyclipper.SimplifyPolygon(reverse_poly)
            else:
                solution = pyclipper.SimplifyPolygon(poly)
            for sol in solution:
                self.polygons.append(sol)
        self.polygons = bool_operation(subj=self.polygons, method='union')
        return self

    @property
    def simplify(self):
        value = 1
        polygons = self.polygons
        self.polygons = []
        for points in polygons:
            factor = (len(points)/100) * 1e5 * value
            sp = ShapelyPolygon(points).simplify(factor)
            pp = [[p[0], p[1]] for p in sp.exterior.coords]

            # if len(points) > 10:
            #     factor = (len(points)/100) * 1e5 * value
            #     sp = ShapelyPolygon(points).simplify(factor)
            #     pp = [[int(p[0]), int(p[1])] for p in sp.exterior.coords]
            # else:
            #     pp = points

            self.polygons.append(pp)

        return self


class __Polygon__(gdspy.PolygonSet, SimplyMixin, BaseElement):

    def __init__(self, polygons, **kwargs):

        self.unit = None

        self.polygons = np.array([])

        if len(polygons):
            scaled = False
            for point in polygons[0]:
                if (point[0] != 0) and (point[1] != 0):
                    p1 = abs(point[0]/SCALE_UP)
                    p2 = abs(point[1]/SCALE_UP)
                    if (p1 < 1e-3) and (p2 < 1e-3):
                        scaled = True

            if scaled: 
                self.polygons = np.array(spu(polygons))
            else:
                self.polygons = np.array(polygons)

        BaseElement.__init__(self, **kwargs)

        gdspy.PolygonSet.__init__(self, self.polygons,
                                  layer=self.gdslayer.number,
                                  datatype=self.gdslayer.datatype,
                                  verbose=False)

    def __repr__(self):
        if self is None:
            return 'Polygon is None!'
        # return ("[SPiRA: Polygon] ({} vertices, layer {}, datatype {})").format(
        #         sum([len(p) for p in self.polygons]),
        #         self.gdslayer.number, self.gdslayer.datatype)
        return ("[SPiRA: Polygon] ({} center, " +
                "{} vertices, layer {}, datatype {})").format(
                self.center, sum([len(p) for p in self.polygons]),
                self.gdslayer.number, self.gdslayer.datatype)

    def __str__(self):
        return self.__repr__()

    def __key(self):
        a = self.area()
        c = tuple(self.center)
        return (self.gdslayer.number, self.gdslayer.datatype, a, c)

    def __eq__(self, other):
        dx = abs(self.center[0] - other.center[0])
        dy = abs(self.center[1] - other.center[1])
        if (dx < 1e-12) and (dy < 1e-12) and (self.gdslayer.number == other.gdslayer.number):
            return True
        return False

    def key_equals(self, other):
        return self.__key() == other.__key()

    def __hash__(self):
        return hash(self.__key())

    def __deepcopy__(self, memo):
        c_poly = self.modified_copy(polygons=self.polygons,
                                    gdslayer=deepcopy(self.gdslayer),
                                    # gdspy_commit=False)
                                    gdspy_commit=deepcopy(self.gdspy_commit))
        return c_poly

    def __add__(self, other):
        polygons = []
        assert isinstance(other, Polygons)
        if self.gdslayer == other.gdslayer:
            for points in self.polygons:
                polygons.append(np.array(points))
            for points in other.polygons:
                polygons.append(np.array(points))
            self.polygons = polygons
        else:
            raise ValueError("To add masks the polygon layers \
                              must be the same.")
        return self

    def __sub__(self, other):
        pp = bool_operation(subj=self.polygons,
                            clip=other.polygons,
                            method='difference')
        return Polygons(polygons=pp,
                        gdslayer=self.gdslayer)

    def __and__(self, other):
        pp = bool_operation(subj=other.polygons,
                            clip=self.polygons,
                            method='union')
        return Polygons(polygons=pp,
                        gdslayer=self.gdslayer)

    def __or__(self, other):
        # print(self.polygons)
        # print(other.polygons)
        pp = bool_operation(subj=other.polygons,
                            clip=self.polygons,
                            method='intersection')

        if len(pp) > 0:
            return Polygons(polygons=pp,
                            gdslayer=self.gdslayer)
        else:
            return None


class PolygonAbstract(__Polygon__):
    """

    """

    id0 = param.StringField()
    gdslayer = param.LayerField()
    text = param.StringField(default='ply')
    color = param.ColorField(default='#F0B27A')
    clockwise = param.BoolField(default=True)
    # points = param.PointListField()

    gdspy_commit = param.BoolField()

    __committed__ = {}

    def __init__(self, polygons=[], **kwargs):
        super().__init__(polygons, **kwargs)

    def dependencies(self):
        return None

    def commit_to_gdspy(self, cell):
        from spira.kernel.utils import scale_polygon_down as spd
        if self.__repr__() not in list(PolygonAbstract.__committed__.keys()):
            ply = deepcopy(self.polygons)
            P = gdspy.PolygonSet(spd(ply),
                                self.gdslayer.number,
                                self.gdslayer.datatype)
            cell.add(P)
            PolygonAbstract.__committed__.update({self.__repr__():P})
        else:
            cell.add(PolygonAbstract.__committed__[self.__repr__()])

    def flat_copy(self, level=-1, commit_to_gdspy=False):
        elems = []
        for points in self.polygons:
            c_poly = self.modified_copy(polygons=[points], 
                                        gdspy_commit=self.gdspy_commit)
            elems.append(c_poly)
            if commit_to_gdspy:
                self.gdspy_commit = True
        return elems

    @property
    def ply_area(self):
        ply = gdspy.PolygonSet(self.polygons)
        return ply.area()

    @property
    def bbox(self):
        self.polygons = np.array(self.polygons)
        bb = self.get_bounding_box()
        assert len(bb) == 2
        return bb

    @property
    def xmax(self):
        return self.bbox[1][0]

    @property
    def ymax(self):
        return self.bbox[1][1]

    @property
    def xmin(self):
        return self.bbox[0][0]

    @property
    def ymin(self):
        return self.bbox[0][1]

    @property
    def center(self):
        # return np.sum(self.bbox, 0)/2
        center = np.sum(self.bbox, 0)/2
        center[0] = int(round(center[0]))
        center[1] = int(round(center[1]))
        # print(center)
        return center

    @property
    def id(self):
        return self.__str__()

    def transform(self, transform):
        if transform['x_reflection']:
            self.reflect(p1=[0,0], p2=[1,0])
            self.rotate(angle=transform['rotation'])
            self.translate(dx=transform['origin'][0], dy=transform['origin'][1])
        else:
            self.rotate(angle=transform['rotation'])
            self.translate(dx=transform['origin'][0], dy=transform['origin'][1])
        return self

    def reflect(self, p1=(0,1), p2=(0,0)):
        for n, points in enumerate(self.polygons):
            self.polygons[n] = _reflect_points(points, p1, p2)
        return self

    def rotate(self, angle=45, center=(0,0)):
        super().rotate(angle=angle*np.pi/180, center=center)
        return self

    def translate(self, dx, dy):
        super().translate(dx=dx, dy=dy)
        return self

    def stretch(self, stretch_class):
        p = stretch_class.apply_to_polygon(self.polygons[0])
        self.polygons = [np.array(p)]
        return self

    @property
    def nodes(self):
        """ Created nodes of each point in the polygon array.
        Converting a point to a node allows us to bind
        other objects to that specific node or point. """
        pass

    @property
    def edges(self):
        """ A list of tuples containing two nodes. """
        pass

    def move_edge(self):
        pass

    def move(self, origin=(0,0), destination=None, axis=None):
        from spira.kernel.elemental.port import PortAbstract
        """ Moves elements of the Device from the origin point to the destination. Both
         origin and destination can be 1x2 array-like, Port, or a key
         corresponding to one of the Ports in this device """

        # If only one set of coordinates is defined, make sure it's used to move things
        if destination is None:
            destination = origin
            origin = [0,0]

        if issubclass(type(origin), PortAbstract):
            o = origin.midpoint
        elif np.array(origin).size == 2:
            o = origin
        elif origin in self.ports:
            o = self.ports[origin].midpoint
        else:
            raise ValueError("[PHIDL] [DeviceReference.move()] ``origin`` " +
                             "not array-like, a port, or port name")

        if issubclass(type(destination), PortAbstract):
            d = destination.midpoint
        elif np.array(destination).size == 2:
            d = destination
        elif destination in self.ports:
            d = self.ports[destination].midpoint
        else:
            raise ValueError("[PHIDL] [DeviceReference.move()] ``destination`` " +
                             "not array-like, a port, or port name")

        if axis == 'x':
            d = (d[0], o[1])
        if axis == 'y':
            d = (o[0], d[1])

        dx, dy = np.array(d) - o

        super().translate(dx, dy)

        return self


class UnionPolygons(PolygonAbstract, SimplyMixin):

    def __init__(self, polygons, **kwargs):
        super().__init__(polygons, **kwargs)

        self.simplify
        self.merge


class Polygons(PolygonAbstract):
    pass


from spira.kernel.parameters.descriptor import DataFieldDescriptor
def PolygonField(polygons=[]):
    return DataFieldDescriptor(default=Polygons(polygons))
    # return DataFieldDescriptor(default=Polygons(spu(polygons)))
