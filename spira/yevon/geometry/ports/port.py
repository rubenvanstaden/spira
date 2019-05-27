import gdspy
import pyclipper
import numpy as np
import spira.all as spira

from copy import copy, deepcopy
from numpy.linalg import norm
from spira.yevon import utils
from spira.yevon.gdsii.base import __Elemental__
from spira.core.parameters.variables import *
from spira.yevon.rdd.gdsii_layer import LayerField
from spira.core.parameters.descriptor import DataField
from spira.yevon.geometry.coord import CoordField
from spira.core.parameters.descriptor import DataField, FunctionField
from spira.yevon.geometry.ports.base import __PhysicalPort__
from spira.yevon.gdsii.group import Group
from spira.yevon.geometry.coord import Coord
from spira.yevon.geometry.vector import Vector
from spira.yevon.rdd import get_rule_deck


RDD = get_rule_deck()


__all__ = ['Port', 'PortField']


class Port(Vector, __PhysicalPort__):
    """  """

    bbox = BoolField(default=False)
    width = NumberField(default=2*1e6)
    # length = NumberField(default=2*1e6)

    # def get_length(self):
    #     if not hasattr(self, '__length__'):
    #         # key = self.layer.name
    #         if key in RDD.keys:
    #             if RDD.name == 'MiTLL':
    #                 self.__length__ = RDD[key].MIN_SIZE * 1e6
    #             elif RDD.name == 'AiST':
    #                 self.__length__ = RDD[key].WIDTH * 1e6
    #         else:
    #             self.__length__ = RDD.GDSII.TERM_WIDTH
    #     return self.__length__
    
    def get_length(self):
        if not hasattr(self, '__length__'):
            self.__length__ = 1*1e6
        return self.__length__

    def set_length(self, value):
        self.__length__ = value

    length = FunctionField(get_length, set_length, doc='Set the width of the terminal edge.')

    def get_alias(self):
        if not hasattr(self, '__alias__'):
            self.__alias__ = self.name
        return self.__alias__

    def set_alias(self, value):
        self.__alias__ = value

    alias = FunctionField(get_alias, set_alias, doc='Functions to generate an alias for cell name.')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return ("[SPiRA: Port] (name {}, alias {}, locked {}, midpoint {} orientation {} width {})").format(self.name, self.alias, self.locked, self.midpoint, self.orientation, self.width)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if isinstance(other, str):
            return (self.name == other)
        else:
            if not isinstance(self.midpoint, Coord):
                self.midpoint = Coord(self.midpoint[0], self.midpoint[1])
            if not isinstance(other.midpoint, Coord):
                other.midpoint = Coord(other.midpoint[0], other.midpoint[1])
            return ((self.name == other.name) and (self.midpoint == other.midpoint) and (self.orientation == other.orientation))

    def __ne__(self, other):
        return (self.midpoint != other.midpoint or (self.orientation != other.orientation)) 

    def id_string(self):
        return self.__repr__()

    def transform(self, transformation):
        self.midpoint = transformation.apply_to_coord(deepcopy(self.midpoint))
        self.orientation = transformation.apply_to_angle(deepcopy(self.orientation))
        return self

    def transform_copy(self, transformation):
        port = Port(
            name=self.name,
            # alias = self.name + transformation.id_string(),
            # midpoint=transformation.apply_to_coord(deepcopy(self.midpoint)),
            # orientation=transformation.apply_to_angle(deepcopy(self.orientation)),
            midpoint=transformation.apply_to_coord(self.midpoint),
            orientation=transformation.apply_to_angle(self.orientation),
            locked=deepcopy(self.locked),
            width=self.width,
            length=self.length,
            local_pid=self.local_pid
        )
        return port

    def encloses_endpoints(self, points):
        if pyclipper.PointInPolygon(self.endpoints[0], points) != 0: return True
        elif pyclipper.PointInPolygon(self.endpoints[1], points) != 0: return True

    @property
    def endpoints(self):
        dx = self.length/2*np.cos((self.orientation - 90)*np.pi/180)
        dy = self.length/2*np.sin((self.orientation - 90)*np.pi/180)
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


def PortField(local_name=None, restriction=None, **kwargs):
    R = RestrictType(Port) & restriction
    return RestrictedParameter(local_name, restrictions=R, **kwargs)




