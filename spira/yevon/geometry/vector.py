import numpy as np

from spira.core.parameters.initializer import ParameterInitializer
from spira.core.transformable import Transformable
from spira.core.parameters.variables import NumberParameter
from spira.core.parameters.descriptor import ParameterDescriptor
from spira.yevon.geometry.coord import Coord, CoordParameter
from spira.core.transforms import *
from spira.core.parameters.descriptor import FunctionParameter
from spira.yevon import constants


__all__ = [
    'Vector',
    'VectorParameter',
    'transformation_from_vector',
    'vector_from_two_points',
    'vector_match_transform',
    'vector_match_axis',
    'vector_match_transform_identical'
]


class Vector(Transformable, ParameterInitializer):
    """ Vector consisting of a point and an orientation. """

    midpoint = CoordParameter(default=(0.0, 0.0), doc='Position of the point.')

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

    angle_rad = FunctionParameter(get_angle_rad, set_angle_rad, doc="The orientation of the port in radians (stored in degrees by default")

    def get_angle_deg(self):
        if hasattr(self, '__angle__'):
            return self.__angle__
        else:
            return 0.0

    def set_angle_deg(self, value):
        self.__angle__ = value % 360.0

    orientation = FunctionParameter(get_angle_deg, set_angle_deg, doc = "The orientation of the port.")

    def __getitem__(self, key):
        if key == 0:
            return self.midpoint[0]
        if key == 1:
            return self.midpoint[1]
        else:
            raise IndexError("Vector supports only subscription[0] and [1], not " + str(key))

    def __eq__(self, other):
        if not isinstance(other, Vector):
            return False
        return self.midpoint == other.midpoint and (self.orientation == other.orientation)

    def __ne__(self, other):
        return self.midpoint != other.midpoint or (self.orientation != other.orientation)

    def __repr__(self):
        return "<Vector (%f, %f), a=%f>" % (self.x, self.y, self.orientation)

    def cos(self):
        return cos(constants.DEG2RAD * self.__angle__)

    def sin(self):
        return sin(constants.DEG2RAD * self.__angle__)

    def tan(self):
        return tan(constants.DEG2RAD * self.__angle__)

    def flip(self):
        return Vector(midpoint=self.midpoint, orientation=(self.__angle__ + 180.0) % 360.0)

    def transform(self, transformation):
        self.midpoint = transformation.apply_to_coord(self.midpoint)
        self.orientation = transformation.apply_to_angle(self.orientation)
        return self


def transformation_from_vector(vector):
    """ Make a transformation (rotation + translation) from a vector """
    return Rotation(vector.orientation) + Translation(vector.midpoint)


def vector_from_two_points(point1, point2):
    """ Make a vector out of two points """
    from spira.yevon.utils.geometry import orientation
    return Vector(midpoint=point1, orientation=orientation(point2, point1))


def vector_match_transform(v1, v2):
    """ Returns transformation to realign vectort 1 to match midpoint and opposite orientation of vector 2 """
    angle = 180.0 + v2.orientation - v1.orientation
    T = Translation(v2.midpoint - v1.midpoint)
    R = Rotation(rotation=angle, rotation_center=v2.midpoint)
    return T + R


def vector_match_axis(v1, v2, axis='x'):
    """ Returns transformation to realign vectort 1 to match midpoint and opposite orientation of vector 2 """
    angle = 180.0 + v2.orientation - v1.orientation
    if axis == 'x':
        dx = v2.midpoint[0] - v1.midpoint[0]
        T = Translation((dx, 0))
    elif axis == 'y':
        dy = v2.midpoint[1] - v1.midpoint[1]
        T = Translation((0, dy))
    else:
        raise ValueError('`axis` can only be `x` or `y`.')
    R = Rotation(rotation=angle, rotation_center=v1.midpoint)
    return T + R


def vector_match_transform_identical(v1, v2):
    """ Returns transformation to realign vectort 1 to match midpoint and orientation with vector 2 """
    angle = v2.orientation - v1.orientation
    T = Translation(v2.midpoint - v1.midpoint) 
    R = Rotation(rotation=angle, rotation_center=v2.midpoint)
    return T + R


def VectorParameter(internal_member_name=None, restriction=None, preprocess=None, **kwargs):
    R = RestrictType(Vector) & restriction
    return RestrictedProperty(internal_member_name, restriction=R, **kwargs)



