import numpy as np
from spira.core.transformation import ReversibleTransform

from spira.yevon import utils
from spira.core.param.variables import *
from spira.yevon.geometry.coord import CoordField, Coord
from spira.core.descriptor import FunctionField, SetFunctionField


class GenericTransform(ReversibleTransform):

    translation = CoordField()
    # rotation = NumberField(default=0)

    def set_rotation(self, value):
        self.__rot__ = value

    rotation = SetFunctionField('__rot__', set_rotation, default=0)

    reflection = BoolField(default=False)
    magnification = NumberField(default=1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __str__(self):
        """ Gives a string representing the transform. """
        return "_M=%s-R=%s-RF=%s-MN=%s" % (
            str(self.translation),
            str(self.rotation),
            str(self.reflection),
            str(self.magnification)
        )

    def __add__(self, other):
        if issubclass(type(other), GenericTransform):
            print(self.translation)
            print(other.translation)
            T = GenericTransform()
            T.reflection = (not self.reflection and other.reflection)
            T.rotation = self.rotation + other.rotation
            T.translation = Coord(self.translation) + other.translation
        else:
            raise ValueError('Not implemented!')
        return T

    def __iadd__(self, other):
        if other is None:
            return self
        if issubclass(type(other), GenericTransform):
            self.reflection = (not self.reflection and other.reflection)
            self.rotation = self.rotation + other.rotation
            self.translation = Coord(self.translation) + other.translation
        else:
            raise ValueError('Not implemented!')
        return self

    def __sub__(self, other):
        return self.__add__(-other)

    def __isub__(self, other):
        return self.__iadd__(-other)

    def __eq__(self, other):
        pass

    def __ne__(self, other):
        pass

    def __neg__(self):
        pass

    def apply_to_object(self, item):
        print('Applying generic transform...')
        print(self)
        print(item)
        print(self.rotation)
        print('\n------------------------')
        if self.reflection is True:
            item = item.__reflect__()
        item = item.__rotate__(angle=self.rotation)
        item = item.__translate__(dx=self.translation[0], dy=self.translation[1])
        return item

    def id_string(self):
        """ Gives a hash of the transform (for naming purposes) """
        return self.__str__()


BASE = GenericTransform

from spira.core.descriptor import ConvertField
class __ConvertableTransform__(GenericTransform):
    """ Converts a transform to a GenericTransform when adding 
    or subtracting multiple transforms. """

    def __convert_transform__(self):
        self.__class__ = BASE
        
    translation = ConvertField(BASE, 'translation', __convert_transform__)
    rotation = ConvertField(BASE, 'rotation', __convert_transform__)
    # reflection = ConvertProperty(BASE, "reflection", __convert_transform__)
    # magnification = ConvertProperty(BASE, "magnification", __convert_transform__)
    
    def __add__(self, other):
        self.__convert_transform__()
        return BASE.__add__(self, other)

    def __iadd__(self, other):
        self.__convert_transform__()
        return BASE.__iadd__(self, other)

    def __isub__(self, other):
        self.__convert_transform__()
        return BASE.__isub__(self, other)

