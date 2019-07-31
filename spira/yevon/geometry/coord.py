import math
import numpy as np
from spira.core.parameters.restrictions import RestrictType
from spira.core.parameters.descriptor import RestrictedParameter
from spira.core.transformable import Transformable
from spira.core.parameters.processors import ProcessorTypeCast


class Coord(Transformable):
    """ Special SPiRA coordinate that can be transformed and moved.

    Example
    -------
    >>> c = Coord(0,0)
    >>> [SPiRA: Coord] ()
    """

    def __init__(self, *args):
        if len(args) == 2:
            self.x, self.y = args
        elif len(args) == 1:
            self.x, self.y = args[0][0], args[0][1]

    def __repr__(self):
        return 'Coord({}, {})'.format(self.x, self.y)

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def __getitem__(self, index):
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        raise IndexError("Coord type only supports index 0 and 1")

    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError("Coord type only supports index 0 and 1")
        return

    def __iter__(self):
        for index in range(2):
            yield self[index]

    def __eq__(self, other):
        return (other != None) and (abs(self[0] - other[0]) < 10e-10) and (abs(self[1] - other[1]) < 10e-10)

    def __ne__(self, other):
        return (other == None) or (abs(self[0] - other[0]) > 10e-10) or (abs(self[1] - other[1]) > 10e-10)

    def __iadd__(self, other):
        self.x += other[0]
        self.y += other[1]
        return self

    def __add__(self, other):
        return Coord(self.x + other[0], self.y + other[1])

    def __isub__(self, other):
        self.x -= other[0]
        self.y -= other[1]
        return self

    def __sub__(self, other):
        return Coord(self.x - other[0], self.y - other[1])

    def __neg__(self):
        return Coord(-self.x, -self.y)    

    def __imul__(self, other):
        self.x *= other
        self.y *= other
        return self

    def __mul__(self, other):
        return Coord(self.x * other, self.y * other)

    def __rmul__(self, other):
        return Coord(self.x * other, self.y * other)

    def __abs__(self):
        return math.sqrt(abs(self.x) ** 2 + abs(self.y) ** 2)

    def snap_to_grid(self, grids_per_unit=None):
        """ Snap the coordinate to the given or current grid. """
        from spira import settings
        if grids_per_unit is None:
            grids_per_unit = settings.get_grids_per_unit()
        self.x = math.floor(self.x * grids_per_unit + 0.5) / grids_per_unit
        self.y = math.floor(self.y * grids_per_unit + 0.5) / grids_per_unit
        return self

    def transform(self, transformation):
        C = transformation.apply_to_coord(self)
        self.x = C.x
        self.y = C.y
        return self

    def transform_copy(self, transformation):
        return transformation.apply_to_coord(Coord(self.x, self.y))

    def move(self, position):
        """ Move the coordinate by a displacement vector. """
        self.x += position[0]
        self.y += position[1]
        return self

    def move_copy(self, position):
        """ Return a moved copy of the coordinate """
        return Coord(self.x + position[0], self.y + position[1])

    def distance(self, other):
        """ The distance to another coordinate """
        return math.sqrt((other[0] - self.x)**2 + (other[1] - self.y)**2)

    def orientation(self, other=(0.0, 0.0)):
        """ the angle with respect to another coordinate, in degrees """
        return 180.0 / math.pi * self.angle_rad(other)

    def angle_rad(self, other=(0.0, 0.0)):
        """ the angle with respect to another coordinate, in radians """
        return math.atan2(self.y - other[1], self.x - other[0])

    def dot(self, other):
        return np.conj(self.x) * other[0] + np.conj(self.y) * other[1]

    def id_string(self):
        return "%d_%d" % (self.x * 1000, self.y * 1000)

    def to_numpy_array(self):
        return np.array([self.x, self.y])

    def to_list(self):
        return [self.x, self.y]


RESTRICT_COORD = RestrictType(Coord)


def CoordParameter(local_name=None, restriction=None, preprocess=None, **kwargs):
    if 'default' not in kwargs:
        kwargs['default'] = Coord(0,0)
    R = RESTRICT_COORD & restriction
    P = ProcessorTypeCast(Coord) + preprocess
    return RestrictedParameter(local_name, restriction=R, preprocess=P, **kwargs)


