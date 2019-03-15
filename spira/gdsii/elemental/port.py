import spira
import gdspy
import pyclipper
import numpy as np
from copy import copy, deepcopy

from spira import param
from spira.visualization import color
from spira.core.initializer import ElementalInitializer
from spira.core.mixin.transform import TranformationMixin
from spira.gdsii.group import GroupElementals


class __Port__(ElementalInitializer):

    __mixins__ = [TranformationMixin]

    __committed__ = {}

    def __add__(self, other):
        if other is None:
            return self
        p1 = np.array(self.midpoint) + np.array(other)
        return p1


class PortAbstract(__Port__):

    name = param.StringField()
    midpoint = param.MidPointField()
    orientation = param.IntegerField(default=0)
    reflection = param.BoolField(default=False)

    parent = param.DataField()
    locked = param.BoolField(default=True)
    gdslayer = param.LayerField(name='PortLayer', number=64)

    __mixins__ = [GroupElementals]

    def encloses(self, polygon):
        return pyclipper.PointInPolygon(self.midpoint, polygon) != 0

    def flat_copy(self, level=-1):
        c_port = self.modified_copy(
            midpoint=deepcopy(self.midpoint),
            orientation=self.orientation,
            reflection=self.reflection,
            gdslayer=deepcopy(self.gdslayer),
            locked=self.locked
        )
        return c_port

    def reflect(self):
        """ Reflect around the x-axis. """
        self.midpoint = [self.midpoint[0], -self.midpoint[1]]
        self.orientation = -self.orientation
        self.orientation = np.mod(self.orientation, 360)
        self.reflection = True
        return self

    def rotate(self, angle=45, center=(0,0)):
        """ Rotate port around the center with angle. """
        self.orientation += angle
        self.orientation = np.mod(self.orientation, 360)
        self.midpoint = self.__rotate__(self.midpoint, angle=angle, center=center)
        return self

    def translate(self, dx, dy):
        """ Translate port by dx and dy. """
        self.midpoint = self.midpoint + np.array([dx, dy])
        return self

    def move(self, midpoint=(0,0), destination=None, axis=None):
        d, o = super().move(midpoint=midpoint, destination=destination, axis=axis)
        dx, dy = np.array(d) - o
        self.translate(dx, dy)
        return self

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
            gdslayer=self.gdslayer,
            texttype=64,
            color=color.COLOR_GHOSTWHITE
        )
        return lbl

    @property
    def key(self):
        return (self.name, self.gdslayer.number, self.midpoint[0], self.midpoint[1])


class Port(PortAbstract):
    """ Ports are objects that connect different polygons
    or references in a layout. Ports represent veritical
    connection such as vias or junctions.

    Examples
    --------
    >>> port = spira.Port()
    """

    radius = param.FloatField(default=0.25*1e6)
    color = param.ColorField(default=color.COLOR_GRAY)

    def __init__(self, port=None, elementals=None, polygon=None, **kwargs):
        ElementalInitializer.__init__(self, **kwargs)
        if elementals is not None:
            self.elementals = elementals

    def __repr__(self):
        return ("[SPiRA: Port] (name {}, number {}, midpoint {}, " +
            "radius {}, orientation {})").format(self.name,
            self.gdslayer.number, self.midpoint,
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
        layer = self.gdslayer.modified_copy(datatype=4)
        ply = spira.Polygons(shape=shape, gdslayer=layer)
        ply.move(midpoint=ply.center, destination=self.midpoint)
        return ply

    def _copy(self):
        new_port = Port(
            parent=self.parent,
            name=self.name,
            midpoint=deepcopy(self.midpoint),
            gdslayer=deepcopy(self.gdslayer),
            orientation=self.orientation,
            color=self.color
        )
        return new_port












