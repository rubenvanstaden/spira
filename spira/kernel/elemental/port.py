import spira
import gdspy
import pyclipper
import numpy as np

from spira.kernel import parameters as param
from spira.kernel.parameters.initializer import BaseElement
from spira.lgm.shape.basic import Rectangle
from spira.lgm.shape.basic import Circle
from spira.kernel.elemental.polygons import PolygonAbstract
from spira.kernel.mixin.transform import TranformationMixin
from spira.rdd import get_rule_deck


RDD = get_rule_deck()


class __Port__(BaseElement):

    __mixins__ = [TranformationMixin]

    def __init__(self, port=None, polygon=None, **kwargs):
        BaseElement.__init__(self, **kwargs)

        # if self.extern_polygon:
        #     pp = self.extern_polygon
        if self.length:
            layer = spira.Layer(name='Rectangle', number=65)
            pp = Rectangle(point1=[0, 0],
                           point2=[self.width, self.length],
                           layer=layer)

            pp.rotate(angle=self.orientation, center=self.midpoint)
            pp.move(origin=pp.center, destination=self.midpoint)
        else:
            pp = Circle(self.midpoint, radius=0.25*self.width)

        L = spira.Label(position=self.midpoint,
                        text=self.name,
                        gdslayer=self.text_layer,
                        texttype=self.text_layer.datatype)

        self.label = L

        if polygon is None:
            self.polygon = pp
        else:
            self.polygon = polygon

    def __repr__(self):
        return ("[SPiRA: Port] (name {}, number {}, midpoint {}, " +
                "width {}, orientation {})").format(self.name, self.gdslayer.number, self.midpoint,
                                                    self.width, self.orientation)

    def __str__(self):
        return self.__repr__()


class PortAbstract(__Port__):

    name = param.StringField()
    midpoint = param.PointField()
    width = param.FloatField(default=1)
    orientation = param.IntegerField()
    length = param.FloatField()
    parent = param.DataField()
    extern_polygon = param.PolygonField()
    gdslayer = param.LayerField(name='PortLayer', number=RDD.GDSII.TERM)
    poly_layer = param.LayerField(name='PortLayer', number=RDD.GDSII.TERM)
    text_layer = param.LayerField(name='PortLayer', number=RDD.GDSII.TEXT)

    gdspy_commit = param.BoolField()

    def __init__(self, port=None, polygon=None, **kwargs):
        super().__init__(port=None, polygon=None, **kwargs)

    @property
    def endpoints(self):
        dx = self.width/2*np.cos((self.orientation - 90)*pi/180)
        dy = self.width/2*np.sin((self.orientation - 90)*pi/180)
        left_point = self.midpoint - np.array([dx,dy])
        right_point = self.midpoint + np.array([dx,dy])
        return np.array([left_point, right_point])

    @endpoints.setter
    def endpoints(self, points):
        p1, p2 = np.array(points[0]), np.array(points[1])
        self.midpoint = (p1+p2)/2
        dx, dy = p2-p1
        self.orientation = np.arctan2(dx,dy)*180/pi
        self.width = sqrt(dx**2 + dy**2)

    @property
    def normal(self):
        dx = np.cos((self.orientation)*pi/180)
        dy = np.sin((self.orientation)*pi/180)
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

    def commit_to_gdspy(self, cell, gdspy_commit=None):
        if gdspy_commit is not None:
            if self.gdspy_commit is False:

                self.gdspy_commit = True

                self.polygon.commit_to_gdspy(cell)
                self.label.commit_to_gdspy(cell)

        # if gdspy_commit is None:
        #     if not self.gdspy_commit:
        #         self.polygon.commit_to_gdspy(cell)
        #         self.label.commit_to_gdspy(cell)
        # else:
        #     self.polygon.commit_to_gdspy(cell)
        #     self.label.commit_to_gdspy(cell)

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
            self.rotate(angle=T['rotation'], center=(0,0))
            self.translate(dx=T['origin'][0],
                           dy=T['origin'][1])
            # self.label.reflect(p1=[0,0], p2=[1,0])
            # self.label.rotate(angle=T['rotation'], center=(0,0))
            # self.label.translate(dx=T['origin'][0],
            #                dy=T['origin'][1])
        else:
            self.rotate(angle=T['rotation'], center=(0,0))
            self.translate(dx=T['origin'][0],
                           dy=T['origin'][1])
            # self.label.rotate(angle=T['rotation'], center=(0,0))
            # self.label.translate(dx=T['origin'][0],
            #                dy=T['origin'][1])

        self.label.move(origin=self.label.position, destination=self.midpoint)
        self.polygon.move(origin=self.polygon.center, destination=self.midpoint)

        return self

    def _copy(self):
        new_port = Port(parent=self.parent,
                        name=self.name,
                        midpoint=self.midpoint,
                        width=self.width,
                        length=self.length,
                        gdslayer=self.gdslayer,
                        poly_layer=self.poly_layer,
                        text_layer=self.text_layer,
                        orientation=self.orientation)
        return new_port

    def update(self, name, layer):
        self.gdslayer = layer
        self.text_layer = spira.Layer(number=layer.number, datatype=RDD.GDSII.TEXT)
        self.name += '_' + str(name)


class Port(PortAbstract):
    pass
