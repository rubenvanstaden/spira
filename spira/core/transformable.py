import numpy as np
from copy import deepcopy
from numpy.linalg import norm
from spira.core.mixin import MixinBowl
from spira.core.transformation import Transform
from spira.core.transformation import TransformationParameter


class __Transformable__(MixinBowl):
    """ Transformable base class. """

    def transform(self, transformation):
        return self

    def transform_copy(self, transformation):
        T = deepcopy(self)
        T.transform(transformation)
        return T

    def reverse_transform(self, transformation):
        return self.transform(-transformation)

    def reverse_transform_copy(self, transformation):
        T = deepcopy(self)
        T.reverse_transform(transformation)
        return T


class Transformable(__Transformable__):
    """ Object that can be transformed. """

    __transform_type__ = Transform

    transformation = TransformationParameter()

    def __init__(self, transformation=None, **kwargs):
        if (not 'transformation' in kwargs) or (transformation != None):
            kwargs['transformation'] = transformation
        super().__init__(**kwargs)

    def transform(self, transformation=None):
        if issubclass(type(transformation), self.__transform_type__):
            self.transformation = self.transformation + transformation
            # self.transformation += transformation
        elif transformation is None:
            return
        else:
            raise TypeError("Wrong type " + str(type(transformation)) + " for transformation in Transformable")
        return self


