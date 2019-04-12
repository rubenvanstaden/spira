import spira
from spira.core.transforms.generic import GenericTransform
from spira.core.transformable import Transformable


class Reflection(GenericTransform):

    def __init__(self, reflection=0, **kwargs):
        kwargs['translation'] = SUPPRESSED
        kwargs['v_mirror'] = True
        
        super().__init__(reflection=reflection, **kwargs)
        
    def set_mirror_plane_y(self, value):
        self.__mirror_plane_y__ = value
        self.translation = Coord2(0.0, 2.0 * value)

    reflection = SetFunctionProperty("__reflection__", set_mirror_plane_y, restriction=RESTRICT_NUMBER, default=0)


class __ReflectionMixin__(object):

    def reflect(self, reflection=False):
        return self.transform(Reflection(reflection))


Transformable.mixin(__ReflectionMixin__)




