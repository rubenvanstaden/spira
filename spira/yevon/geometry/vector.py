import numpy as np

from spira.core.initializer import FieldInitializer
from spira.core.transformable import Transformable
from spira.core.param.variables import NumberField
from spira.core.descriptor import DataFieldDescriptor
from spira.yevon.geometry.coord import Coord
from spira.core.transforms import *
from spira.core.descriptor import FunctionField
from spira.yevon import constants


__all__ = [
    'Vector',
    'VectorField',
    'transformation_from_vector',
    'vector_from_two_points',
    'vector_match_transform',
    'vector_match_transform_identical'
]


class Vector(Transformable, FieldInitializer):
    """ Vector consisting of a point and an orientation. """

    midpoint = CoordField(default=(0.0, 0.0), doc='Position of the point.')

    @property
    def x(self):
        return self.midpoint.x

    @property
    def y(self):
        return self.midpoint.y

    def get_angle_rad(self):
        if hasattr(self, '__angle__'):
            return constants.DEG2RAD * self.__angle__
        else:
            return 0.0

    def set_angle_rad(self, value):
        self.__angle__ = (constants.RAD2DEG * value) % 360.0

    angle_rad = FunctionField(get_angle_rad, set_angle_rad, doc="The outward facing orientation of the port in radians (stored in degrees by default, converted to radians if needed)")

    def get_angle_deg(self):
        if hasattr(self, '__angle__'):
            return self.__angle__
        else:
            return 0.0

    def set_angle_deg(self, value):
        self.__angle__ = value % 360.0

    orientation = FunctionField(get_angle_deg, set_angle_deg, doc = "The outward facing orientation of the port.")

    def cos(self):
        return cos(constants.DEG2RAD * self.__angle__)

    def sin(self):
        return sin(constants.DEG2RAD * self.__angle__)

    def tan(self):
        return tan(constants.DEG2RAD * self.__angle__)

    def flip(self):
        return Vector(midpoint=self.midpoint, orientation=(self.__angle__ + 180.0) % 360.0)

    def __getitem__(self, key):
        # Behave like a coordinate.
        if key == 0:
            return self.midpoint[0]
        if key == 1:
            return self.midpoint[1]
        else:
            raise IndexError("Vector supports only subscription[0] and [1], not " + str(key))

    def __eq__(self, other):
        if not isinstance(other, Vector):
            return False
        return self.midpoint == other.midpoint and (self.angle_deg == other.angle_deg)
    
    def __ne__(self, other):
        return self.midpoint != other.midpoint or (self.angle_deg != other.angle_deg)

    def __repr__(self):
        return "<Vector (%f, %f), a=%f>" % (self.x, self.y, self.angle_deg)

    def transform(self, transformation):
        self.midpoint = transformation.apply_to_coord(self.midpoint)
        self.angle_deg = transformation.apply_to_angle(self.angle_deg)
        return self


def transformation_from_vector(vector):
    """ Make a transformation (rotation + translation) from a vector """
    return Rotation(vector.orientation) + Translation(vector.midpoint)


def vector_from_two_points(point1, point2):
    """ Make a vector out of two points """
    return Vector(midpoint=point1, orientation=shape_info.angle_deg(point2, point1))


def vector_match_transform(v1, v2):
    """ Returns transformation to realign vectort 1 to match midpoint and opposite orientation of vector 2 """
    angle = 180.0 + v2.orientation - v1.orientation
    # angle = vector2.orientation - vector1.orientation
    T = Translation(v2.midpoint - v1.midpoint)
    # R = Rotation(rotation=angle, center=v2.midpoint)
    R = Rotation(rotation=angle, center=v1.midpoint)
    return T + R


def vector_match_transform_identical(vector1, vector2):
    """ Returns transformation to realign vectort 1 to match midpoint and orientation with vector 2 """
    T = Translation(vector2.midpoint - vector1.midpoint) 
    R = Rotation(vector2.midpoint, vector2.angle_deg - vector1.angle_deg)  
    return T + R


def VectorField(internal_member_name=None, restriction=None, preprocess=None, **kwargs):
    R = RestrictType(Vector) & restriction
    return RestrictedProperty(internal_member_name, restriction=R, **kwargs)



