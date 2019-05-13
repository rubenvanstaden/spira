import gdspy
import pyclipper
import hashlib
import numpy as np
import spira.all as spira

from spira.core import param
from spira.yevon import utils
from copy import copy, deepcopy
from spira.yevon.visualization import color
from spira.yevon.gdsii.base import __Elemental__
from spira.yevon import utils
from spira.yevon.properties.polygon import PolygonProperties
from spira.yevon.layer import LayerField
from spira.core.param.variables import *
from spira.yevon.geometry.coord import CoordField, Coord
from spira.yevon.visualization.color import ColorField
from spira.core.descriptor import DataFieldDescriptor, FunctionField, DataField
from spira.yevon.geometry.ports.base import __Port__
from spira.core.transforms.stretching import *


__all__ = ['Polygon']


class __Polygon__(gdspy.PolygonSet, __Elemental__):

    __committed__ = {}

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __copy__(self):
        return self.modified_copy(
            shape=deepcopy(self.shape),
            gds_layer=deepcopy(self.gds_layer)
        )

    def __deepcopy__(self, memo):
        ply = self.modified_copy(
            shape=deepcopy(self.shape),
            gds_layer=deepcopy(self.gds_layer),
        )
        return ply

    def __add__(self, other):
        polygons = []
        assert isinstance(other, Polygon)
        if self.gds_layer == other.gds_layer:
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
        points = utils.boolean(
            subj=self.shape.points,
            clip=other.shape.points,
            method='not'
        )
        return points

    def __and__(self, other):
        pp = utils.boolean(
            subj=other.shape.points,
            clip=self.shape.points,
            method='and'
        )
        if len(pp) > 0:
            return Polygon(shape=np.array(pp), gds_layer=self.gds_layer)
        else:
            return None

    def __or__(self, other):
        pp = utils.boolean(
            subj=other.shape.points,
            clip=self.shape.points,
            method='or'
        )
        if len(pp) > 0:
            return Polygon(shape=pp, gds_layer=self.gds_layer)
        else:
            return None

    def union(self, other):
        return self.__or__(self, other)

    def intersection(self, other):
        return self.__and__(self, other)

    def difference(self, other):
        return self.__sub__(self, other)

    def is_equal_layers(self, other):
        if self.gds_layer.number == other.gds_layer.number:
            return True
        return False


class PolygonAbstract(__Polygon__):

    name = StringField()
    gds_layer = LayerField()
    direction = IntegerField(default=0)

    @property
    def count(self):
        # FIXME: For multiple polygons
        return np.size(self.shape.points[0], 0)

    @property
    def layer(self):
        return self.gds_layer.layer

    @property
    def datatype(self):
        return self.gds_layer.datatype

    def encloses(self, point):
        for points in self.points:
            if pyclipper.PointInPolygon(point, points) == 0:
                return False
        return True

    def flat_copy(self, level=-1):
        E = self.modified_copy(
            shape=deepcopy(self.shape),
            transformation=self.transformation
        )
        E.transform_copy(self.transformation)
        return E

    # def fillet(self, radius, angle_resolution=128, precision=0.001*1e6):
    #     super().fillet(radius=radius, points_per_2pi=angle_resolution, precision=precision)
    #     self.shape.points = self.polygons
    #     return self

    # def stretch(self, sx, sy=None, center=(0,0)):
    #     super().scale(scalex=sx, scaley=sy, center=center)
    #     self.shape.points = self.polygons
    #     return self

    def stretch(self, factor=(1,1), center=(0,0)):
        self = scale_elemental(self, scaling=factor, scale_center=center)
        return self

    def transform_copy(self, transformation):
        if transformation is not None:
            new_shape = deepcopy(self.shape)
            new_shape = new_shape.transform(transformation)
            poly = self.__class__(
                name=self.name,
                # shape.points=transformation.apply_to_array(self.shape.points)
                shape=new_shape
            )
        else:
            poly = self.__class__(
                name=self.name,
                shape=deepcopy(self.shape),
            )
        return poly

    def transform(self, transformation):
        if transformation is not None:
            self.shape.points = transformation.apply_to_array(self.shape.points)
            # self.shape.points = np.array([self.shape.points])
        # self.alias = self.__repr__() + transformation.id_string()
        # print(self.alias)
        return self

    def merge(self):
        sc = 2**30
        polygons = pyclipper.scale_to_clipper(self.points, sc)
        points = []
        for poly in polygons:
            if pyclipper.Orientation(poly) is False:
                reverse_poly = pyclipper.ReversePath(poly)
                solution = pyclipper.SimplifyPolygon(reverse_poly)
            else:
                solution = pyclipper.SimplifyPolygon(poly)
            for sol in solution:
                points.append(sol)
        value = boolean(subj=points, method='or')
        PTS = []
        mc = pyclipper.scale_from_clipper(value, sc)
        for pts in pyclipper.SimplifyPolygons(mc):
            PTS.append(np.array(pts))
        self.shape.points = np.array(pyclipper.CleanPolygons(PTS))
        self.polygons = self.shape.points
        return self

    def fast_boolean(self, other, operation):
        mm = gdspy.fast_boolean(
            self.shape.points,
            other.shape.points,
            operation=operation
        )
        return Polygon(shape=mm.points, gds_layer=self.gds_layer)


class Polygon(PolygonAbstract):
    """ Elemental that connects shapes to the GDSII file format.
    Polygon are objects that represents the shapes in a layout.

    Examples
    --------
    >>> layer = spira.Layer(number=99)
    >>> rect_shape = spira.RectangleShape(p1=[0,0], p2=[1,1])
    >>> ply = spira.Polygon(shape=rect_shape, gds_layer=layer)
    """

    color = ColorField(default=color.COLOR_BLUE_VIOLET)

    _ID = 0

    def get_alias(self):
        if not hasattr(self, '__alias__'):
            self.__alias__ = self.gds_layer.name
        return self.__alias__

    def set_alias(self, value):
        self.__alias__ = value

    alias = FunctionField(get_alias, set_alias, doc='Functions to generate an alias for cell name.')

    def __init__(self, shape, **kwargs):
        from spira.yevon.geometry.shapes.shape import __Shape__
        from spira.yevon.geometry.shapes.shape import Shape

        if issubclass(type(shape), __Shape__):
            self.shape = shape
        elif isinstance(shape, (list, set, np.ndarray)):
            self.shape = Shape(points=shape)
        else:
            raise ValueError('Shape type not supported!')

        __Elemental__.__init__(self, **kwargs)
        gdspy.PolygonSet.__init__(self,
            polygons=self.shape.points,
            layer=self.gds_layer.number,
            datatype=self.gds_layer.datatype,
            verbose=False
        )

        Polygon._ID += 1

    # def __repr__(self):
    #     if self is None:
    #         return 'Polygon is None!'
    #     return ("[SPiRA: Polygon] ({} area " +
    #             "{} vertices, layer {}, datatype {})").format(
    #             self.ply_area, sum([len(p) for p in self.shape.points]),
    #             self.gds_layer.number, self.gds_layer.datatype)

    def __repr__(self):
        if self is None:
            return 'Polygon is None!'
        polygon_hashes = np.sort([hashlib.sha1(p).digest() for p in self.shape.points])
        return ("[SPiRA: Polygon {}] ({} center, {} area " +
                "{} vertices, layer {}, datatype {}, hash {})").format(Polygon._ID,
                self.shape.center_of_mass, self.ply_area, sum([len(p) for p in self.shape.points]),
                self.gds_layer.number, self.gds_layer.datatype, polygon_hashes)

    def __str__(self):
        return self.__repr__()

    # def expand_transform(self):
    #     self.transform(self.transformation)
    #     # self.transformation = None
    #     return self

    def __translate__(self, dx, dy):
        self.polygons = self.shape.points
        tt = super().translate(dx=dx, dy=dy)
        self.shape.points = self.polygons
        return self

    def move_new(self, position):
        p = np.array([position[0], position[1]])
        self.shape.points += p
        return self

    def move(self, midpoint=(0,0), destination=None, axis=None):

        if destination is None:
            destination = midpoint
            midpoint = [0,0]

        if isinstance(midpoint, Coord):
            o = midpoint
        elif np.array(midpoint).size == 2:
            o = midpoint
        elif issubclass(type(midpoint), __Port__):
            o = midpoint.midpoint
        else:
            raise ValueError("[PHIDL] [DeviceReference.move()] ``midpoint`` " +
                                "not array-like, a port, or port name")

        if issubclass(type(destination), __Port__):
            d = destination.midpoint
        if isinstance(destination, Coord):
            d = destination
        elif np.array(destination).size == 2:
            d = destination
        else:
            raise ValueError("[PHIDL] [DeviceReference.move()] ``destination`` " +
                                "not array-like, a port, or port name")

        dxdy = np.array([d[0], d[1]]) - np.array([o[0], o[1]])

        self.polygons = self.shape.points
        super().translate(dx=dxdy[0], dy=dxdy[1])
        self.shape.points = self.polygons

        return self

    @property
    def ply_bbox(self):
        # self.polygons = np.array(self.shape.points)
        bb = self.get_bounding_box()
        return bb
        # return self.get_bounding_box()

    @property
    def ply_center(self):

        self.polygons = self.shape.points
        ply = deepcopy(self.polygons)
        bb = np.array(((min(pts[:, 0].min() for pts in ply),
                        min(pts[:, 1].min() for pts in ply)),
                       (max(pts[:, 0].max() for pts in ply),
                        max(pts[:, 1].max() for pts in ply))))
        pp = np.sum(bb, 0)/2
        return pp

        # print(self.shape.points)
        # return self.shape.center_of_mass
        # pts = self.ply_bbox
        # c = np.mean(pts, 0)
        # return [c[0], c[1]]
        # return np.sum(self.ply_bbox, 0)/2

    def commit_to_gdspy(self, cell=None, transformation=None):
        # if self.__repr__() not in list(PolygonAbstract.__committed__.keys()):
        if self.node_id not in list(Polygon.__committed__.keys()):

            # if transformation is not None:
            #     # self.transform(transformation)
            #     Dp = deepcopy(self)
            #     new_poly = Dp.transform(transformation)
            # else:
            #     new_poly = deepcopy(self)

            new_poly = deepcopy(self)

            P = gdspy.PolygonSet(
                polygons=deepcopy(new_poly.shape.points),
                layer=new_poly.gds_layer.number,
                datatype=new_poly.gds_layer.datatype,
                verbose=False
            )
            # PolygonAbstract.__committed__.update({self.__repr__():P})
            Polygon.__committed__.update({self.node_id:P})
        else:
            # P = PolygonAbstract.__committed__[self.__repr__()]
            P = Polygon.__committed__[self.node_id]
        if cell is not None:
            cell.add(P)
        return P


Polygon.mixin(PolygonProperties)



