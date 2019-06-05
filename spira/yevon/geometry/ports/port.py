import gdspy
import pyclipper
import numpy as np
import spira.all as spira

from copy import copy, deepcopy
from numpy.linalg import norm
from spira.core.parameters.variables import *
from spira.yevon.geometry.coord import CoordField
from spira.core.parameters.descriptor import FunctionField
from spira.yevon.geometry.ports.base import __PhysicalPort__
from spira.yevon.geometry.coord import Coord
from spira.yevon.geometry.vector import *
from spira.yevon.geometry.line import *
from spira.yevon.process import get_rule_deck


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
            self.__length__ = 0.5*1e6
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

        if 'locked' in kwargs:
            if kwargs['locked'] is True:
                self.purpose = RDD.PURPOSE.PORT.EDGE_DISABLED

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

    @property
    def unlock(self):
        self.purpose = RDD.PURPOSE.PORT.EDGE_ENABLED
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

    def connect(self, port, destination):
        T = vector_match_transform(v1=port, v2=destination)
        self.transform(T)
        return self
    
    def align(self, port, destination, distance):
        destination = deepcopy(destination)
        self = self.connect(port, destination)
    
        L = line_from_point_angle(point=destination.midpoint, angle=destination.orientation)
        dx, dy = L.get_coord_from_distance(destination, distance)
    
        T = spira.Translation(translation=(dx, dy))
        self.transform(T)
        return self


def PortField(local_name=None, restriction=None, **kwargs):
    R = RestrictType(Port) & restriction
    return RestrictedParameter(local_name, restrictions=R, **kwargs)


def point_in_port_polygon(port, point):
    pass


# def point_in_port_polygon(port, point):
#     from spira.yevon.process.physical_layer import PhysicalLayer
#     dw = port.width
#     dl = port.length
#     layer = PhysicalLayer(process=port.process, purpose=port.purpose)
#     p = spira.Box(width=dw, height=dl, layer=layer)
#     p.center = (0,0)
#     angle = port.orientation - 90
#     T = spira.Rotation(rotation=angle)
#     T += spira.Translation(port.midpoint)
#     p.transform(T)

#     print(p)
#     print(p.points)

#     pp = pyclipper.PointInPolygon(point, p.points) != 0

#     print(pp)

#     return pp

#     # if pp == 0:
#     #     return False
#     # else:
#     #     return True


