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
from spira.yevon.gdsii.generators import PortGenerator
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = ['Port', 'PortParameter']


class Port(Vector, __Port__):
    """  """

    name = StringParameter()
    width = NumberParameter(default=2)
    length = NumberParameter(default=0.5)
    # template = TemplateParameter(default=RDD.TEMPLATES.PORT)

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)

    def __repr__(self):
        class_string = "[SPiRA: Port] (name {}, midpoint {} orientation {} width {}, process {}, purpose {})"
        return class_string.format(self.name, self.midpoint, self.orientation, self.width, self.process.symbol, self.purpose.name)

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

    def net_source(self):
        return 'source: {}'.format(self.name)

    def net_target(self):
        return 'target: {}'.format(self.name)

    def is_valid_path(self):
        return True

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

    # def encloses_endpoints(self, points):
    #     if pyclipper.PointInPolygon(self.endpoints[0], points) != 0: return True
    #     elif pyclipper.PointInPolygon(self.endpoints[1], points) != 0: return True

    # def get_corner1(self):
    #     port_position = self.midpoint
    #     port_angle = (self.orientation-90) * constants.DEG2RAD
    #     wg_width = self.width
    #     port_corner1_x = port_position[0] + (wg_width / 2.0) * np.cos(port_angle-np.pi/2.0)
    #     port_corner1_y = port_position[1] + (wg_width / 2.0) * np.sin(port_angle-np.pi/2.0)
    #     return Coord(port_corner1_x, port_corner1_y)

    # def get_corner2(self):
    #     port_position = self.midpoint
    #     port_angle = (self.orientation-90) * constants.DEG2RAD
    #     wg_width = self.width
    #     port_corner2_x = port_position[0] + (wg_width / 2.0) * np.cos(port_angle+np.pi/2.0)
    #     port_corner2_y = port_position[1] + (wg_width / 2.0) * np.sin(port_angle+np.pi/2.0)
    #     return Coord(port_corner2_x, port_corner2_y)

    # @property
    # def endpoints(self):

    #     angle = (self.orientation - 90) * constants.DEG2RAD
    #     dx = self.length/2 * np.cos(angle)
    #     dy = self.length/2 * np.sin(angle)

    #     left_point = self.midpoint - np.array([dx,dy])
    #     right_point = self.midpoint + np.array([dx,dy])

    #     left_point = left_point.to_numpy_array()
    #     right_point = right_point.to_numpy_array()

    #     return np.array([left_point, right_point])

    # @endpoints.setter
    # def endpoints(self, points):
    #     p1, p2 = np.array(points[0]), np.array(points[1])
    #     self.midpoint = (p1+p2)/2
    #     dx, dy = p2-p1
    #     self.orientation = np.arctan2(dx,dy)*180/np.pi
    #     self.width = np.sqrt(dx**2 + dy**2)

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


