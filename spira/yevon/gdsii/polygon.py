import gdspy
import pyclipper
import hashlib
import numpy as np

from spira.core.transforms import stretching
from spira.yevon.geometry import bbox_info
from spira.yevon.utils import clipping
from copy import copy, deepcopy
from spira.yevon.visualization import color
from spira.yevon.gdsii.base import __LayerElemental__
from spira.core.parameters.variables import *
from spira.yevon.geometry.coord import CoordField, Coord
from spira.yevon.visualization.color import ColorField
from spira.core.parameters.descriptor import DataFieldDescriptor, FunctionField, DataField
from spira.yevon.geometry.ports.base import __Port__
from spira.core.transforms.stretching import *
from spira.yevon.geometry.shapes import Shape, ShapeField
from spira.yevon.geometry import shapes
from spira.yevon.gdsii.group import Group
from spira.yevon.process.gdsii_layer import Layer
from spira.yevon.process.physical_layer import PhysicalLayer
from spira.yevon.process import get_rule_deck


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


class __Polygon__(__LayerElemental__):

    shape = ShapeField()
    enable_edges = BoolField(default=True)

    def __hash__(self):
        return hash(self.id)

    # FIXME: This have to be removed, but for some reason
    # it gives an error when copying the layer object.
    def __deepcopy__(self, memo):
        return self.__class__(
            shape=deepcopy(self.shape),
            # ports=deepcopy(self.ports),
            layer=deepcopy(self.layer),
            transformation=deepcopy(self.transformation)
        )

    @property
    def count(self):
        return np.size(self.shape.points, 0)

    @property
    def bbox_info(self):
        return self.shape.bbox_info.transform_copy(self.transformation)

    @property
    def hash_polygon(self):
        # pts = np.array([self.shape.points])
        return np.sort([hashlib.sha1(p).digest() for p in self.points])

    def encloses(self, point):
        return not pyclipper.PointInPolygon(point, self.points) == 0

    def flat_copy(self, level=-1):
        # E = self.modified_copy(
        # E = self.
        #     shape=deepcopy(self.shape), 
        #     layer=deepcopy(self.layer), 
        #     transformation=self.transformation
        # )
        E = deepcopy(self)
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
        """
        The elemental by moving the subject port, without 
        distorting the entire elemental. Note: The opposite 
        port position is used as the stretching center.
        """
        opposite_port = bbox_info.get_opposite_boundary_port(self, port)
        T = stretching.stretch_elemental_by_port(self, opposite_port, port, destination)
        T.apply(self)
        return self

    def id_string(self):
        return self.__repr__()
        # return str(self.hash_polygon)

    def move(self, midpoint=(0,0), destination=None, axis=None):
        """  """

        if destination is None:
            destination = midpoint
            midpoint = Coord(0,0)

        if isinstance(midpoint, Coord):
            m = midpoint
        elif np.array(midpoint).size == 2:
            m = Coord(midpoint)
        elif issubclass(type(midpoint), __Port__):
            m = midpoint.midpoint
        else:
            raise ValueError('Midpoint error')

        if issubclass(type(destination), __Port__):
            d = destination.midpoint
        if isinstance(destination, Coord):
            d = destination
        elif np.array(destination).size == 2:
            d = Coord(destination)
        else:
            raise ValueError('Destination error')

        dxdy = d - m 
        self.translate(dxdy)
        return self


class Polygon(__Polygon__):
    """ Elemental that connects shapes to the GDSII file format.
    Polygon are objects that represents the shapes in a layout.

    Examples
    --------
    >>> layer = spira.Layer(number=99)
    >>> rect_shape = spira.RectangleShape(p1=[0,0], p2=[1,1])
    >>> ply = spira.Polygon(shape=rect_shape, layer=layer)
    """

    def get_alias(self):
        if not hasattr(self, '__alias__'):
            self.__alias__ = self.layer.name
        return self.__alias__

    def set_alias(self, value):
        if value is not None:
            self.__alias__ = value

    alias = FunctionField(get_alias, set_alias, doc='Functions to generate an alias for cell name.')

    def __init__(self, shape, layer, **kwargs):
        super().__init__(shape=shape, layer=layer, **kwargs)

    def __repr__(self):
        if self is None:
            return 'Polygon is None!'
        return ("[SPiRA: Polygon {} {}] (center {}, area {}, vertices {}, layer {}, datatype {}, hash {})").format(
            self.alias, 0,
            self.bbox_info.center,
            self.area,
            sum([len(p) for p in self.shape.points]),
            self.layer.number,
            self.layer.datatype,
            self.hash_polygon
        )

    def __str__(self):
        return self.__repr__()

    def convert_to_gdspy(self, transformation=None):
        """
        Converts a SPiRA polygon to a Gdspy polygon.
        The extra transformation parameter is the
        polygon edge ports.
        """
        layer = RDD.GDSII.EXPORT_LAYER_MAP[self.layer]
        T = self.transformation + transformation
        shape = deepcopy(self.shape).transform(T)
        # shape = self.shape
        return gdspy.Polygon(
            points=shape.points,
            layer=layer.number,
            datatype=layer.datatype,
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


def Rectangle(layer, p1=(0,0), p2=(2,2), center=(0,0), alias=None):
    """ Creates a rectangular shape that can be used in 
    GDSII format as a polygon object.

    Example
    -------
    >>> p = spira.Rectangle(p1=(0,0), p2=(10,0), layer=RDD.PLAYER.M6)
    >>> [SPiRA: Rectangle] ()
    """
    shape = shapes.RectangleShape(p1=p1, p2=p2)
    return Polygon(alias=alias, shape=shape, layer=layer)


def Box(layer, width=1, height=1, center=(0,0), alias=None, enable_edges=False):
    """ Creates a box shape that can be used in 
    GDSII format as a polygon object.

    Example
    -------
    >>> p = spira.Box(p1=(0,0), p2=(10,0), layer=RDD.PLAYER.M6)
    >>> [SPiRA: Rectangle] ()
    """
    shape = shapes.BoxShape(width=width, height=height)
    return Polygon(alias=alias, shape=shape, layer=layer, enable_edges=enable_edges)


def Circle(layer, box_size=(1,1), angle_step=1, center=(0,0), alias=None):
    """ Creates a circle shape that can be used in 
    GDSII format as a polygon object.

    Example
    -------
    >>> p = spira.Circle(p1=(0,0), p2=(10,0), layer=RDD.PLAYER.M6)
    >>> [SPiRA: Rectangle] ()
    """
    shape = shapes.CircleShape(box_size=box_size, angle_step=angle_step)
    return Polygon(alias=alias, shape=shape, layer=layer)


def Convex(layer, radius=1.0*1e6, num_sides=6, center=(0,0), alias=None):
    """ Creates a circle shape that can be used in 
    GDSII format as a polygon object.

    Example
    -------
    >>> p = spira.Circle(p1=(0,0), p2=(10,0), layer=RDD.PLAYER.M6)
    >>> [SPiRA: Rectangle] ()
    """
    shape = shapes.ConvexShape(radius=radius, num_sides=num_sides)
    return Polygon(alias=alias, shape=shape, layer=layer)


def Cross(layer, box_size=20*1e6, thickness=5*1e6, center=(0,0), alias=None):
    """ Creates a circle shape that can be used in 
    GDSII format as a polygon object.

    Example
    -------
    >>> p = spira.Circle(p1=(0,0), p2=(10,0), layer=RDD.PLAYER.M6)
    >>> [SPiRA: Rectangle] ()
    """
    shape = shapes.CrossShape(box_size=box_size, thickness=thickness)
    return Polygon(alias=alias, shape=shape, layer=layer)


def Wedge(layer, begin_coord=(0,0), end_coord=(10*1e6,0), begin_width=3*1e6, end_width=1*1e6, center=(0,0), alias=None):
    """ Creates a circle shape that can be used in 
    GDSII format as a polygon object.

    Example
    -------
    >>> p = spira.Circle(p1=(0,0), p2=(10,0), layer=RDD.PLAYER.M6)
    >>> [SPiRA: Rectangle] ()
    """
    shape = shapes.WedgeShape(
        begin_coord=begin_coord, 
        end_coord=end_coord, 
        begin_width=begin_width, 
        end_width=end_width
    )
    return Polygon(alias=alias, shape=shape, layer=layer)


def Parabolic(layer, begin_coord=(0,0), end_coord=(10*1e6,0), begin_width=3*1e6, end_width=1*1e6, center=(0,0), alias=None):
    """ Creates a circle shape that can be used in 
    GDSII format as a polygon object.

    Example
    -------
    >>> p = spira.Circle(p1=(0,0), p2=(10,0), layer=RDD.PLAYER.M6)
    >>> [SPiRA: Rectangle] ()
    """
    shape = shapes.ParabolicShape(
        begin_coord=begin_coord, 
        end_coord=end_coord, 
        begin_width=begin_width, 
        end_width=end_width
    )
    return Polygon(alias=alias, shape=shape, layer=layer)

