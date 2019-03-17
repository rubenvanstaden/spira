import numpy as np
from spira import param
from spira.core.initializer import FieldInitializer


class __Point__(FieldInitializer):

    def __init__(self, *args):
        if len(args) == 2:
            self.x, self.y = args
        elif len(args) == 1:
            self.x, self.y = args[0][0], args[0][1]

    def __getitem__(self, index):
        if index == 0: return self.x
        if index == 1: return self.y
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

    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

    def __eq__(self, other):
        return (other != None) and (abs(self[0] - other[0]) < 10e-10) and (abs(self[1] - other[1]) < 10e-10)

    def __ne__(self, other):
        return (other == None) or (abs(self[0] - other[0]) > 10e-10) or (abs(self[1] - other[1]) > 10e-10)

    def __iadd__(self, other):
        self.x += other[0]
        self.y += other[1]
        return self

    def __add__(self, other):
        return Point(self.x + other[0], self.y + other[1])

    def __isub__(self, other):
        self.x -= other[0]
        self.y -= other[1]
        return self

    def __sub__(self, other):
        return Point(self.x - other[0], self.y - other[1])

    def __neg__(self):
        return Point(-self.x, -self.y)

    def __imul__(self, other):
        self.x *= other
        self.y *= other
        return self

    def __mul__(self, other):
        return Point(self.x * other, self.y * other)

    def __rmul__(self, other):
        return Point(self.x * other, self.y * other)

    def __repr__(self):
        return "C2(%f, %f)" % (self.x, self.y)

    def dot(self, other):
        return np.conj(self.x) * other[0] + np.conj(self.y) * other[1]

    def __abs__(self):
        return np.math.sqrt(abs(self.x) ** 2 + abs(self.y) ** 2)


class Point(__Point__):
    """ 

    """

    __scaled__ = False

    def __init__(self, *args):
        super().__init__(*args)

    def transform(self, transformation):
        """
        apply a transformation to the coordinate
        """
        C = transformation.apply_to_coord(self)
        self.x = C.x
        self.y = C.y
        return self

    def transform_copy(self, transformation):
        """ return a transformed copy of the coordinate """
        return transformation.apply_to_coord(Point(self.x, self.y))

    def move(self, position):
        self.x += position[0]
        self.y += position[1]
        return self

    def move_copy(self, position):
        """ return a moved copy of the coordinate """
        return Point(self.x + position[0], self.y + position[1])

    def snap_to_grid(self, grids_per_unit = None):
        pass

    def distance(self, other):
        """  the distance to another coordinate """
        return np.sqrt((other[0] - self.x) ** 2 + (other[1] - self.y) ** 2)

    def angle_deg(self, other=(0.0, 0.0)):
        """ the angle with respect to another coordinate, in degrees """
        return 180.0 / np.pi * self.angle_rad(other)

    def angle_rad(self, other=(0.0, 0.0)):
        """ the angle with respect to another coordinate, in radians """
        return np.math.atan2(self.y - other[1], self.x - other[0])

    def id_string(self):
        return "%d_%d" % (self.x * 1000, self.y * 1000)

    def convert_to_array(self):
        return [self.x, self.y]









