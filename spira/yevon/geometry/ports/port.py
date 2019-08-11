import gdspy
import pyclipper
import numpy as np
import spira.all as spira

from copy import copy, deepcopy
from numpy.linalg import norm
from spira.yevon import constants
from spira.core.parameters.variables import *
from spira.yevon.geometry.coord import CoordParameter
from spira.core.parameters.descriptor import FunctionParameter
from spira.yevon.geometry.ports.base import __Port__
from spira.yevon.geometry.coord import Coord
from spira.yevon.geometry.vector import *
from spira.yevon.geometry.line import *
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = ['Port', 'PortParameter']


class Port(Vector, __Port__):
    """  """

    width = NumberParameter(default=2)
    length = NumberParameter(default=0.5)

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)

    def __repr__(self):
        class_string = "[SPiRA: Port \'{}\'] (name {}, midpoint {} orientation {} width {}, process {}, purpose {})"
        return class_string.format(self.alias, self.name, self.midpoint, self.orientation, self.width,
                                self.process.symbol, self.purpose.name)

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
            return (
                (self.name == other.name) and
                (self.midpoint == other.midpoint) and
                (self.orientation == other.orientation)
            )

    def __ne__(self, other):
        return (self.midpoint != other.midpoint or (self.orientation != other.orientation)) 

    # def id_string(self):
    #     return self.__repr__()

    # FIXME: Why do it like this?
    def id_string(self):
        name = self.name.split('_')[0]
        return '{}_{}'.format(name, self.midpoint)

    def flip(self):
        """ Return the port rotated 180 degrees. """
        angle = (self.orientation + 180.0) % 360.0
        return self.__class__(name=self.name, midpoint=self.midpoint, orientation=angle)

    def transform(self, transformation):
        self.midpoint = transformation.apply_to_coord(self.midpoint)
        self.orientation = transformation.apply_to_angle(self.orientation)
        return self

    def transform_copy(self, transformation):
        # port = self.copy(
        #     midpoint=transformation.apply_to_coord(self.midpoint),
        #     orientation=transformation.apply_to_angle(self.orientation),
        # )
        
        # port = self.__class__(
        #     midpoint=transformation.apply_to_coord(self.midpoint),
        #     orientation=transformation.apply_to_angle(self.orientation),
        # )

        port = Port(
            name=self.name,
            midpoint=transformation.apply_to_coord(self.midpoint),
            orientation=transformation.apply_to_angle(self.orientation),
            process=self.process,
            purpose=self.purpose,
            width=self.width,
            length=self.length,
            local_pid=self.local_pid
        )

        return port

    def net_source(self):
        return 'source: {}'.format(self.name)

    def net_target(self):
        return 'target: {}'.format(self.name)

    def is_valid_path(self):
        return True

    def connect(self, port, destination):
        T = vector_match_transform(v1=port, v2=destination)
        self.transform(T)
        return self

    def distance_alignment(self, port, destination, distance):
        destination = deepcopy(destination)
        self = self.connect(port, destination)
    
        L = line_from_point_angle(point=destination.midpoint, angle=destination.orientation)
        dx, dy = L.get_coord_from_distance(destination, distance)
    
        T = spira.Translation(translation=(dx, dy))
        self.transform(T)
        return self

    @property
    def key(self):
        return (self.name, self.layer, self.midpoint[0], self.midpoint[1])


def PortParameter(local_name=None, restriction=None, **kwargs):
    R = RestrictType(Port) & restriction
    return RestrictedParameter(local_name, restrictions=R, **kwargs)


