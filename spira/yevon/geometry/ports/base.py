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
from spira.yevon.rdd.layer import PhysicalLayerField


RDD = get_rule_deck()


class __Port__(__Elemental__):

    name = StringField()

    midpoint = CoordField()
    orientation = NumberField(default=0)

    parent = DataField()
    locked = BoolField(default=True)
    pid = StringField()

    def __add__(self, other):
        if other is None:
            return self
        p1 = np.array(self.midpoint) + np.array(other)
        return p1

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
        if transformation is not None:
            self.midpoint = transformation.apply_to_coord(self.midpoint)
            self.orientation = transformation.apply_to_angle(self.orientation)
        return self

    # def transform(self, transformation):
    #     if transformation is not None:
    #         transformation.apply_to_object(self)
    #     return self
        
    # def transform_copy(self, transformation):
    #     T = deepcopy(self)
    #     T.transform(transformation)
    #     return T

    # def __reflect__(self):
    #     """ Reflect around the x-axis. """
    #     self.midpoint = [self.midpoint[0], -self.midpoint[1]]
    #     self.orientation = -self.orientation
    #     self.orientation = np.mod(self.orientation, 360)
    #     # self.reflection = True
    #     return self

    # def __rotate__(self, angle=45, center=(0,0)):
    #     """ Rotate port around the center with angle. """
    #     self.orientation += angle
    #     self.orientation = np.mod(self.orientation, 360)
    #     self.midpoint = utils.rotate_algorithm(self.midpoint, angle=angle, center=center)
    #     return self

    def __translate__(self, dx, dy):
        """ Translate port by dx and dy. """
        self.midpoint = self.midpoint + np.array([dx, dy])
        return self

    def move(self, midpoint=(0,0), destination=None, axis=None):
        d, o = utils.move_algorithm(obj=self, midpoint=midpoint, destination=destination, axis=axis)
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
    def key(self):
        return (self.name, self.gds_layer.number, self.midpoint[0], self.midpoint[1])


class __PhysicalPort__(__Port__):

    color = ColorField(default=color.COLOR_GRAY)

    gds_layer = LayerField(name='PortLayer', number=64)
    ps_layer = PhysicalLayerField()
    text_type = NumberField(default=RDD.GDSII.TEXT)

    # label = DataField(fdef_name='create_label')

    # # def create_label(self):
    # @property
    # def label(self):
    #     lbl = spira.Label(
    #         position=self.midpoint,
    #         text=self.name,
    #         gds_layer=self.gds_layer,
    #         texttype=self.text_type,
    #         orientation=self.orientation,
    #         color=color.COLOR_GHOSTWHITE
    #     )
    #     # lbl.__rotate__(angle=self.orientation)
    #     # lbl.move(midpoint=lbl.position, destination=self.midpoint)
    #     return lbl


class __VerticalPort__(__PhysicalPort__):
    __committed__ = {}


class __HorizontalPort__(__PhysicalPort__):
    __committed__ = {}


def PortField(midpoint=[0, 0], **kwargs):
    R = RestrictType(__Port__)
    return DataFieldDescriptor(restrictions=R, **kwargs)
