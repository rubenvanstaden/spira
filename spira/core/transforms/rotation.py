import spira.all as spira
from spira.yevon.geometry.coord import CoordField, Coord
from spira.core.transformable import Transformable
from spira.core.transforms.generic import GenericTransform, __ConvertableTransform__
from spira.core.descriptor import FunctionField, SetFunctionField


class Rotation(__ConvertableTransform__):

    def __init__(self, rotation=0, center=(0,0), **kwargs):
        super().__init__(rotation=rotation, center=center, **kwargs)
        
    # center = CoordField(default=(0,0))
    # rotation = getattr(GenericTransform, 'rotation')

    def set_rotation(self, value):
        self.__rot__ = value
        if hasattr(self, '__center__'):
            print('center detected!!!')
            print(self.center)
            center = self.__center__
            self.translation = Coord(center[0], center[1])

    rotation = SetFunctionField('__rot__', set_rotation, default=0)
    
    def set_center(self, value):
        self.__center__ = value
        if hasattr(self, 'rotation'):
            print('rotation detected!!!')
            self.translation = Coord(value[0], value[1])

    center = SetFunctionField('__center__', set_center, default=0)

    # def get_rotation(self):
    #     return self.__rotation__

    # def set_rotation(self, value):
    #     self.__rotation__ = value
    #     if hasattr(self, 'center'):
    #         print('center detected!!!')
    #         # self.translation = Coord(self.center[0], self.center[1])

    # rotation = FunctionField(get_rotation, set_rotation)

    def __neg__(self):
        return Rotation(rotation=-self.rotation, center=self.center)

    def apply_to_object(self, item):
        print('Apply rotation...')
        print(item)
        item = item.__rotate__(angle=self.rotation, center=self.center)
        return item


class __RotationMixin__(object):

    def _rotate(self, rotation=0, center=(0,0)):
        return self.transform(Rotation(rotation, center))

    def rotate_copy(self, rotation=0, center=(0,0)):
        return self.transform_copy(Rotation(rotation, center))


Transformable.mixin(__RotationMixin__)


 