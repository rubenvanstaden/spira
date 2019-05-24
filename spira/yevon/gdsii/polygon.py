import gdspy
import pyclipper
import hashlib
import numpy as np

from spira.core.transforms import stretching
from spira.yevon.geometry import bbox_info
from spira.yevon.utils import clipping
from copy import copy, deepcopy
from spira.yevon.visualization import color
from spira.yevon.gdsii.base import __Elemental__
from spira.yevon.layer import LayerField
from spira.core.parameters.variables import *
from spira.yevon.geometry.coord import CoordField, Coord
from spira.yevon.visualization.color import ColorField
from spira.core.parameters.descriptor import DataFieldDescriptor, FunctionField, DataField
from spira.yevon.geometry.ports.base import __Port__
from spira.core.transforms.stretching import *
from spira.yevon.geometry.shapes import Shape, ShapeField
from spira.yevon.geometry import shapes
from spira.yevon.rdd.layer import PhysicalLayerField
from spira.yevon.gdsii.group import Group
from spira.yevon.rdd import get_rule_deck


RDD = get_rule_deck()


__all__ = [
    'Polygon',
    'Rectangle',
    'Box',
    'Circle',
    'Convex',
    'Cross',
    'Wedge',
    'Parabolic',
    'PolygonGroup'
]


class __Polygon__(gdspy.PolygonSet, __Elemental__):

    ps_layer = PhysicalLayerField(default=RDD.PLAYER.COU)

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __copy__(self):
        return self.modified_copy(
            shape=deepcopy(self.shape),
            gds_layer=deepcopy(self.gds_layer)
        )

    # def __deepcopy__(self, memo):
    #     ply = self.modified_copy(
    #         shape=deepcopy(self.shape),
    #         ports=deepcopy(self.ports),
    #         gds_layer=deepcopy(self.gds_layer),
    #         ps_layer=deepcopy(self.ps_layer)
    #     )
    #     return ply

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
        points = clipping.boolean(
            subj=self.shape.points,
            clip=other.shape.points,
            method='not'
        )
        return points

    def __and__(self, other):
        pp = clipping.boolean(
            subj=[other.shape.points],
            clip=[self.shape.points],
            method='and'
        )
        if len(pp) > 0:
            return Polygon(shape=np.array(pp), gds_layer=self.gds_layer)
        else:
            return None

    def __or__(self, other):
        pp = clipping.boolean(
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

    @property
    def count(self):
        return np.size(self.shape.points, 0)

    @property
    def layer_number(self):
        return self.ps_layer.layer.number

    @property
    def layer_datatype(self):
        return self.ps_layer.layer.datatype

    @property
    def bbox_info(self):
        return self.shape.bbox_info.transform_copy(self.transformation)

    @property
    def hash_polygon(self):
        pts = np.array([self.shape.points])
        polygon_hashes = np.sort([hashlib.sha1(p).digest() for p in pts])
        return polygon_hashes

    def encloses(self, point):
        if pyclipper.PointInPolygon(point, self.points) == 0:
            return False
        return True

    def flat_copy(self, level=-1):
        E = self.modified_copy(shape=deepcopy(self.shape), transformation=self.transformation)
        return E.transform_copy(self.transformation)

    def fillet(self, radius, angle_resolution=128, precision=0.001*1e6):
        super().fillet(radius=radius, points_per_2pi=angle_resolution, precision=precision)
        self.shape.points = self.polygons
        return self

    def stretch(self, factor=(1,1), center=(0,0)):
        T = spira.Stretch(stretch_factor=factor, stretch_center=center)
        return T.apply(self)

    def stretch_copy(self, factor=(1,1), center=(0,0)):
        T = spira.Stretch(stretch_factor=factor, stretch_center=center)
        return T.apply_copy(self)

    def stretch_port(self, port, destination):
        """ The elemental by moving the subject port, without distorting the entire elemental. 
        Note: The opposite port position is used as the stretching center."""
        opposite_port = bbox_info.get_opposite_boundary_port(self, port)
        return stretching.stretch_elemental_by_port(self, opposite_port, port, destination)

    def id_string(self):
        return self.__repr__()


class Polygon(PolygonAbstract):
    """ Elemental that connects shapes to the GDSII file format.
    Polygon are objects that represents the shapes in a layout.

    Examples
    --------
    >>> layer = spira.Layer(number=99)
    >>> rect_shape = spira.RectangleShape(p1=[0,0], p2=[1,1])
    >>> ply = spira.Polygon(shape=rect_shape, gds_layer=layer)
    """

    # _ID = 0

    shape = ShapeField()
    enable_edges = BoolField(default=True)
    color = ColorField(default=color.COLOR_BLUE_VIOLET)

    def get_alias(self):
        if not hasattr(self, '__alias__'):
            self.__alias__ = self.gds_layer.name
        return self.__alias__

    def set_alias(self, value):
        if value is not None:
            self.__alias__ = value

    alias = FunctionField(get_alias, set_alias, doc='Functions to generate an alias for cell name.')

    def __init__(self, **kwargs):
        __Elemental__.__init__(self, **kwargs)
        gdspy.PolygonSet.__init__(self,
            polygons=self.shape.points,
            layer=self.gds_layer.number,
            datatype=self.gds_layer.datatype,
            verbose=False
        )
        # Polygon._ID += 1

    def __repr__(self):
        if self is None:
            return 'Polygon is None!'
        return ("[SPiRA: Polygon {} {}] (center {}, area {}, vertices {}, layer {}, datatype {}, hash {})").format(
            self.alias, 0,
            self.bbox_info.center,
            self.ply_area,
            sum([len(p) for p in self.shape.points]),
            self.layer_number,
            self.layer_datatype,
            self.hash_polygon
        )

    def __str__(self):
        return self.__repr__()

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

    def convert_to_gdspy(self, transformation=None):
        """ Converts a SPiRA polygon to a Gdspy polygon.
        The extra transformation parameter is the 
        polygon edge ports. """
        T = self.transformation + transformation
        shape = self.shape.transform(T)
        return gdspy.Polygon(
            points=shape.points,
            layer=self.layer_number,
            datatype=self.layer_datatype,
            verbose=False
        )


class PolygonGroup(Group, Polygon):
    """ Collection of polygon elementals. Boolean
    operation can be applied on these polygons.

    Example
    -------
    >>> cp = spira.PolygonCollection()
    """

    def create_elementals(self, elems):

        return elems


def Rectangle(ps_layer, p1=(0,0), p2=(2,2), center=(0,0), alias=None):
    """ Creates a rectangular shape that can be used in 
    GDSII format as a polygon object.

    Example
    -------
    >>> p = spira.Rectangle(p1=(0,0), p2=(10,0), ps_layer=RDD.PLAYER.M6)
    >>> [SPiRA: Rectangle] ()
    """
    shape = shapes.RectangleShape(p1=p1, p2=p2)
    return Polygon(alias=alias, shape=shape, ps_layer=ps_layer)


def Box(ps_layer, width=1, height=1, center=(0,0), alias=None):
    """ Creates a box shape that can be used in 
    GDSII format as a polygon object.

    Example
    -------
    >>> p = spira.Box(p1=(0,0), p2=(10,0), ps_layer=RDD.PLAYER.M6)
    >>> [SPiRA: Rectangle] ()
    """
    shape = shapes.BoxShape(width=width, height=height)
    return Polygon(alias=alias, shape=shape, ps_layer=ps_layer)


def Circle(ps_layer, box_size=(1,1), angle_step=1, center=(0,0), alias=None):
    """ Creates a circle shape that can be used in 
    GDSII format as a polygon object.

    Example
    -------
    >>> p = spira.Circle(p1=(0,0), p2=(10,0), ps_layer=RDD.PLAYER.M6)
    >>> [SPiRA: Rectangle] ()
    """
    shape = shapes.CircleShape(box_size=box_size, angle_step=angle_step)
    return Polygon(alias=alias, shape=shape, ps_layer=ps_layer)


def Convex(ps_layer, radius=1.0*1e6, num_sides=6, center=(0,0), alias=None):
    """ Creates a circle shape that can be used in 
    GDSII format as a polygon object.

    Example
    -------
    >>> p = spira.Circle(p1=(0,0), p2=(10,0), ps_layer=RDD.PLAYER.M6)
    >>> [SPiRA: Rectangle] ()
    """
    shape = shapes.ConvexShape(radius=radius, num_sides=num_sides)
    return Polygon(alias=alias, shape=shape, ps_layer=ps_layer)


def Cross(ps_layer, box_size=20*1e6, thickness=5*1e6, center=(0,0), alias=None):
    """ Creates a circle shape that can be used in 
    GDSII format as a polygon object.

    Example
    -------
    >>> p = spira.Circle(p1=(0,0), p2=(10,0), ps_layer=RDD.PLAYER.M6)
    >>> [SPiRA: Rectangle] ()
    """
    shape = shapes.CrossShape(box_size=box_size, thickness=thickness)
    return Polygon(alias=alias, shape=shape, ps_layer=ps_layer)


def Wedge(ps_layer, begin_coord=(0,0), end_coord=(10*1e6,0), begin_width=3*1e6, end_width=1*1e6, center=(0,0), alias=None):
    """ Creates a circle shape that can be used in 
    GDSII format as a polygon object.

    Example
    -------
    >>> p = spira.Circle(p1=(0,0), p2=(10,0), ps_layer=RDD.PLAYER.M6)
    >>> [SPiRA: Rectangle] ()
    """
    shape = shapes.WedgeShape(
        begin_coord=begin_coord, 
        end_coord=end_coord, 
        begin_width=begin_width, 
        end_width=end_width
    )
    return Polygon(alias=alias, shape=shape, ps_layer=ps_layer)


def Parabolic(ps_layer, begin_coord=(0,0), end_coord=(10*1e6,0), begin_width=3*1e6, end_width=1*1e6, center=(0,0), alias=None):
    """ Creates a circle shape that can be used in 
    GDSII format as a polygon object.

    Example
    -------
    >>> p = spira.Circle(p1=(0,0), p2=(10,0), ps_layer=RDD.PLAYER.M6)
    >>> [SPiRA: Rectangle] ()
    """
    shape = shapes.ParabolicShape(
        begin_coord=begin_coord, 
        end_coord=end_coord, 
        begin_width=begin_width, 
        end_width=end_width
    )
    return Polygon(alias=alias, shape=shape, ps_layer=ps_layer)

