import spira
import gdspy
import pyclipper
import numpy as np
from copy import copy, deepcopy

from spira import param
from spira.core.initializer import BaseElement
from spira.core.mixin.transform import TranformationMixin


class __Port__(BaseElement):

    __mixins__ = [TranformationMixin]

    __committed__ = {}

    name = param.StringField()
    midpoint = param.MidPointField()
    orientation = param.IntegerField()
    parent = param.DataField()
    gdslayer = param.LayerField(name='PortLayer', number=64)
    poly_layer = param.LayerField(name='PortLayer', number=64)
    text_layer = param.LayerField(name='PortLayer', number=63)

    def __init__(self, port=None, polygon=None, **kwargs):
        BaseElement.__init__(self, **kwargs)

    @property
    def endpoints(self):
        dx = self.width/2*np.cos((self.orientation - 90)*np.pi/180)
        dy = self.width/2*np.sin((self.orientation - 90)*np.pi/180)
        left_point = self.midpoint - np.array([dx,dy])
        right_point = self.midpoint + np.array([dx,dy])
        return np.array([left_point, right_point])

    @endpoints.setter
    def endpoints(self, points):
        p1, p2 = np.array(points[0]), np.array(points[1])
        self.midpoint = (p1+p2)/2
        dx, dy = p2-p1
        self.orientation = np.arctan2(dx,dy)*180/np.pi
        self.width = np.sqrt(dx**2 + dy**2)

    @property
    def normal(self):
        dx = np.cos((self.orientation)*np.pi/180)
        dy = np.sin((self.orientation)*np.pi/180)
        return np.array([self.midpoint, self.midpoint + np.array([dx,dy])])

    @property
    def x(self):
        return self.midpoint[0]

    @property
    def y(self):
        return self.midpoint[1]

    def flat_copy(self, level=-1, commit_to_gdspy=False):
        c_port = self.modified_copy(midpoint=self.midpoint)
        if commit_to_gdspy:
            self.gdspy_write = True
        return c_port

    def point_inside(self, polygon):
        return pyclipper.PointInPolygon(self.midpoint, polygon) != 0

    def commit_to_gdspy(self, cell):
        if self.__repr__() not in list(__Port__.__committed__.keys()):
            self.polygon.commit_to_gdspy(cell)
            self.label.commit_to_gdspy(cell)
            if self.arrow:
                self.arrow.commit_to_gdspy(cell)
            __Port__.__committed__.update({self.__repr__():self})

    def reflect(self, p1=(0,1), p2=(0,0)):
        self.midpoint = [self.midpoint[0], -self.midpoint[1]]
        self.orientation = -self.orientation
        self.orientation = np.mod(self.orientation, 360)
        return self

    def rotate(self, angle=45, center=(0,0)):
        self.midpoint = self._rotate_points(self.midpoint, angle=angle, center=center)
        self.orientation += angle
        self.orientation = np.mod(self.orientation, 360)
        return self

    def translate(self, dx, dy):
        self.midpoint = self.midpoint + np.array([dx, dy])
        return self

    def stretch(self, stretch_class):
        p = stretch_class.apply(self.midpoint)
        self.midpoint = p
        return self

    def transform(self, T):
        if T['x_reflection']:
            self.reflect(p1=[0,0], p2=[1,0])
        if T['rotation']:
            self.rotate(angle=T['rotation'], center=(0,0))
        if T['origin']:
            self.translate(dx=T['origin'][0], dy=T['origin'][1])

        self.label.move(origin=self.label.position, destination=self.midpoint)
        self.polygon.move(origin=self.polygon.center, destination=self.midpoint)

        return self

    def _update(self, name, layer):
        ll = deepcopy(layer)
        ll.datatype = 65
        self.polygon.gdslayer = ll
        self.label.gdslayer = ll


class Port(__Port__):

    radius = param.FloatField(default=1)

    def __init__(self, port=None, polygon=None, **kwargs):
        from spira import shapes
        __Port__.__init__(self, port=port, polygon=polygon, **kwargs)

        shape = shapes.CircleShape(center=self.midpoint, 
                                   radius=0.25*self.radius, 
                                   gdslayer=self.gdslayer)
        pp = shapes.Circle(shape=shape)

        L = spira.Label(position=self.midpoint,
                        text=self.name,
                        gdslayer=self.gdslayer,
                        texttype=self.text_layer.number)

        self.arrow = None
        self.label = L

        if polygon is None:
            self.polygon = pp
        else:
            self.polygon = polygon

    def __repr__(self):
        return ("[SPiRA: Port] (name {}, number {}, midpoint {}, " +
                "radius {}, orientation {})").format(self.name, self.gdslayer.number, self.midpoint,
                                                    self.radius, self.orientation)

    def __str__(self):
        return self.__repr__()

    def _copy(self):
        new_port = Port(parent=self.parent,
                        name=self.name,
                        midpoint=self.midpoint,
                        radius=self.radius,
                        gdslayer=deepcopy(self.gdslayer),
                        poly_layer=deepcopy(self.poly_layer),
                        text_layer=deepcopy(self.text_layer),
                        orientation=deepcopy(self.orientation))
        return new_port









