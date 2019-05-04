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
        return coord

    # def apply_to_object(self, item):
    #     if self.reflection is True:
    #         item = item.__reflect__(p1=(0,0), p2=(1,0))
    #     else:
    #         item = self
    #     # item = item.__translate__(self)
    #     return item


class __ReflectionMixin__(object):

    def _reflect(self, reflection=False):
        return self.transform(Reflection(reflection))


Transformable.mixin(__ReflectionMixin__)




