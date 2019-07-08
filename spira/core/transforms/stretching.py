import numpy as np

from spira.core.transformation import ReversibleTransform
from spira.core.parameters.descriptor import SetFunctionParameter
from spira.yevon.geometry.coord import CoordParameter, Coord


__all__ = ['Stretch', 'scale_element', 'stretch_element_by_port']


class Stretch(ReversibleTransform):
    """ Stretch an object using.

    Example
    -------
    >>> s = Stretch()(shape)
    """

    stretch_center = CoordParameter(default=(0,0))

    def set_stretch_factor(self, value):
        if isinstance(value, Coord):
            self.__stretch_factor__ = value
        else:
            self.__stretch_factor__ = Coord(value[0], value[1])
        if self.__stretch_factor__[0] == 0.0 or self.__stretch_factor__[1] == 0.0:
            raise ValueError("Error: Stretch factor cannot be zero in Stretch transform")

    stretch_factor = SetFunctionParameter('__stretch_factor__', set_stretch_factor)

    def __repr__(self):
        return "[SPiRA: Stretch] (factor {}, center {})".format(self.stretch_factor, self.stretch_center)

    def __str__(self):
        return self.__repr__()

    def apply_to_coord(self, coord):
        x1 = self.__stretch_factor__[0] * coord[0]
        x2 = (1 - self.__stretch_factor__[0]) * self.stretch_center[0]
        y1 = self.__stretch_factor__[1] * coord[1]
        y2 = (1 - self.__stretch_factor__[1]) * self.stretch_center[1]
        return Coord(x1+x2, y1+y2)

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

    def apply_to_angle(self, angle):
        # FIXME: This is required for transforming polygon ports.
        # This is currently just a temporary fix.
        return angle

    def is_identity(self):
        """ Returns True if the transformation does nothing """
        return ((self.stretch_factor.x == 1.0) and (self.stretch_factor.y == 1.0))

    def id_string(self):
        return self.__repr__()


def scale_element(elem, scaling=(1.0, 1.0), scale_center=(0.0, 0.0)):
    from spira.core.transforms.magnification import Magnification
    if scaling[0] == scaling[1]:
        return Magnification(scale_center, scaling[0])(elem)
    else:
        return Stretch(stretch_factor=scaling, stretch_center=scale_center)(elem)


def stretch_element_by_port(elem, const_port, subj_port, destination):
    """  """
    p1, p2 = const_port, subj_port
    d0 = p1.midpoint.distance(p2.midpoint)
    d1 = p1.midpoint.distance(destination)
    sf = d1/d0
    if p2.orientation == 0:
        T = Stretch(stretch_factor=(sf,1), stretch_center=p1.midpoint)
    elif p2.orientation == 90:
        T = Stretch(stretch_factor=(1,sf), stretch_center=p1.midpoint)
    elif p2.orientation == 180:
        T = Stretch(stretch_factor=(sf,1), stretch_center=p1.midpoint)
    elif p2.orientation == 270:
        T = Stretch(stretch_factor=(1,sf), stretch_center=p1.midpoint)
    return T

