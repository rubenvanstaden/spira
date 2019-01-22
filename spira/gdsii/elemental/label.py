import spira
import gdspy
import pyclipper
import numpy as np
from copy import copy, deepcopy
from spira.core.initializer import ElementalInitializer
from spira import param
from spira.core.mixin.transform import TranformationMixin


class __Label__(gdspy.Label, ElementalInitializer):

    __mixins__ = [TranformationMixin]

    __committed__ = {}

    def __init__(self, position, **kwargs):

        # TODO: Convert to Point object.
        if isinstance(position, (list, tuple, set, np.ndarray)):
            self.position = list(position)
        else:
            raise ValueError('Position type not supported!')

        ElementalInitializer.__init__(self, **kwargs)
        gdspy.Label.__init__(self,
            text=self.text,
            position=self.position,
            anchor=str('o'),
            rotation=self.rotation,
            magnification=self.magnification,
            x_reflection=self.reflection,
            layer=self.gdslayer.number,
            texttype=self.texttype
        )

    def __eq__(self, other):
        return self.id == other.id

    def __deepcopy__(self, memo):
        c_label = self.modified_copy(
            position=deepcopy(self.position),
            gdslayer=deepcopy(self.gdslayer)
        )
        return c_label


class LabelAbstract(__Label__):

    gdslayer = param.LayerField()
    color = param.StringField(default='#g54eff')
    text = param.StringField()
    id0 = param.StringField()
    str_anchor = param.StringField(default='o')
    rotation = param.FloatField(default=0)
    magnification = param.FloatField(default=1)
    reflection = param.BoolField(default=False)
    texttype = param.IntegerField(default=0)
    gdspy_commit = param.BoolField()

    def __init__(self, position, **kwargs):
        super().__init__(position, **kwargs)

    def commit_to_gdspy(self, cell):
        if self.__repr__() not in list(LabelAbstract.__committed__.keys()):
            L = gdspy.Label(self.text,
                deepcopy(self.position),
                anchor='o',
                rotation=self.rotation,
                magnification=self.magnification,
                x_reflection=self.reflection,
                layer=self.gdslayer.number,
                texttype=self.texttype
            )
            cell.add(L)
            LabelAbstract.__committed__.update({self.__repr__():L})
        else:
            cell.add(LabelAbstract.__committed__[self.__repr__()])

    def reflect(self, p1=(0,1), p2=(0,0)):
        self.position = [self.position[0], -self.position[1]]
        self.rotation = self.rotation * (-1)
        self.rotation = np.mod(self.rotation, 360)
        return self

    def rotate(self, angle=45, center=(0,0)):
        self.position = self.__rotate__(self.position, angle=angle, center=[0, 0])
        self.rotation += angle
        self.rotation = np.mod(self.rotation, 360)
        return self

    def point_inside(self, ply):
        if isinstance(ply, spira.Polygons):
            return pyclipper.PointInPolygon(self.position, ply.shape.points) != 0
        elif isinstance(ply, (list, set, np.ndarray)):
            return pyclipper.PointInPolygon(self.position, ply) != 0
        else:
            raise ValueError('Not Implemented!')

    def transform(self, transform):
        if transform['reflection']:
            self.reflect(p1=[0,0], p2=[1,0])
        if transform['rotation']:
            self.rotate(angle=transform['rotation'])
        if transform['midpoint']:
            self.translate(dx=transform['midpoint'][0], dy=transform['midpoint'][1])
        return self

    def flat_copy(self, level=-1, commit_to_gdspy=False):
        c_label = self.modified_copy(position=self.position)
        if commit_to_gdspy:
            self.gdspy_commit = True
        return c_label

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

        super().translate(dx, dy)

        return self


class Label(LabelAbstract):
    """

    """

    def __init__(self, position, **kwargs):
        super().__init__(position, **kwargs)

    # def __repr__(self):
    #     if self is None:
    #         return 'Label is None!'
    #     params = [ self.text, self.position, self.rotation,
    #                self.magnification, self.reflection,
    #                self.layer, self.texttype ]
    #     return ("[SPiRA: Label] (\"{0}\", at ({1[0]}, {1[1]}), " +
    #             "rot: {2}, mag: {3}, ref: {4}, layer: {5}, " +
    #             "texttype: {6})").format(*params)







