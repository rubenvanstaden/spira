import spira.all as spira
from spira.core.transforms.generic import GenericTransform
from spira.core.transformable import Transformable


class Reflection(GenericTransform):

    def __init__(self, reflection=False, **kwargs):
        super().__init__(reflection=reflection, **kwargs)

    reflection = getattr(GenericTransform, 'reflection')

    def apply_to_coord(self, coord):
        coord = self.__reflect__(coord)
        coord = self.__translate__(coord)
        return coord

    def apply_to_array(self, coords):
        coords = self.__reflect_array__(coords)
        coords = self.__translate_array__(coords)
        return coords


def shape_reflect(shape, reflection=False):
    return Reflection(reflection=reflection)(shape)


class __ReflectionMixin__(object):

    def reflect(self, reflection=False):
        return self.transform(Reflection(reflection))

    def reflect_copy(self, reflection=False):
        return self.transform_copy(Reflection(reflection))


Transformable.mixin(__ReflectionMixin__)




