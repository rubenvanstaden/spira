import numpy as np
from spira.yevon.properties.base import __Property__


class __ClipperAspects__(__Property__):

    def __sub__(self, shape):
        raise Exception("Method __sub__ not implemented in abstract class __ShapeBooleanOpsAspect__")
    
    def __and__(self, shape):
        raise Exception("Method __and__ not implemented in abstract class __ShapeBooleanOpsAspect__")
    
    def __or__(self, shape):
        raise Exception("Method __or__ not implemented in abstract class __ShapeBooleanOpsAspect__")
    
    def sub(self, shape):
        return self.__sub__(shape)
        
    def xor(self, shape):        
        return self.__xor__(shape)    
    
  