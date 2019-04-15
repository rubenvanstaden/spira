from spira.core.transformation import ReversibleTransform

from spira.core.param.variables import *


class GenericTransform(ReversibleTransform):

    # def __init__(self, translation=(0,0), rotation=0, reflection=False, magnification=1, **kwargs):
    #     super().__init__(
    #         translation=translation,
    #         rotation=rotation,
    #         reflection=reflection,
    #         magnification=magnification,
    #         **kwargs
    #     )

    translation = TupleField(default=(0,0))
    rotation = NumberField(default=0)
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
        print(other)
        if issubclass(type(other), GenericTransform):
            T = GenericTransform()
            T.rotation = self.rotation + other.rotation
            T.translation = self.translation + other.translation
        else:
            raise ValueError('Not implemented!')
        return T

    def __iadd__(self, other):
        self.__add__(other)
        return self

    def __eq__(self, other):
        pass

    def __ne__(self, other):
        pass

    def __sub__(self, other):
        return self.__add__(-other)
        
    def __isub__(self, other):
        return self.__iadd__(-other)

    def __neg__(self):
        pass

    def apply_to_object(self, item):
        item = item.__reflect__()
        item = item.__rotate__(angle=self.rotation)
        item = item.__translate__(dx=self.translation[0], dy=self.translation[1])
        return item

    def id_string(self):
        """ Gives a hash of the transform (for naming purposes) """
        return self.__str__()

