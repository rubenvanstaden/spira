import spira.all as spira
import gdspy
import pyclipper
import numpy as np
from copy import copy, deepcopy
from spira.core import param
from spira.yevon.visualization import color
from spira.yevon.gdsii.base import __Elemental__
from spira.yevon.layer import LayerField
from spira.core.param.variables import *
from spira.yevon.visualization.color import ColorField


__all__ = ['Label']


class __Label__(gdspy.Label, __Elemental__):

    __committed__ = {}

    def __eq__(self, other):
        return self.id == other.id

    def __deepcopy__(self, memo):
        c_label = self.modified_copy(
            position=deepcopy(self.position),
            gds_layer=deepcopy(self.gds_layer)
        )
        return c_label


class LabelAbstract(__Label__):

    gds_layer = LayerField()
    text = StringField(default='no_text')
    rotation = NumberField(default=0)
    reflection = BoolField(default=False)
    magnification = NumberField(default=1.0)
    texttype = IntegerField(default=0)

    def __init__(self, position, **kwargs):
        super().__init__(position, **kwargs)

    def commit_to_gdspy(self, cell=None, transformation=None):
        if self.__repr__() not in list(LabelAbstract.__committed__.keys()):
            L = gdspy.Label(self.text,
                deepcopy(self.position),
                anchor='o',
                rotation=self.rotation,
                magnification=self.magnification,
                x_reflection=self.reflection,
                layer=self.gds_layer.number,
                texttype=self.texttype
            )
            LabelAbstract.__committed__.update({self.__repr__():L})
        else:
            L = LabelAbstract.__committed__[self.__repr__()]
        if cell is not None:
            cell.add(L)
        return L

    def reflect(self, p1=(0,1), p2=(0,0), angle=None):
        self.position = [self.position[0], -self.position[1]]
        self.rotation = self.rotation * (-1)
        self.rotation = np.mod(self.rotation, 360)
        return self

    def rotate(self, angle=45, center=(0,0)):
        self.position = self.__rotate__(self.position, angle=angle, center=[0, 0])
        self.rotation += angle
        self.rotation = np.mod(self.rotation, 360)
        return self

    def encloses(self, ply):
        if isinstance(ply, spira.Polygon):
            return pyclipper.PointInPolygon(self.position, ply.shape.points) != 0
        elif isinstance(ply, (list, set, np.ndarray)):
            return pyclipper.PointInPolygon(self.position, ply) != 0
        else:
            raise ValueError('Not Implemented!')

    def flat_copy(self, level=-1, commit_to_gdspy=False):
        c_label = self.modified_copy(position=self.position)
        if commit_to_gdspy:
            self.gdspy_commit = True
        return c_label

    def move(self, midpoint=(0,0), destination=None, axis=None):
        d, o = super().move(midpoint=midpoint, destination=destination, axis=axis)
        dx, dy = np.array(d) - o
        super().translate(dx, dy)
        return self


class Label(LabelAbstract):
    """

    """

    route = StringField(default='no_route')
    color = ColorField(default=color.COLOR_BLUE)

    def __init__(self, position, **kwargs):

        # TODO: Convert to Point object.
        if isinstance(position, (list, tuple, set, np.ndarray)):
            self.position = list(position)
        else:
            raise ValueError('Position type not supported!')

        __Elemental__.__init__(self, **kwargs)
        gdspy.Label.__init__(self,
            text=self.text,
            position=self.position,
            anchor=str('o'),
            rotation=self.rotation,
            magnification=self.magnification,
            x_reflection=self.reflection,
            layer=self.gds_layer.number,
            texttype=self.texttype
        )
        
    def __repr__(self):
        if self is None:
            return 'Label is None!'
        params = [ self.text, self.position, self.rotation,
                   self.magnification, self.reflection,
                   self.layer, self.texttype ]
        return ("[SPiRA: Label] (\"{0}\", at ({1[0]}, {1[1]}), " +
                "rot: {2}, mag: {3}, ref: {4}, layer: {5}, " +
                "texttype: {6})").format(*params)







