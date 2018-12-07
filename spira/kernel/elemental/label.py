import gdspy
import pyclipper
import numpy as np
from copy import copy, deepcopy
from spira.kernel.parameters.initializer import BaseElement
from spira.kernel import parameters as param
from spira.kernel.mixin.transform import TranformationMixin


class __Label__(gdspy.Label, BaseElement):

    __mixins__ = [TranformationMixin]

    def __init__(self, position, **kwargs):

        self.position = position

        BaseElement.__init__(self, **kwargs)

        self.id = '{}_{}'.format(self.text, Label._ID)
        Label._ID += 1

        gdspy.Label.__init__(self, text=self.text,
                             position=self.position,
                             anchor=str('o'),
                             rotation=self.rotation,
                             magnification=self.magnification,
                             x_reflection=self.x_reflection,
                             layer=self.gdslayer.number,
                             texttype=self.texttype)

    def __repr__(self):
        params = [ self.text, self.position, self.rotation,
                   self.magnification, self.x_reflection,
                   self.layer, self.texttype ]
        return ("[SPiRA: Label] (\"{0}\", at ({1[0]}, {1[1]}), " +
                "rot: {2}, mag: {3}, ref: {4}, layer: {5}, " +
                "texttype: {6})").format(*params)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return self.id == other.id

    def __deepcopy__(self, memo):
        c_label = self.modified_copy(position=self.position, 
                                     gdslayer=deepcopy(self.gdslayer))
        return c_label


class LabelAbstract(__Label__):
    """

    """

    _ID = 0

    gdslayer = param.LayerField()
    text = param.StringField()
    metals = param.ListField()
    color = param.ColorField(default='#F0B27A')

    str_anchor = param.StringField(default='o')
    rotation = param.FloatField()
    magnification = param.FloatField()
    x_reflection = param.BoolField()
    texttype = param.IntegerField()

    gdspy_commit = param.BoolField()

    __committed__ = {}

    def __init__(self, position, **kwargs):
        super().__init__(position, **kwargs)

    def commit_to_gdspy(self, cell):
        from spira.kernel.utils import scale_coord_down as scd
        if self.__repr__() not in list(LabelAbstract.__committed__.keys()):
            pos = deepcopy(self.position)
            L = gdspy.Label(self.text,
                            scd(pos),
                            anchor='o',
                            rotation=self.rotation,
                            magnification=self.magnification,
                            x_reflection=self.x_reflection,
                            layer=self.gdslayer.number,
                            texttype=self.texttype)
            cell.add(L)
            LabelAbstract.__committed__.update({self.__repr__():L})
        else:
            cell.add(LabelAbstract.__committed__[self.__repr__()])

    # def commit_to_gdspy(self, cell, gdspy_commit=None):
    #     from spira.kernel.utils import scale_coord_down as scd
    #     if gdspy_commit is not None:
    #         if self.gdspy_commit is False:
    #             L = gdspy.Label(self.text,
    #                             scd(self.position),
    #                             anchor='o',
    #                             rotation=self.rotation,
    #                             magnification=self.magnification,
    #                             x_reflection=self.x_reflection,
    #                             layer=self.gdslayer.number,
    #                             texttype=self.texttype)
    #             cell.add(L)
    #             self.gdspy_commit = True

    def reflect(self, p1=(0,1), p2=(0,0)):
        self.position = [self.position[0], -self.position[1]]
        self.rotation = self.rotation * (-1)
        self.rotation = np.mod(self.rotation, 360)
        return self

    def rotate(self, angle=45, center=(0,0)):
        self.position = self._rotate_points(self.position, angle=angle, center=[0, 0])
        self.rotation += angle
        self.rotation = np.mod(self.rotation, 360)
        return self

    def point_inside(self, polygon):
        return pyclipper.PointInPolygon(self.position, polygon) != 0

    def transform(self, transform):
        if transform['x_reflection']:
            self.reflect(p1=[0,0], p2=[1,0])
        if transform['rotation']:
            self.rotate(angle=transform['rotation'])
        if transform['origin']:
            self.translate(dx=transform['origin'][0], dy=transform['origin'][1])
        return self

    def flat_copy(self, level=-1, commit_to_gdspy=False):
        c_label = self.modified_copy(position=self.position)
        if commit_to_gdspy:
            self.gdspy_commit = True
        return c_label

    def move(self, origin=(0,0), destination=None, axis=None):
        from spira.kernel.elemental.port import PortAbstract

        if destination is None:
            destination = origin
            origin = [0,0]

        if issubclass(type(origin), PortAbstract):
            o = origin.midpoint
        elif np.array(origin).size == 2:
            o = origin
        elif origin in self.ports:
            o = self.ports[origin].midpoint
        else:
            raise ValueError("[PHIDL] [DeviceReference.move()] ``origin`` " +
                             "not array-like, a port, or port name")

        if issubclass(type(destination), PortAbstract):
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

        super().translate(dx, dy)

        return self


class Label(LabelAbstract):
    pass
