
import spira
from spira.core.transforms.generic import GenericTransform
from spira.core.transformable import Transformable


class Rotation(GenericTransform):

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
            self.__ca__ = cos(value * constants.DEG2RAD)
            self.__sa__ = sin(value * constants.DEG2RAD)
        if hasattr(self, "__rotation_center__"):
            center = self.__rotation_center__
            self.translation = Coord2(center.x * (1 - self.__ca__) + center.y * self.__sa__,
                                      center.y * (1 - self.__ca__) - center.x * self.__sa__)
            
    rotation = SetFunctionProperty("__rotation__", set_rotation, default = 0.0)
    
    def set_rotation_center(self, center):
        if not isinstance(center, Coord2):
            center = Coord2(center[0], center[1])
        self.__rotation_center__ = center
        if hasattr(self, "__ca__"):
            self.translation = Coord2(center.x * (1 - self.__ca__) + center.y * self.__sa__,
                                      center.y * (1 - self.__ca__) - center.x * self.__sa__)

    rotation_center = SetFunctionProperty("__rotation_center__", set_rotation_center, restriction = RestrictType(Coord2), preprocess = ProcessorTypeCast(Coord2), default = (0.0, 0.0))
 

class __RotationMixin__(object):

    def rotate(self, rotation=0, center=(0,0)):
        return self.transform(Rotation(rotation, center))

    def rotate_copy(self, rotation=0, center=(0,0)):
        return self.transform_copy(Rotation(rotation, center))


Transformable.mixin(__RotationMixin__)


 