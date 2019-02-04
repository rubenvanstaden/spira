import spira
import gdspy
import pyclipper
import numpy as np
from copy import copy, deepcopy

from spira import param
from spira.core.initializer import ElementalInitializer
from spira.core.mixin.transform import TranformationMixin


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
    orientation = param.IntegerField()
    parent = param.DataField()
    gdslayer = param.LayerField(name='PortLayer', number=64)
    poly_layer = param.LayerField(name='PortLayer', number=64)
    text_layer = param.LayerField(name='PortLayer', number=63)

    def __init__(self, port=None, polygon=None, **kwargs):
        super().__init__(**kwargs)

        self.orientation = np.mod(self.orientation, 360)

        L = spira.Label(position=self.midpoint,
            text=self.name,
            gdslayer=self.gdslayer,
            texttype=self.text_layer.number
        )
        self.label = L
        self.arrow = None

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

    def point_inside(self, polygon):
        return pyclipper.PointInPolygon(self.midpoint, polygon) != 0

    def flat_copy(self, level=-1, commit_to_gdspy=False):
        c_port = self.modified_copy(midpoint=self.midpoint)
        if commit_to_gdspy:
            self.gdspy_write = True
        return c_port

    def commit_to_gdspy(self, cell):
        if self.__repr__() not in list(__Port__.__committed__.keys()):
            # self.polygon.rotate(angle=self.orientation)
            # self.polygon.move(midpoint=self.polygon.center, destination=self.midpoint)
            self.polygon.commit_to_gdspy(cell)
            self.label.commit_to_gdspy(cell)
            if self.arrow:
                # print(self.orientation)
                # self.arrow.rotate(angle=45)
                # self.arrow.rotate(angle=90)
                # self.arrow.rotate(angle=90-self.orientation)
                self.arrow.move(midpoint=self.arrow.center, destination=self.midpoint)
                self.arrow.commit_to_gdspy(cell)
            __Port__.__committed__.update({self.__repr__():self})

    def reflect(self):
        """ Reflect around the x-axis. """
        self.midpoint = [self.midpoint[0], -self.midpoint[1]]
        self.orientation = -self.orientation
        self.orientation = np.mod(self.orientation, 360)

        self.polygon.reflect()

        if self.arrow:
            self.arrow.reflect()

        return self

    def rotate(self, angle=45, center=(0,0)):
        """ Rotate port around the center with angle. """
        self.midpoint = self.__rotate__(self.midpoint, angle=angle, center=center)
        self.orientation += angle
        self.orientation = np.mod(self.orientation, 360)

        self.polygon.rotate(angle=self.orientation)

        if self.arrow:
            # self.arrow.rotate(angle=angle)
            self.arrow.rotate(angle=np.mod(angle, 90))

        return self

    def translate(self, dx, dy):
        """ Translate port by dx and dy. """
        self.midpoint = self.midpoint + np.array([dx, dy])
        return self

    def move(self, midpoint=(0,0), destination=None, axis=None):
        from spira.gdsii.elemental.port import __Port__

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

        self.label.move(midpoint=self.label.position, destination=self.midpoint)
        self.polygon.move(midpoint=self.polygon.center, destination=self.midpoint)
        if self.arrow:
            self.arrow.move(midpoint=self.polygon.center, destination=self.midpoint)

        return self

    def stretch(self, stretch_class):
        """ Stretch port by with the given stretch class. """
        p = stretch_class.apply(self.midpoint)
        self.midpoint = p
        return self

    def transform(self, T):
        """ Transform port with the given transform class. """
        if T['reflection']:
            self.reflect()
            self.label.reflect()
            self.polygon.reflect()
            if self.arrow:
                self.arrow.reflect()
        if T['rotation']:
            self.rotate(angle=T['rotation'], center=(0,0))
            self.label.rotate(angle=T['rotation'])
            self.polygon.rotate(angle=T['rotation'])
            if self.arrow:
                self.arrow.rotate(angle=T['rotation'])
        if T['midpoint']:
            self.translate(dx=T['midpoint'][0], dy=T['midpoint'][1])
            self.label.move(midpoint=self.label.position, destination=self.midpoint)
            self.polygon.move(midpoint=self.polygon.center, destination=self.midpoint)
            if self.arrow:
                self.arrow.move(midpoint=self.polygon.center, destination=self.midpoint)

        return self

    def _update(self, name, layer):
        ll = deepcopy(layer)
        ll.datatype = 65
        self.polygon.gdslayer = ll
        self.label.gdslayer = ll


class Port(PortAbstract):
    """ Ports are objects that connect different polygons
    or references in a layout. Ports represent vertical
    connection such as vias or junctions.

    Examples
    --------
    >>> port = spira.Port()
    """

    edge_width = param.FloatField(default=0.25)

    def __init__(self, port=None, polygon=None, **kwargs):
        super().__init__(port=port, polygon=polygon, **kwargs)

        if polygon is None:
            from spira import shapes
            shape = shapes.CircleShape(
                center=self.midpoint,
                box_size=[self.edge_width, self.edge_width]
            )
            pp = spira.Polygons(shape=shape, gdslayer=self.gdslayer)
            pp.move(midpoint=pp.center, destination=self.midpoint)
            self.polygon = pp
        else:
            self.polygon = polygon

    def __repr__(self):
        return ("[SPiRA: Port] (name {}, number {}, midpoint {}, " +
            "radius {}, orientation {})").format(self.name,
            self.gdslayer.number, self.midpoint,
            self.edge_width, self.orientation
        )

    def _copy(self):
        new_port = Port(parent=self.parent,
            polygon=deepcopy(self.polygon),
            name=self.name,
            midpoint=deepcopy(self.midpoint),
            edge_width=self.edge_width,
            gdslayer=deepcopy(self.gdslayer),
            poly_layer=deepcopy(self.poly_layer),
            text_layer=deepcopy(self.text_layer),
            orientation=deepcopy(self.orientation))
        return new_port













