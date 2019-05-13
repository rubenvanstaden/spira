import numpy as np

from spira.core.transformation import ReversibleTransform
from spira.core.descriptor import SetFunctionField
from spira.yevon.geometry.coord import CoordField, Coord


__all__ = ['Stretch', 'scale_elemental']


class Stretch(ReversibleTransform):
    """ Stretch an object using.

    Example
    -------
    >>> s = Stretch()(shape)
    """

    stretch_center = CoordField(default = (0.0, 0.0))

    def set_stretch_factor(self, value):
        if isinstance(value, Coord):
            self.__stretch_factor__ = value
        else:
            self.__stretch_factor__ = Coord(value[0], value[1])
        if self.__stretch_factor__[0] == 0.0 or self.__stretch_factor__[1] == 0.0:
            raise ValueError("Error: Stretch factor cannot be zero in Stretch transform")

    stretch_factor = SetFunctionField('__stretch_factor__', set_stretch_factor, required = True)

    def __repr__(self):
        return "[SPiRA: Stretch] (factor {}, center {})".format(self.stretch_factor, self.stretch_center)

    def __str__(self):
        return self.__repr__()

    def apply_to_coord(self, coord):
        x1 = self.__stretch_factor__[0] * coord[0]
        x2 = (1 - self.__stretch_factor__[0]) * self.stretch_center[0]
        y1 = self.__stretch_factor__[1] * coord[1]
        y2 = (1 - self.__stretch_factor__[1]) * self.stretch_center[1]
        return Coord(x1+x2, y1+y)

    def reverse_on_coord(self, coord):
        x1 = 1.0 / self.__stretch_factor__[0] * coord[0]
        x2 = (1 - 1.0 / self.__stretch_factor__[0]) * self.stretch_center[0]
        y1 = 1.0 / self.__stretch_factor__[1] * coord[1]
        y2 = (1 - 1.0 / self.__stretch_factor__[1]) * self.stretch_center[1]
        return Coord(x1+x2, y1+y2)

    def apply_to_array(self, coords):
        coords *= np.array([self.stretch_factor.x, self.stretch_factor.y])
        x = (1 - self.__stretch_factor__.x) * self.stretch_center.x
        y = (1 - self.__stretch_factor__.y) * self.stretch_center.y
        coords += np.array([x, y])
        return coords

    def reverse_on_array(self, coords):
        coords *= np.array([1.0 / self.stretch_factor.x, 1.0 / self.stretch_factor.y])
        x = (1 - 1.0 / self.__stretch_factor__.x) * self.stretch_center.x
        y = (1 - 1.0 / self.__stretch_factor__.y) * self.stretch_center.y
        coords += np.array([x, y])
        return coords

    def is_identity(self):
        """ Returns True if the transformation does nothing """
        return ((self.stretch_factor.x == 1.0) and (self.stretch_factor.y == 1.0))

    def id_string(self):
        return self.__repr__()


def scale_elemental(elem, scaling=(1.0, 1.0), scale_center=(0.0, 0.0)):
    from spira.core.transforms.magnification import Magnification
    if scaling[0] == scaling[1]:
        return Magnification(scale_center, scaling[0])(elem)
    else:
        return Stretch(stretch_factor=scaling, stretch_center=scale_center)(elem)


