import spira.all as spira
from spira.core.transforms.generic import GenericTransform
from spira.core.transformable import Transformable


class Magnification(GenericTransform):

    def __init__(self, magnification=1, center=(0,0), **kwargs):
        super().__init__(magnification=magnification, center=center, **kwargs)
        
    magnification = getattr(GenericTransform, 'magnification')

    # absolute_magnification = getattr(NoDistortTransform, 'absolute_magnification')
    
    # def set_magnification(self, value):
    #     self.__magnification__ = value
    #     if hasattr(self, "__magnification_center__"):
    #         center = self.__magnification_center__
    #         self.translation = Coord2((1 - self.__magnification__) * center.x,
    #                                       (1 - self.__magnification__) * center.y)
            
            
    # magnification = SetFunctionProperty("__magnification__", set_magnification, default = 1.0)
    
    # def set_magnification_center(self, center):
    #     if not isinstance(center, Coord2):
    #         center = Coord2(center[0], center[1])
    #     self.__magnification_center__ = center
    #     if hasattr(self, "__magnification__"):
    #         self.translation = Coord2((1 - self.__magnification__) * center.x,
    #                                       (1 - self.__magnification__) * center.y)
    # magnification_center = SetFunctionProperty("__magnification_center__", set_magnification_center, restriction = RestrictType(Coord2), preprocess = ProcessorTypeCast(Coord2), default = (0.0, 0.0))


class __Magnification__(object):

    def _magnify(self, magnification=1.0, center=(0,0)):
        return self.transform(Magnification(magnification, center))

    def magnify_copy(self, magnification=1.0, center=(0,0)):
        return self.transform_copy(Magnification(magnification, center))


print('Magnification MIXIN')
Transformable.mixin(__Magnification__)

