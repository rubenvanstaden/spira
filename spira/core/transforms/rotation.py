import spira.all as spira
import numpy as np
from spira.yevon.geometry.coord import CoordField, Coord
from spira.core.transformable import Transformable
from spira.core.transforms.generic import GenericTransform, __ConvertableTransform__
from spira.core.descriptor import FunctionField, SetFunctionField
from spira.core.param.restrictions import RestrictType
from spira.yevon import constants


class Rotation(__ConvertableTransform__):

    def __init__(self, rotation=0, center=(0,0), **kwargs):
        super().__init__(rotation=rotation, center=center, **kwargs)

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
        if hasattr(self, '__center__'):
            print('A')
            center = self.__center__
            self.translation = Coord(
                center.x * (1 - self.__ca__) + center.y * self.__sa__,
                center.y * (1 - self.__ca__) - center.x * self.__sa__
            )

    rotation = SetFunctionField('__rotation__', set_rotation, default = 0.0)

    def set_rotation_center(self, center):
        if not isinstance(center, Coord):
            center = Coord(center[0], center[1])
        self.__rotation_center__ = center
        if hasattr(self, '__ca__'):
            self.translation = Coord(
                center.x * (1 - self.__ca__) + center.y * self.__sa__,
                center.y * (1 - self.__ca__) - center.x * self.__sa__
            )

    # center = SetFunctionField("__center__", set_rotation_center, restriction=RestrictType(Coord), default=(0.0, 0.0))
    center = SetFunctionField('__center__', set_rotation_center, default=(0.0, 0.0))

    def apply_to_coord(self, coord):
        coord = self.__rotate__(coord)
        coord = self.__translate__(coord)
        return coord
        
    def reverse_on_coord(self, coord):      
        coord = self.__inv_translate__(coord)
        coord = self.__inv_rotate__(coord)
        return coord

    def apply_to_array(self, coords):
        coords = coords[0]
        coords = self.__rotate_array__(coords)
        coords = self.__translate_array__(coords)
        coords = np.array([coords])
        return coords

    def apply_to_angle(self, angle):
        a = angle
        a += self.rotation
        return a % 360.0


class __RotationMixin__(object):

    def _rotate(self, rotation=0, center=(0,0)):
        return self.transform(Rotation(rotation, center))

    def rotate_copy(self, rotation=0, center=(0,0)):
        return self.transform_copy(Rotation(rotation, center))


Transformable.mixin(__RotationMixin__)


 