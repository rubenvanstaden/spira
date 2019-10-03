import spira.all as spira
import numpy as np
from spira.yevon.geometry.coord import CoordParameter, Coord
from spira.core.transformable import Transformable
from spira.core.transforms.generic import GenericTransform, __ConvertableTransform__
from spira.core.parameters.descriptor import FunctionParameter, SetFunctionParameter
from spira.core.parameters.processors import ProcessorTypeCast
from spira.core.parameters.restrictions import RestrictType
from spira.core.parameters.initializer import SUPPRESSED
from spira.yevon import constants


class Rotation(__ConvertableTransform__):

    def __init__(self, rotation=0, rotation_center=(0,0), absolute_rotation=False, **kwargs):
        if not 'translation' in kwargs:
            kwargs['translation'] = SUPPRESSED
        super().__init__(
            rotation=rotation,
            rotation_center=rotation_center,
            absolute_rotation=absolute_rotation,
            **kwargs)

    absolute_rotation = getattr(GenericTransform, 'absolute_rotation')

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
                self.__sa__ = -1.
        else:
            self.__ca__ = np.cos(value * constants.DEG2RAD)
            self.__sa__ = np.sin(value * constants.DEG2RAD)
        if hasattr(self, '__rotation_center__'):
            rotation_center = self.__rotation_center__
            self.translation = Coord(
                rotation_center.x * (1 - self.__ca__) + rotation_center.y * self.__sa__,
                rotation_center.y * (1 - self.__ca__) - rotation_center.x * self.__sa__)

    rotation = SetFunctionParameter('__rotation__', set_rotation, default=0.0)

    def set_rotation_center(self, rotation_center):
        if not isinstance(rotation_center, Coord):
            rotation_center = Coord(rotation_center[0], rotation_center[1])
        self.__rotation_center__ = rotation_center
        if hasattr(self, '__ca__'):
            self.translation = Coord(
                  rotation_center.x * (1 - self.__ca__) + rotation_center.y * self.__sa__,
                - rotation_center.x * self.__sa__       + rotation_center.y * (1 - self.__ca__))

    rotation_center = SetFunctionParameter(
        local_name='__rotation_center__',
        fset=set_rotation_center,
        restriction=RestrictType(Coord),
        preprocess=ProcessorTypeCast(Coord), 
        default=(0.0, 0.0)
    )

    def __neg__(self):
        return Rotation(-self.rotation, self.rotation_center)

    def apply_to_coord(self, coord):
        coord = self.__rotate__(coord)
        coord = self.__translate__(coord)
        return coord

    def reverse_on_coord(self, coord):      
        coord = self.__inv_translate__(coord)
        coord = self.__inv_rotate__(coord)
        return coord

    def apply_to_array(self, coords):
        coords = self.__rotate_array__(coords)
        coords = self.__translate_array__(coords)
        return coords

    def apply_to_angle(self, angle):
        a = angle
        a += self.rotation
        return a % 360.0

    def is_identity(self):
        return (self.rotation == 0.0)


def shape_rotate(shape, rotation=90, rotation_center=(0,0)):
    return Rotation(rotation, rotation_center)(shape)


class __RotationMixin__(object):

    def rotate(self, rotation=0, rotation_center=(0,0)):
        return self.transform(Rotation(rotation, rotation_center))

    def rotate_copy(self, rotation=0, rotation_center=(0,0)):
        return self.transform_copy(Rotation(rotation, rotation_center))


Transformable.mixin(__RotationMixin__)


 