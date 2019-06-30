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
from spira.yevon.geometry.ports.base import __PhysicalPort__
from spira.yevon.geometry.coord import Coord
from spira.yevon.geometry.vector import *
from spira.yevon.geometry.line import *
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = ['Port', 'PortParameter', 'ContactPort', 'DummyPort']


class Port(Vector, __PhysicalPort__):
    """  """

    bbox = BoolParameter(default=False)
    width = NumberParameter(default=2)
    port_type = StringParameter(default='terminal')

    # length = NumberParameter(default=2)

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
            self.__length__ = 0.5
        return self.__length__

    def set_length(self, value):
        self.__length__ = value

    length = FunctionParameter(get_length, set_length, doc='Set the width of the terminal edge.')

    def get_alias(self):
        if not hasattr(self, '__alias__'):
            self.__alias__ = self.name
        return self.__alias__

    def set_alias(self, value):
        self.__alias__ = value

    alias = FunctionParameter(get_alias, set_alias, doc='Functions to generate an alias for cell name.')

    # def __init__(self, midpoint, orientation, **kwargs):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if 'port_type' in kwargs:
            if kwargs['port_type'] == 'contact':
                self.__class__ = ContactPort
            elif kwargs['port_type'] == 'branch':
                self.__class__ = BranchPort
            elif kwargs['port_type'] == 'route':
                self.__class__ = RoutePort
            elif kwargs['port_type'] == 'dummy':
                self.__class__ = DummyPort

        if 'locked' in kwargs:
            if kwargs['locked'] is True:
                self.purpose = RDD.PURPOSE.PORT.OUTSIDE_EDGE_DISABLED

    def __repr__(self):
        class_string = "[SPiRA: Port] (name {}, alias {}, locked {}, midpoint {} orientation {} width {})"
        return class_string.format(self.name, self.alias, self.locked, self.midpoint, self.orientation, self.width)

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

    def flip(self):
        """ Return the port rotated 180 degrees. """
        angle = (self.orientation + 180.0) % 360.0
        return self.__class__(midpoint=self.midpoint, orientation=angle)

    @property
    def unlock(self):
        self.purpose = RDD.PURPOSE.PORT.OUTSIDE_EDGE_ENABLED
        return self

    def transform(self, transformation):
        self.midpoint = transformation.apply_to_coord(self.midpoint)
        self.orientation = transformation.apply_to_angle(self.orientation)
        return self

    def transform_copy(self, transformation):
        port = Port(
            name=self.name,
            # alias = self.name + transformation.id_string(),
            midpoint=transformation.apply_to_coord(self.midpoint),
            orientation=transformation.apply_to_angle(self.orientation),
            process=self.process,
            purpose=self.purpose,
            width=self.width,
            length=self.length,
            local_pid=self.local_pid
        )
        return port

    def encloses_endpoints(self, points):
        if pyclipper.PointInPolygon(self.endpoints[0], points) != 0: return True
        elif pyclipper.PointInPolygon(self.endpoints[1], points) != 0: return True

    def get_corner1(self):
        port_position = self.midpoint
        port_angle = (self.orientation-90) * constants.DEG2RAD
        wg_width = self.width
        port_corner1_x = port_position[0] + (wg_width / 2.0) * np.cos(port_angle-np.pi/2.0)
        port_corner1_y = port_position[1] + (wg_width / 2.0) * np.sin(port_angle-np.pi/2.0)
        return Coord(port_corner1_x, port_corner1_y)

    def get_corner2(self):
        port_position = self.midpoint
        port_angle = (self.orientation-90) * constants.DEG2RAD
        wg_width = self.width
        port_corner2_x = port_position[0] + (wg_width / 2.0) * np.cos(port_angle+np.pi/2.0)
        port_corner2_y = port_position[1] + (wg_width / 2.0) * np.sin(port_angle+np.pi/2.0)
        return Coord(port_corner2_x, port_corner2_y)

    @property
    def endpoints(self):

        angle = (self.orientation - 90) * constants.DEG2RAD
        dx = self.length/2 * np.cos(angle)
        dy = self.length/2 * np.sin(angle)

        left_point = self.midpoint - np.array([dx,dy])
        right_point = self.midpoint + np.array([dx,dy])

        left_point = left_point.to_numpy_array()
        right_point = right_point.to_numpy_array()

        return np.array([left_point, right_point])

    @endpoints.setter
    def endpoints(self, points):
        p1, p2 = np.array(points[0]), np.array(points[1])
        self.midpoint = (p1+p2)/2
        dx, dy = p2-p1
        self.orientation = np.arctan2(dx,dy)*180/np.pi
        self.width = np.sqrt(dx**2 + dy**2)

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


from spira.yevon.process.purpose_layer import PurposeLayerParameter
class ContactPort(Port):

    width = NumberParameter(default=0.4)
    length = NumberParameter(default=0.4)
    purpose = PurposeLayerParameter(default=RDD.PURPOSE.PORT.CONTACT)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        class_string = "[SPiRA: ContactPort] (name {}, alias {}, locked {}, midpoint {} orientation {} width {})"
        return class_string.format(self.name, self.alias, self.locked, self.midpoint, self.orientation, self.width)

    def id_string(self):
        return self.__repr__()


class BranchPort(Port):

    width = NumberParameter(default=0.4)
    length = NumberParameter(default=0.4)
    purpose = PurposeLayerParameter(default=RDD.PURPOSE.PORT.BRANCH)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        class_string = "[SPiRA: BranchPort] (name {}, alias {}, locked {}, midpoint {} orientation {} width {})"
        return class_string.format(self.name, self.alias, self.locked, self.midpoint, self.orientation, self.width)


class RoutePort(Port):

    width = NumberParameter(default=0.4)
    length = NumberParameter(default=0.4)
    purpose = PurposeLayerParameter(default=RDD.PURPOSE.PORT.BRANCH)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        class_string = "[SPiRA: BranchPort] (name {}, alias {}, locked {}, midpoint {} orientation {} width {})"
        return class_string.format(self.name, self.alias, self.locked, self.midpoint, self.orientation, self.width)


class DummyPort(Port):

    width = NumberParameter(default=0.4)
    length = NumberParameter(default=0.4)
    purpose = PurposeLayerParameter(default=RDD.PURPOSE.DUMMY)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        class_string = "[SPiRA: DummyPort] (name {}, alias {}, locked {}, midpoint {} orientation {} width {})"
        return class_string.format(self.name, self.alias, self.locked, self.midpoint, self.orientation, self.width)


def PortParameter(local_name=None, restriction=None, **kwargs):
    R = RestrictType(Port) & restriction
    return RestrictedParameter(local_name, restrictions=R, **kwargs)



