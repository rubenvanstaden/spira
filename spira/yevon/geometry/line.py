import numpy as np

from spira.yevon import constants
from spira.core.parameters.initializer import ParameterInitializer
from spira.core.transformable import Transformable
from spira.core.parameters.variables import NumberParameter
from spira.core.parameters.descriptor import ParameterDescriptor
from spira.yevon.geometry.coord import Coord


__all__ = [
    'Line',
    'LineParameter',
    'line_from_point_angle',
    'line_from_slope_intercept',
    'line_from_two_points',
    'line_from_vector'
]


class Line(Transformable, ParameterInitializer):
    """ Creates a line ax + by + c = 0. """

    a = NumberParameter(default=1)
    b = NumberParameter(default=1)
    c = NumberParameter(default=1)

    def __init__(self, a, b, c, **kwargs):
        super().__init__(a=a, b=b, c=c, **kwargs)

    def __repr__(self):
        return "[SPiRA: Line] ({}x {}y + {})".format(self.a, self.b, self.c)

    def __str__(self):
        return self.__repr__()

    @property
    def slope(self):
        if self.b == 0: return None
        return -self.a / self.b

    @property
    def angle_rad(self):
        return np.arctan2(-self.a, self.b)

    @property
    def orientation(self):
        return constants.RAD2DEG * self.angle_rad

    @property
    def y_intercept(self):
        if self.b == 0.0: return None
        return -self.c / -self.b

    @property
    def x_intercept(self):
        if self.a == 0.0: return None
        return -self.c / -self.a

    def is_on_line(self, coordinate):
        return abs(self.a * coordinate[0] + self.b * coordinate[1] + self.c) < 1E-10

    def distance(self, coordinate):
        return abs(self.a*coordinate[0] + self.b*coordinate[1] + self.c) / np.sqrt(self.a**2 + self.b**2)

    def get_coord_from_distance(self, destination, distance):
        d = distance
        m = self.slope
        x0 = destination.midpoint[0]
        y0 = destination.midpoint[1]

        if m is None:
            dx, dy = 0, distance
        else:
            angle = self.orientation
            angle = np.mod(angle, 360)
            if 90 < angle <= 270:
                x = x0 + d / np.sqrt(1 + m**2)
            elif (0 < angle <= 90) or (270 < angle <= 360):
                x = x0 - d / np.sqrt(1 + m**2)
            else:
                raise ValueError('Angle {} not accepted.'.format(angle))
            y = m*(x - x0) + y0
            dx = x - x0
            dy = y - y0

        return (dx, dy)

    def intersection(self, line):
        """ gives intersection of line with other line """
        if (self.b * line.a - self.a * line.b) == 0.0: return None
        x = -(self.b * line.c - line.b * self.c) / (self.b * line.a - self.a * line.b)
        y =  (self.a * line.c - line.a * self.c) / (self.b * line.a - self.a * line.b)
        return Coord(x, y)

    def closest_point(self, point):
        """ Gives closest point on line """
        line2 = straight_line_from_point_angle(point, self.orientation + 90.0)
        return self.intersection(line2)

    def is_on_same_side(self, point1, point2):
        """ Returns True is both points are on the same side of the line """
        v1 = self.a * point1[0] + self.b * point1[1] + self.c
        v2 = self.a * point2[0] + self.b * point2[1] + self.c
        return np.sign(v1) == np.sign(v2)

    def is_parallel(self, other):
        """ Returns True is lines are parallel """
        return abs(self.a * other.b - self.b * other.a) < 1E-10

    def __eq__(self, other):
        v1 = abs(self.a * other.b - self.b * other.a)
        v2 = abs(self.c * other.b - self.b * other.c)
        v3 = abs(self.a * other.c - self.c * other.a)
        return (v1 < 1E-10) and (v2 < 1E-10) and (v3 < 1E-10)

    def __ne__(self, other):
        return (not self.__eq__(other))    

    def __get_2_points__(self):
        from spira.yevon.geometry import shapes
        if b == 0:
            return shapes.Shape([Coord(-self.c / self.a, 0.0), Coord(-self.c / self.a, 1.0)])
        elif a == 0: 
            return shapes.Shape([Coord(0.0, -self.c / self.b), Coord(1.0, -self.c / self.b)])
        else:
            return shapes.Shape([Coord(-self.c / self.a, 0.0), Coord(0.0, -self.c / self.b)])

    def transform(self, transformation):
        p = self.__get_2_points__().transform(transformation)
        self.a = y2 - y1
        self.b = x1 - x2
        self.c = (x2 - x1) * y1 - (y2 - y1) * x1

    def transform_copy(self, transformation):
        p = self.__get_2_points__().transform(transformation)
        return line_from_two_points(p[0], p[1])


def line_from_slope_intercept(slope, y_intercept):
    """ Creates a Line object from slope and y_intercept. """
    return Line(slope, -1.0, intercept)


def line_from_two_points(point1, point2):
    """ Creates a Line object from two points. """
    x1, y1 = point1[0], point1[1]
    x2, y2 = point2[0], point2[1]
    a, b = (y2 - y1), (x1 - x2)
    c = (x2 - x1) * y1 - (y2 - y1) * x1
    return Line(a=a, b=b, c=c)


def line_from_point_angle(point, angle):
    """ Creates a Line object from point and angle. """
    if abs(angle % 180.0 - 90.0) <= 1e-12:
        return line_from_two_points(point, Coord(0.0, 1) + point)
    slope = np.tan(constants.DEG2RAD * angle)
    return Line(slope, -1, point[1] - slope * point[0])


def line_from_vector(vector):
    """ Creates a Line object from a vector. """
    return line_from_point_angle(vector.position, vector.orientation)


def LineParameter(restriction=None, preprocess=None, **kwargs):
    if 'default' not in kwargs:
        kwargs['default'] = Line()
    R = RestrictType(Line) & restriction
    return ParameterDescriptor(restrictions=R, **kwargs)

