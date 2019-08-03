import numpy as np
from spira.core.transformation import ReversibleTransform

from spira.yevon import utils
from numpy.linalg import norm
from copy import deepcopy
from spira.core.parameters.variables import *
from spira.yevon.geometry.coord import CoordParameter, Coord
from spira.core.parameters.descriptor import FunctionParameter, SetFunctionParameter
from spira.core.transformation import Transform
from spira.yevon import constants


class GenericTransform(ReversibleTransform):
    """  """

    def __init__(self, translation=(0,0), rotation=0, absolute_rotation=False, **kwargs):
        super().__init__(translation=translation, rotation=rotation, absolute_rotation=absolute_rotation, **kwargs)

    def set_rotation(self, value):
        self.__rotation__ = value % 360.0
        if value % 90.0 == 0.0:
            if self.__rotation__ == 0.0:
                self.__ca__ = 1.0
                self.__sa__ = 0.0
            elif self.__rotation__ == 90.0:
                self.__ca__ = 0.0
                self.__sa__ = 1.0
            elif self.__rotation__ == 180.0:
                self.__ca__ = -1.0
                self.__sa__ = 0.0
            elif self.__rotation__ == 270.0:
                self.__ca__ = 0.0
                self.__sa__ = -1.0
        else:
            self.__ca__ = np.cos(value * constants.DEG2RAD)
            self.__sa__ = np.sin(value * constants.DEG2RAD)

    rotation = SetFunctionParameter(local_name='__rotation__', fset=set_rotation, default=0.0)
    magnification = NumberParameter(default=1)
    reflection = BoolParameter(default=False)
    translation = CoordParameter(local_name='__translation__')
    absolute_rotation = BoolParameter(local_name='__absolute_rotation__', default=False)

    def __str__(self):
        """ Gives a string representing the transform. """
        return "<T {}, R {}, RF {}, M {}>".format(
            str(self.translation),
            str(self.rotation),
            str(self.reflection),
            str(self.magnification)
        )

    def __translate__(self, coord):
        C = Coord(coord[0] + self.translation.x, coord[1] + self.translation.y)
        return C

    def __rotate__(self, coord):
        return Coord(coord[0] * self.__ca__ - coord[1] * self.__sa__, coord[0] * self.__sa__ + coord[1] * self.__ca__)

    def __magnify__(self, coord):
        return Coord(coord[0] * self.magnification, coord[1] * self.magnification)

    def __inv_translate__(self, coord):
        return Coord(coord[0] - self.translation.x, coord[1] - self.translation.y)
    
    def __inv_rotate__(self, coord):
        return Coord(coord[0] * self.__ca__ + coord[1] * self.__sa__, - coord[0] * self.__sa__ + coord[1] * self.__ca__)

    def __inv_magnify__(self, coord):
        return Coord(coord[0] / self.magnification, coord[1] / self.magnification)

    def __reflect__(self, coords, p1=(0,0), p2=(1,0)):
        if self.reflection is True:
            points = np.array(coords.to_numpy_array())
            p1 = np.array(p1)
            p2 = np.array(p2)
            if np.asarray(points).ndim == 1:
                t = np.dot((p2-p1), (points-p1))/norm(p2-p1)**2
                pts = 2*(p1 + (p2-p1)*t) - points
            if np.asarray(points).ndim == 2:
                raise ValueError('This is a array, not an coordinate.')
        else:
            pts = coords
        pts = Coord(pts[0], pts[1])
        return pts

    def __reflect_array__(self, coords, p1=(0,0), p2=(1,0)):
        if self.reflection is True:
            points = np.array(coords)
            p1 = np.array(p1)
            p2 = np.array(p2)
            if np.asarray(points).ndim == 1:
                raise ValueError('This is a coordinate, not an array.')
            if np.asarray(points).ndim == 2:
                t = np.dot((p2-p1), (p2-p1))/norm(p2-p1)**2
                pts = np.array([2*(p1 + (p2-p1)*t) - p for p in points])
        else:
            pts = coords
        return pts

    def __translate_array__(self, coords):
        # FIXME: Why should I convert to float!
        coords = [[float(c[0]), float(c[1])] for c in coords]
        coords += np.array([self.translation.x, self.translation.y])
        return coords

    def __rotate_array__(self, coords):
        x_a = np.array([self.__ca__, -self.__sa__])
        y_a = np.array([self.__sa__, self.__ca__])
        coords = np.transpose(np.vstack((np.sum(coords * x_a, 1), np.sum(coords * y_a, 1))))
        return coords

    def __magnify_array__(self, coords):
        coords *= np.array([self.magnification, self.magnification])
        return coords

    def apply_to_coord(self, coord):
        coord = self.__reflect__(coord)
        coord = self.__rotate__(coord)
        coord = self.__magnify__(coord)
        coord = self.__translate__(coord)
        return coord

    def apply_to_array(self, coords):
        coords = self.__reflect_array__(coords)
        coords = self.__rotate_array__(coords)
        coords = self.__magnify_array__(coords)
        coords = self.__translate_array__(coords)
        return coords

    def apply_to_angle(self, angle):
        a = angle
        if self.reflection:
            a = -a
        a += self.rotation
        return a % 360.0

    def __add__(self, other):
        if other is None:
            return deepcopy(self)

        # if issubclass(type(other), GenericTransform):
        if isinstance(other, GenericTransform):
            T = GenericTransform()

            if other.reflection is True: s_1 = -1
            else: s_1 = 1

            M1 = 1.0

            if not self.absolute_rotation:
                T.rotation = s_1 * self.rotation + other.rotation
                ca = other.__ca__
                sa = other.__sa__
            else:
                T.rotation = s_1 * self.rotation
                ca = 1.0
                sa = 0.0

            # Counterclockwise rotation
            # cx = self.translation.x + ca * other.translation.x * M1 - s_1 * sa * other.translation.y * M1
            # cy = self.translation.y + sa * other.translation.x * M1 + s_1 * ca * other.translation.y * M1
            cx = other.translation.x + ca * self.translation.x * M1 - s_1 * sa * self.translation.y * M1
            cy = other.translation.y + sa * self.translation.x * M1 + s_1 * ca * self.translation.y * M1
            # cx = other.translation.x + ca * self.translation.x * M1 + s_1 * sa * self.translation.y * M1
            # cy = -other.translation.y + sa * self.translation.x * M1 + s_1 * ca * self.translation.y * M1
            T.translation = Coord(cx, cy)

            T.absolute_rotation = self.absolute_rotation or other.absolute_rotation
            T.reflection = (not self.reflection == other.reflection)

        else:
            T = Transform.__add__(self, other)
        return T

    def __iadd__(self, other):

        # return self.__add__(other)

        if other is None:
            return self

        # if issubclass(type(other), GenericTransform):
        if isinstance(other, GenericTransform):
            T = GenericTransform()

            if other.reflection is True: s_1 = -1
            else: s_1 = 1

            M1 = 1.0

            if not self.absolute_rotation:
                self.rotation = s_1 * self.rotation + other.rotation
                ca = other.__ca__
                sa = other.__sa__
            else:
                self.rotation = s_1 * self.rotation
                ca = 1
                sa = 0

            # Counterclockwise rotation
            # cx = self.translation.x + ca * other.translation.x * M1 - s_1 * sa * other.translation.y * M1
            # cy = self.translation.y + sa * other.translation.x * M1 + s_1 * ca * other.translation.y * M1
            cx = other.translation.x + ca * self.translation.x * M1 - s_1 * sa * self.translation.y * M1
            cy = other.translation.y + sa * self.translation.x * M1 + s_1 * ca * self.translation.y * M1
            # cx = other.translation.x + ca * self.translation.x * M1 + s_1 * sa * self.translation.y * M1
            # cy = -other.translation.y + sa * self.translation.x * M1 + s_1 * ca * self.translation.y * M1
            self.translation = Coord(cx, cy)

            self.absolute_rotation = self.absolute_rotation or other.absolute_rotation
            self.reflection = (not self.reflection == other.reflection)

        else:
            raise ValueError('Cannot add transforms')

        return self

    def __sub__(self, other):
        """ returns the concatenation of this transform and the reverse of other """
        if other is None: return copy.deepcopy(self)
        if not isinstance(other, ReversibleTransform):
            raise TypeError("Cannot subtract an irreversible transform")
        return self.__add__(-other)

    def __isub__(self, other):
        """ concatenates the reverse of other to this transform """
        if other is None: return self
        if not isinstance(other, ReversibleTransform):
            raise TypeError("Cannot subtract an irreversible transform")
        return self.__iadd__(self, -other)

    def __eq__(self, other):
        if other is None: return self.is_identity()
        if not isinstance(other, GenericTransform):
            return False
        return (
            (self.rotation == other.rotation) and
            (self.translation == other.translation) and
            (self.reflection == other.reflection) and
            (self.magnification == other.magnification)
        )

    def __ne__(self, other):
        """ checks if the transforms do different things """

        if other is None: return not self.is_identity()
        if not isinstance(other, GenericTransform):
            return False
        return (
            (self.rotation != other.rotation) or
            (self.translation != other.translation) or
            (self.reflection != other.reflection) or
            (self.magnification != other.magnification)
        )

    def __neg__(self):
        from spira.core.transforms.translation import Translation
        from spira.core.transforms.rotation import Rotation
        T = Translation(translation=-self.translation) + Rotation(rotation=-self.rotation, rotation_center=(0,0))
        # T = Translation(translation=-self.translation)
        # T += Rotation(rotation=-self.rotation, rotation_center=(0,0))
        return T

    def id_string(self):
        """ Gives a hash of the transform (for naming purposes) """
        return self.__str__()

    def is_identity(self):
        """ Returns True if the transformation does nothing """
        return (
            (self.rotation == 0.0) and 
            (self.translation.x == 0.0) and 
            (self.translation.y == 0.0) and 
            (not self.reflection) and 
            (self.magnification == 1.0)
        )


BASE = GenericTransform

from spira.core.parameters.descriptor import ConvertParameter
class __ConvertableTransform__(GenericTransform):
    """ Converts a transform to a GenericTransform when adding 
    or subtracting multiple transforms. """

    def __convert_transform__(self):
        self.__class__ = BASE

    reflection = ConvertParameter(BASE, 'reflection', __convert_transform__)
    rotation = ConvertParameter(BASE, 'rotation', __convert_transform__)
    translation = ConvertParameter(BASE, 'translation', __convert_transform__)
    magnification = ConvertParameter(BASE, 'magnification', __convert_transform__)
    absolute_rotation = ConvertParameter(BASE, 'absolute_rotation', __convert_transform__)

    def __add__(self, other):
        self.__convert_transform__()
        return BASE.__add__(self, other)

    def __iadd__(self, other):
        self.__convert_transform__()
        return BASE.__iadd__(self, other)

    def __isub__(self, other):
        self.__convert_transform__()
        return BASE.__isub__(self, other)

