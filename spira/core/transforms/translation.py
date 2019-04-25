import spira.all as spira
from spira.core.transformable import Transformable
from spira.core.transforms.generic import __ConvertableTransform__, GenericTransform


class Translation(__ConvertableTransform__):

    def __init__(self, translation=(0,0), **kwargs):
        super().__init__(translation=translation, **kwargs)

    translation = getattr(GenericTransform, 'translation')

    def apply_to_object(self, item):
        print('Applying translation')
        print(self.translation)
        return item.__translate__(dx=self.translation[0], dy=self.translation[1])


class __TranslationMixin__(object):
    # def move(self, position):
    #     return self.transform(Translation(position))

    # def move_copy(self, position):
    #     return self.transform_copy(Translation(position))

    def _translate(self, translation=(0,0)):
        print('jjdfbdbsfbksdfjb')
        return self.transform(Translation(translation))

    def translate_copy(self, position):
        return self.transform_copy(Translation(position))


Transformable.mixin(__TranslationMixin__)




