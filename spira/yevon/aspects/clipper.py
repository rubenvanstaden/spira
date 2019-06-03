import numpy as np
from spira.yevon.aspects.base import __Aspects__


class __ClipperAspects__(__Aspects__):

    def __sub__(self, shape):
        raise Exception("Method __sub__ not implemented in abstract class __ShapeBooleanOpsAspect__")
    
    def __and__(self, shape):
        raise Exception("Method __and__ not implemented in abstract class __ShapeBooleanOpsAspect__")
    
    def __or__(self, shape):
        raise Exception("Method __or__ not implemented in abstract class __ShapeBooleanOpsAspect__")
    
    def union(self, other):
        return self.__or__(other)

    def intersection(self, other):
        return self.__and__(other)

    def difference(self, other):
        return self.__sub__(other)

  