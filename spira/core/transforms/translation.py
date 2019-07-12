import spira.all as spira
from copy import deepcopy
from spira.core.transformable import Transformable
from spira.yevon.geometry.coord import Coord
from spira.core.transforms.generic import __ConvertableTransform__, GenericTransform


class Translation(__ConvertableTransform__):
    """  """

    def __init__(self, translation=(0,0), **kwargs):
        super().__init__(translation=translation, **kwargs)

    translation = getattr(GenericTransform, 'translation')

    def apply_to_coord(self, coord):
        return self.__translate__(coord)

    def apply_to_array(self, coords):
        return self.__translate_array__(coords)

    def reverse_on_coord(self, coord):      
        return self.__inv_translate__(coord)

    def reverse_on_array(self, coords):      
        return self.__inv_translate_array__(coords)

    def __add__(self, other):
        """ Returns the concatenation of this transform and other """
        if other is None:
            return deepcopy(self)
        if isinstance(other, Translation):
            x = self.translation.x + other.translation.x
            y = self.translation.y + other.translation.y
            return Translation(Coord(x, y))
        else:
            # return GenericTransform.__add__(self, other)
            return __ConvertableTransform__.__add__(self, other)

    def __iadd__(self, other):
        """ Concatenates other to this transform. """
        if other is None:
            return self
        if isinstance(other, Translation):
            x = self.translation.x + other.translation.x
            y = self.translation.y + other.translation.y
            self.translation = Coord(x, y)
            return self
        else:
            # return GenericTransform.__iadd__(self, other)
            return __ConvertableTransform__.__iadd__(self, other)

    def __neg__(self):
        """ Helper methods which returns the reverse transformation """
        return Translation(Coord(-self.translation.x, -self.translation.y))

    def is_identity(self):
        return ((self.translation.x == 0.0) and (self.translation.y == 0.0))


def shape_translate(shape, translation=(1,0)):
    return Translation(translation)(shape)


class __TranslationMixin__(object):

    def translate(self, translation=(0,0)):
        return self.transform(Translation(translation))

    def translate_copy(self, position):
        return self.transform_copy(Translation(position))


Transformable.mixin(__TranslationMixin__)




