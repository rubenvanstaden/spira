import gdspy
import numpy as np

from spira import param
from copy import copy, deepcopy

from spira.gdsii.utils import *
from spira.core.initializer import ElementalInitializer
from spira.core.mixin.transform import TranformationMixin
from spira.core.mixin.property import PolygonMixin


class __Polygon__(gdspy.PolygonSet, ElementalInitializer):

    __mixins__ = [TranformationMixin, PolygonMixin]

    __committed__ = {}

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __deepcopy__(self, memo):
        ply = self.modified_copy(
            shape=deepcopy(self.shape),
            gdslayer=deepcopy(self.gdslayer),
            gdspy_commit=deepcopy(self.gdspy_commit))
        return ply

    def __add__(self, other):
        polygons = []
        assert isinstance(other, Polygons)
        if self.gdslayer == other.gdslayer:
            for points in self.shape.points:
                polygons.append(np.array(points))
            for points in other.polygons:
                polygons.append(np.array(points))
            self.shape.points = polygons
        else:
            raise ValueError("To add masks the polygon layers \
                              must be the same.")
        return self

    def __sub__(self, other):
        pp = bool_operation(subj=self.shape.points,
                            clip=other.shape.points,
                            method='difference')
        if len(pp) > 0:
            return Polygons(shape=pp, gdslayer=self.gdslayer)
        else:
            return None

    def __and__(self, other):
        pp = bool_operation(subj=other.shape.points,
                            clip=self.shape.points,
                            method='intersection')
        if len(pp) > 0:
            return Polygons(shape=pp, gdslayer=self.gdslayer)
        else:
            return None

    def __or__(self, other):
        pp = bool_operation(subj=other.shape.points,
                            clip=self.shape.points,
                            method='union')

        if len(pp) > 0:
            return Polygons(shape=pp, gdslayer=self.gdslayer)
        else:
            return None


class PolygonAbstract(__Polygon__):

    gdslayer = param.LayerField()
    gdspy_commit = param.BoolField()
    clockwise = param.BoolField(default=True)

    nodes = param.DataField(fdef_name='create_nodes')
    edges = param.DataField(fdef_name='create_edges')

    def __init__(self, shape, **kwargs):
        from spira.lgm.shapes.shape import __Shape__
        from spira.lgm.shapes.shape import Shape

        if issubclass(type(shape), __Shape__):
            self.shape = shape
        elif isinstance(shape, (list, set, np.ndarray)):
            self.shape = Shape(points=shape)
        else:
            raise ValueError('Shape type not supported!')

        ElementalInitializer.__init__(self, **kwargs)
        gdspy.PolygonSet.__init__(self,
            self.shape.points,
            layer=self.gdslayer.number,
            datatype=self.gdslayer.datatype,
            verbose=False)

    def create_nodes(self):
        """ Created nodes of each point in the polygon array.
        Converting a point to a node allows us to bind
        other objects to that specific node or point. """
        pass

    def create_edges(self):
        """ A list of tuples containing two nodes. """
        pass

    def move_edge(self):
        pass

    def commit_to_gdspy(self, cell):
        if self.__repr__() not in list(PolygonAbstract.__committed__.keys()):
            ply = deepcopy(self.shape.points)
            P = gdspy.PolygonSet(ply, self.gdslayer.number, self.gdslayer.datatype)
            cell.add(P)
            PolygonAbstract.__committed__.update({self.__repr__():P})
        else:
            cell.add(PolygonAbstract.__committed__[self.__repr__()])

    def flat_copy(self, level=-1, commit_to_gdspy=False):
        elems = []
        for points in self.shape.points:
            c_poly = self.modified_copy(shape=deepcopy([points]),
                                        gdspy_commit=self.gdspy_commit)
            elems.append(c_poly)
            if commit_to_gdspy:
                self.gdspy_commit = True
        return elems

    def merge(self, other):
        if isinstance(other, (list, set)):
            pass
        elif isinstance(other, Polygons):
            pass
        else:
            raise ValueError('Type is not supported for Polygon merging.')

    def transform(self, transform):
        if transform['reflection']:
            self.reflect(p1=[0,0], p2=[1,0])
        if transform['rotation']:
            self.rotate(angle=transform['rotation'])
        if transform['midpoint']:
            self.translate(dx=transform['midpoint'][0], dy=transform['midpoint'][1])
        self.shape.points = self.polygons
        return self

    def reflect(self, p1=(0,1), p2=(0,0)):
        for n, points in enumerate(self.shape.points):
            self.shape.points[n] = self.__reflect__(points, p1, p2)
        self.shape.points = self.polygons
        return self

    def rotate(self, angle=45, center=(0,0)):
        super().rotate(angle=angle*np.pi/180, center=center)
        self.shape.points = self.polygons
        return self

    def translate(self, dx, dy):
        super().translate(dx=dx, dy=dy)
        self.shape.points = self.polygons
        return self

    def stretch(self, stretch_class):
        p = stretch_class.apply_to_polygon(self.points[0])
        self.shape.points = [np.array(p)]
        return self

    def move(self, midpoint=(0,0), destination=None, axis=None):
        from spira.gdsii.elemental.port import __Port__
        """ Moves elements of the Device from the midpoint point to the destination. Both
         midpoint and destination can be 1x2 array-like, Port, or a key
         corresponding to one of the Ports in this device """

        if destination is None:
            destination = midpoint
            midpoint = [0,0]

        if issubclass(type(midpoint), __Port__):
            o = midpoint.midpoint
        elif np.array(midpoint).size == 2:
            o = midpoint
        elif midpoint in self.ports:
            o = self.ports[midpoint].midpoint
        else:
            raise ValueError("[PHIDL] [DeviceReference.move()] ``midpoint`` " +
                             "not array-like, a port, or port name")

        if issubclass(type(destination), __Port__):
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

        self.translate(dx, dy)

        return self

    def fast_boolean(self, other, operation):
        mm = gdspy.fast_boolean(
            self.shape.points,
            other.shape.points,
            operation=operation
        )
        return Polygons(shape=mm.points, gdslayer=self.gdslayer)


class Polygons(PolygonAbstract):
    """ Elemental that connects shapes to the GDSII file format.
    Polygons are objects that represents the shapes in a layout.

    Examples
    --------
    >>> layer = spira.Layer(number=99)
    >>> rect_shape = spira.RectangleShape(p1=[0,0], p2=[1,1])
    >>> ply = spira.Polygons(shape=rect_shape, gdslayer=layer)
    """

    def __init__(self, shape, **kwargs):
        super().__init__(shape, **kwargs)

    def __repr__(self):
        if self is None:
            return 'Polygon is None!'
        # return ("[SPiRA: Polygon] (" +
        #         "{} vertices, layer {}, datatype {})").format(
        #         sum([len(p) for p in self.shape.points]),
        #         self.gdslayer.number, self.gdslayer.datatype)
        return ("[SPiRA: Polygon] ({} center, " +
                "{} vertices, layer {}, datatype {})").format(
                self.center, sum([len(p) for p in self.shape.points]),
                self.gdslayer.number, self.gdslayer.datatype)
















