import gdspy
import pyclipper
import numpy as np

from spira.core import param
from spira.yevon import utils
from copy import copy, deepcopy
from spira.yevon.visualization import color
from spira.yevon.gdsii.base import __Elemental__
from spira.yevon import utils
from spira.yevon.properties.polygon import PolygonProperties
from spira.yevon.layer import LayerField
from spira.core.param.variables import *
from spira.yevon.visualization.color import ColorField
from spira.core.descriptor import DataFieldDescriptor, FunctionField, DataField


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
        points = boolean(
            subj=self.shape.points,
            clip=other.shape.points,
            method='not'
        )
        return points

    def __and__(self, other):
        pp = boolean(
            subj=other.shape.points,
            clip=self.shape.points,
            method='and'
        )
        if len(pp) > 0:
            return Polygon(shape=np.array(pp), gds_layer=self.gds_layer)
        else:
            return None

    def __or__(self, other):
        pp = boolean(
            subj=other.shape.points,
            clip=self.shape.points,
            method='or'
        )
        if len(pp) > 0:
            return Polygon(shape=pp, gds_layer=self.gds_layer)
        else:
            return None

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

    def commit_to_gdspy(self, cell=None, transformation=None):
        # if self.transformation is not None:
        #     self.transform(self.transformation)
        # if transformation is not None:
        #     self.transform(transformation)
        if self.__repr__() not in list(PolygonAbstract.__committed__.keys()):
            P = gdspy.PolygonSet(
                polygons=deepcopy(self.shape.points),
                layer=self.gds_layer.number, 
                datatype=self.gds_layer.datatype,
                verbose=False
            )
            PolygonAbstract.__committed__.update({self.__repr__():P})
        else:
            P = PolygonAbstract.__committed__[self.__repr__()]
        if cell is not None:
            cell.add(P)
        return P
        
    def flat_copy(self, level=-1):
        E = self.modified_copy(
            shape=deepcopy(self.shape),
            transformation=self.transformation
        )
        E.transform_copy(self.transformation)
        return E

    def __reflect__(self, p1=(0,0), p2=(1,0), angle=None):
        for n, points in enumerate(self.shape.points):
            self.shape.points[n] = utils.reflect_algorithm(points, p1, p2)
        self.polygons = self.shape.points
        return self

    def __rotate__(self, angle=45, center=(0,0)):
        super().rotate(angle=(angle-self.direction)*np.pi/180, center=center)
        self.shape.points = self.polygons
        return self

    def __translate__(self, dx, dy):
        super().translate(dx=dx, dy=dy)
        self.shape.points = self.polygons
        return self

    def move(self, midpoint=(0,0), destination=None, axis=None):
        d, o = utils.move_algorithm(midpoint=midpoint, destination=destination, axis=axis)
        dx, dy = np.array(d) - o
        self.translate(dx, dy)
        return self

    def fillet(self, radius, angle_resolution=128, precision=0.001*1e6):
        super().fillet(radius=radius, points_per_2pi=angle_resolution, precision=precision)
        self.shape.points = self.polygons
        return self

    def stretch(self, sx, sy=None, center=(0,0)):
        super().scale(scalex=sx, scaley=sy, center=center)
        self.shape.points = self.polygons
        return self

    def transform(self, transformation):
        transformation.apply_to_object(self)
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
        gdspy.PolygonSet.__init__(
            self, self.shape.points,
            layer=self.gds_layer.number,
            datatype=self.gds_layer.datatype,
            verbose=False
        )

    def __repr__(self):
        if self is None:
            return 'Polygon is None!'
        return ("[SPiRA: Polygon] ({} center, {} area " +
                "{} vertices, layer {}, datatype {})").format(
                self.center, self.ply_area, sum([len(p) for p in self.shape.points]),
                self.gds_layer.number, self.gds_layer.datatype)

    def __str__(self):
        return self.__repr__()

    def expand_transform(self):
        self.transform(self.transformation)
        # self.transformation = None
        return self


Polygon.mixin(PolygonProperties)






