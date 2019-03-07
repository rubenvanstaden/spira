import gdspy
import pyclipper
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
        )
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
        points = bool_operation(
            subj=self.shape.points,
            clip=other.shape.points,
            method='difference'
        )
        return points

    def __and__(self, other):
        pp = bool_operation(
            subj=other.shape.points,
            clip=self.shape.points,
            method='intersection'
        )
        # print(pp)
        if len(pp) > 0:
            return Polygons(shape=np.array(pp), gdslayer=self.gdslayer)
        else:
            return None

    def __or__(self, other):
        pp = bool_operation(
            subj=other.shape.points,
            clip=self.shape.points,
            method='union'
        )
        if len(pp) > 0:
            return Polygons(shape=pp, gdslayer=self.gdslayer)
        else:
            return None

    def is_equal_layers(self, other):
        if self.gdslayer.number == other.gdslayer.number:
            return True
        return False


class PolygonAbstract(__Polygon__):

    name = param.StringField()
    gdslayer = param.LayerField()
    direction = param.IntegerField(default=0)

    @property
    def points(self):
        return self.shape.points
        
    def encloses(self, point):
        for points in self.points:
            if pyclipper.PointInPolygon(point, points) == 0:
                return False
        return True
    
    def commit_to_gdspy(self, cell):
        if self.__repr__() not in list(PolygonAbstract.__committed__.keys()):
            P = gdspy.PolygonSet(
                polygons=deepcopy(self.shape.points), 
                layer=self.gdslayer.number, 
                datatype=self.gdslayer.datatype,
                verbose=False
            )
            cell.add(P)
            PolygonAbstract.__committed__.update({self.__repr__():P})
        else:
            cell.add(PolygonAbstract.__committed__[self.__repr__()])

    def flat_copy(self, level=-1, commit_to_gdspy=False):
        elems = []
        for points in self.shape.points:
            c_poly = self.modified_copy(shape=deepcopy([points]))
            elems.append(c_poly)
        return elems

    def reflect(self, p1=(0,0), p2=(1,0), angle=None):
        for n, points in enumerate(self.shape.points):
            self.shape.points[n] = self.__reflect__(points, p1, p2)
        self.polygons = self.shape.points
        return self

    def rotate(self, angle=45, center=(0,0)):
        super().rotate(angle=(angle-self.direction)*np.pi/180, center=center)
        self.shape.points = self.polygons
        return self

    def translate(self, dx, dy):
        super().translate(dx=dx, dy=dy)
        self.shape.points = self.polygons
        return self

    def move(self, midpoint=(0,0), destination=None, axis=None):
        d, o = super().move(midpoint=midpoint, destination=destination, axis=axis)
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
        from spira.lgm.shapes.shape import __Shape__
        from spira.lgm.shapes.shape import Shape

        if issubclass(type(shape), __Shape__):
            self.shape = shape
        elif isinstance(shape, (list, set, np.ndarray)):
            self.shape = Shape(points=shape)
        else:
            raise ValueError('Shape type not supported!')

        ElementalInitializer.__init__(self, **kwargs)
        gdspy.PolygonSet.__init__(
            self, self.shape.points,
            layer=self.gdslayer.number,
            datatype=self.gdslayer.datatype,
            verbose=False
        )

    def __repr__(self):
        if self is None:
            return 'Polygon is None!'
        return ("[SPiRA: Polygon] ({} center, {} area " +
                "{} vertices, layer {}, datatype {})").format(
                self.center, self.ply_area, sum([len(p) for p in self.shape.points]),
                self.gdslayer.number, self.gdslayer.datatype)

    def __str__(self):
        return self.__repr__()








