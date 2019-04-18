import spira.all as spira
import gdspy
import pyclipper
import numpy as np
from copy import copy, deepcopy
from numpy.linalg import norm
from spira.yevon import utils

from spira.core import param
from spira.yevon.visualization import color
from spira.yevon.gdsii.base import __Elemental__
from spira.yevon.rdd import get_rule_deck

from spira.core.param.variables import *
from spira.yevon.visualization.color import ColorField
from spira.yevon.layer import LayerField
from spira.core.descriptor import DataField
from spira.yevon.geometry.coord import CoordField


__all__ = ['Port', 'PortField']


RDD = get_rule_deck()


class __Port__(__Elemental__):
    __committed__ = {}

    def __add__(self, other):
        if other is None:
            return self
        p1 = np.array(self.midpoint) + np.array(other)
        return p1


class PortAbstract(__Port__):

    name = StringField()
    midpoint = CoordField()
    orientation = NumberField(default=0)

    parent = DataField()
    locked = BoolField(default=True)
    gds_layer = LayerField(name='PortLayer', number=64)
    text_type = NumberField(default=RDD.GDSII.TEXT)
    pid = StringField()

    def flat_copy(self, level=-1):
        E = self.modified_copy(transformation=self.transformation)
        E.transform_copy(self.transformation)
        return E

    @property
    def x(self):
        return self.midpoint[0]

    @property
    def y(self):
        return self.midpoint[1]

    def encloses(self, polygon):
        return pyclipper.PointInPolygon(self.midpoint, polygon) != 0

    def transform(self, transformation):
        transformation.apply_to_object(self)
        return self

    def __reflect__(self):
        """ Reflect around the x-axis. """
        self.midpoint = [self.midpoint[0], -self.midpoint[1]]
        self.orientation = -self.orientation
        self.orientation = np.mod(self.orientation, 360)
        # self.reflection = True
        return self

    def __rotate__(self, angle=45, center=(0,0)):
        """ Rotate port around the center with angle. """
        self.orientation += angle
        self.orientation = np.mod(self.orientation, 360)
        self.midpoint = utils.rotate_algorithm(self.midpoint, angle=angle, center=center)
        return self

    def __translate__(self, dx, dy):
        """ Translate port by dx and dy. """
        self.midpoint = self.midpoint + np.array([dx, dy])
        return self

    def move(self, midpoint=(0,0), destination=None, axis=None):
        d, o = super().move(midpoint=midpoint, destination=destination, axis=axis)
        dx, dy = np.array(d) - o
        self.__translate__(dx, dy)
        return self

    def distance(self, other):
        return norm(np.array(self.midpoint) - np.array(other.midpoint))

    def connect(self, S, P):
        """ Connects the port to a specific polygon in a cell reference. """
        self.node_id = '{}_{}'.format(S.ref.name, P.id)

    @property
    def normal(self):
        dx = np.cos((self.orientation)*np.pi/180)
        dy = np.sin((self.orientation)*np.pi/180)
        return np.array([self.midpoint, self.midpoint + np.array([dx,dy])])

    @property
    def label(self):
        lbl = spira.Label(
            position=self.midpoint,
            text=self.name,
            gds_layer=self.gds_layer,
            texttype=self.text_type,
            color=color.COLOR_GHOSTWHITE
        )
        return lbl

    @property
    def key(self):
        return (self.name, self.gds_layer.number, self.midpoint[0], self.midpoint[1])


class Port(PortAbstract):
    """ Ports are objects that connect different polygons
    or references in a layout. Ports represent veritical
    connection such as vias or junctions.

    Examples
    --------
    >>> port = spira.Port()
    """

    radius = FloatField(default=0.25*1e6)
    color = ColorField(default=color.COLOR_GRAY)

    def __init__(self, port=None, elementals=None, polygon=None, **kwargs):
        __Elemental__.__init__(self, **kwargs)
        if elementals is not None:
            self.elementals = elementals

    def __repr__(self):
        return ("[SPiRA: Port] (name {}, number {}, datatype {}, midpoint {}, " +
            "radius {}, orientation {})").format(self.name,
            self.gds_layer.number, self.gds_layer.datatype, self.midpoint,
            self.radius, self.orientation
        )

    def commit_to_gdspy(self, cell=None):
        if self.__repr__() not in list(__Port__.__committed__.keys()):
            self.surface.commit_to_gdspy(cell=cell)
            self.label.commit_to_gdspy(cell=cell)
            __Port__.__committed__.update({self.__repr__(): self})
        else:
            p = __Port__.__committed__[self.__repr__()]
            p.surface.commit_to_gdspy(cell=cell)
            p.label.commit_to_gdspy(cell=cell)

    @property
    def surface(self):
        from spira import shapes
        shape = shapes.CircleShape(
            center=self.midpoint,
            box_size=[self.radius, self.radius]
        )
        layer = deepcopy(self.gds_layer)
        ply = spira.Polygon(shape=shape, gds_layer=layer)
        ply.move(midpoint=ply.center, destination=self.midpoint)
        return ply


def PortField(midpoint=[0, 0], **kwargs):
    if 'default' not in kwargs:
        kwargs['default'] = Port(midpoint=midpoint)
    R = RestrictType(Port)
    return DataFieldDescriptor(restrictions=R, **kwargs)










