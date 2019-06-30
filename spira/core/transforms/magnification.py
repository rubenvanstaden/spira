import spira.all as spira
import numpy as np
from spira.yevon.geometry.coord import CoordParameter, Coord
from spira.core.transformable import Transformable
from spira.core.transforms.generic import GenericTransform, __ConvertableTransform__
from spira.core.parameters.descriptor import FunctionParameter, SetFunctionParameter
from spira.core.parameters.restrictions import RestrictType
from spira.core.parameters.processors import ProcessorTypeCast
from spira.yevon import constants
from spira.core.parameters.processors import *


__all__ = ["Magnification"]


class Magnification(__ConvertableTransform__):
    """ Scaling transformation with respect to a given point. """

    def __init__(self, magnification=1.0, magnification_center=(0.0, 0.0), **kwargs):
        super().__init__(magnification=magnification, magnification_center=magnification_center, **kwargs)

    def set_magnification(self, value):
        self.__magnification__ = value
        if hasattr(self, '__magnification_center__'):
            center = self.__magnification_center__
            self.translation = Coord((1 - self.__magnification__) * center.x, (1 - self.__magnification__) * center.y)
            

    magnification = SetFunctionParameter('__magnification__', set_magnification, default=1.0)
    
    def set_magnification_center(self, center):
        if not isinstance(center, Coord):
            center = Coord(center[0], center[1])
        self.__magnification_center__ = center
        if hasattr(self, '__magnification__'):
            self.translation = Coord((1 - self.__magnification__) * center.x, (1 - self.__magnification__) * center.y)

    magnification_center = SetFunctionParameter(
        local_name='__magnification_center__', 
        fset=set_magnification_center, 
        restriction=RestrictType(Coord), 
        preprocess=ProcessorTypeCast(Coord), 
        default=(0.0, 0.0)
    )
    
    def apply_to_coord(self, coord):      
        coord = self.__magnify__(coord)
        coord = self.__translate__(coord)
        return coord

    def reverse_on_coord(self, coord):      
        coord = self.__inv_translate__(coord)
        coord = self.__inv_magnify__(coord)
        return coord

    def apply_to_array(self, coords):      
        coords = self.__magnify_array__(coords)
        coords = self.__translate_array__(coords)
        return coords

    def reverse_on_array(self, coords):      
        coords = self.__inv_translate_array__(coords)
        coords = self.__inv_magnify__array__(coords)
        return coords

    def apply_to_length(self, length):
        return length * self.magnification
    
    def reverse_on_length(self, length):
        return length / self.magnification
    
    def __neg__(self):
        """ Returns reverse transformation """
        return Magnification(self.magnification_center, 1.0 / self.magnification)    

    def is_identity(self):
        return (self.magnification == 1.0)


class __Magnification__(object):

    def magnify(self, magnification=1.0, center=(0,0)):
        return self.transform(Magnification(magnification, center))

    def magnifycopy(self, magnification=1.0, center=(0,0)):
        return self.transform_copy(Magnification(magnification, center))


Transformable.mixin(__Magnification__)

