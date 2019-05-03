import numpy as np
from spira.core.transformation import ReversibleTransform

from spira.yevon import utils
from numpy.linalg import norm
from spira.core.param.variables import *
from spira.yevon.geometry.coord import CoordField, Coord
from spira.core.descriptor import FunctionField, SetFunctionField


DEG2RAD = np.pi/180


class GenericTransform(ReversibleTransform):
    """  """

    def __init__(self, translation=(0,0), rotation=0, **kwargs):
        super().__init__(translation=translation, rotation=rotation, **kwargs)

    translation = CoordField()

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
            self.__ca__ = np.cos(value * DEG2RAD)
            self.__sa__ = np.sin(value * DEG2RAD)

    rotation = SetFunctionField("__rotation__", set_rotation, default=0.0)

    # def set_rotation(self, value):
    #     self.__rot__ = value

    # rotation = SetFunctionField('__rot__', set_rotation, default=0)

    reflection = BoolField(default=False)
    magnification = NumberField(default=1)

    def __str__(self):
        """ Gives a string representing the transform. """
        return "_M=%s-R=%s-RF=%s-MN=%s" % (
            str(self.translation),
            str(self.rotation),
            str(self.reflection),
            str(self.magnification)
        )

    def __translate__(self, coord):
        if not isinstance(self.translation, Coord):
            self.translation = Coord(self.translation[0], self.translation[1])
        return Coord(coord[0] + self.translation.x, coord[1] + self.translation.y)

    def __rotate__(self, coord):
        return Coord(coord[0] * self.__ca__ - coord[1] * self.__sa__, coord[0] * self.__sa__ + coord[1] * self.__ca__)

    def __magnify__(self, coord):
        return Coord(coord[0] * self.magnification, coord[1] * self.magnification)
        
    def __reflect__(self, coords, p1=(0,0), p2=(1,0)):

        if self.reflection is True:
            points = np.array(coords.convert_to_array())
            p1 = np.array(p1)
            p2 = np.array(p2)
            print(points)
            if np.asarray(points).ndim == 1:
                print('wmefuebfk')
                t = np.dot((p2-p1), (points-p1))/norm(p2-p1)**2
                pts = 2*(p1 + (p2-p1)*t) - points
            if np.asarray(points).ndim == 2:
                raise ValueError('This is a array, not an coordinate.')
                # t = np.dot((p2-p1), (p2-p1))/norm(p2-p1)**2
                # pts = np.array([2*(p1 + (p2-p1)*t) - p for p in points])
        else:
            pts = coords
        pts = Coord(pts[0], pts[1])
        return pts

    def __reflect_array__(self, coords, p1=(0,0), p2=(1,0)):
        print('Reflection Array!!!')
        if self.reflection is True:
            points = np.array(coords); p1 = np.array(p1); p2 = np.array(p2)
            if np.asarray(points).ndim == 1:
                # t = np.dot((p2-p1), (points-p1))/norm(p2-p1)**2
                # pts = 2*(p1 + (p2-p1)*t) - points
                raise ValueError('This is a coordinate, not an array.')
            if np.asarray(points).ndim == 2:
                t = np.dot((p2-p1), (p2-p1))/norm(p2-p1)**2
                pts = np.array([2*(p1 + (p2-p1)*t) - p for p in points])
        else:
            pts = coords
        return pts

    def __translate_array__(self, coords):
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
        coords = coords[0]
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
        if issubclass(type(other), GenericTransform):
            T = GenericTransform()

            if other.reflection is True: S_1 = -1
            else: S_1 = 1

            T.reflection = (not self.reflection == other.reflection)
            T.rotation = S_1 * (self.rotation + other.rotation)
            T.translation = Coord(self.translation) + other.translation
        else:
            raise ValueError('Not implemented!')
        return T

    def __iadd__(self, other):
        return self.__add__(other)

        # if other is None:
        #     return self
        # # if issubclass(type(other), GenericTransform):
        # print('\n\n')
        # print(self)
        # print(type(self))
        # print(type(other))
        # if isinstance(other, GenericTransform):
        #     self.reflection = (not self.reflection and other.reflection)
        #     self.rotation = self.rotation + other.rotation
        #     self.translation = Coord(self.translation) + other.translation
        # else:
        #     raise ValueError('Not implemented!')
        # print(self)
        # print(type(self))
        # print('\n\n')
        # return self

    def __sub__(self, other):
        return self.__add__(-other)

    def __isub__(self, other):
        return self.__iadd__(-other)

    def __eq__(self, other):
        pass

    def __ne__(self, other):
        pass

    def __neg__(self):
        pass

    def id_string(self):
        """ Gives a hash of the transform (for naming purposes) """
        return self.__str__()


BASE = GenericTransform

from spira.core.descriptor import ConvertField
class __ConvertableTransform__(GenericTransform):
    """ Converts a transform to a GenericTransform when adding 
    or subtracting multiple transforms. """

    def __convert_transform__(self):
        self.__class__ = BASE

    reflection = ConvertField(BASE, 'reflection', __convert_transform__)
    rotation = ConvertField(BASE, 'rotation', __convert_transform__)
    translation = ConvertField(BASE, 'translation', __convert_transform__)
    # magnification = ConvertProperty(BASE, 'magnification', __convert_transform__)

    def __add__(self, other):
        self.__convert_transform__()
        return BASE.__add__(self, other)

    def __iadd__(self, other):
        self.__convert_transform__()
        return BASE.__iadd__(self, other)

    def __isub__(self, other):
        self.__convert_transform__()
        return BASE.__isub__(self, other)

