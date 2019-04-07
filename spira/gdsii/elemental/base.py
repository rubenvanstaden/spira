from spira.core.transformable import Transformable
from spira.core.initializer import ElementalInitializer


class __Element__(Transformable, ElementalInitializer):
    """ Base class for all transformable elementals. """

    # def __init__(self, transformation=None, **kwargs):
    #     super().__init__(self, transformation=transformation, **kwargs)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def dependencies(self):
        return None

    def __add__(self, other):
        if isinstance(other, list):
            l = ElementList([self])
            l.extend(other)
            return l
        elif isinstance(other, __Element__):
            return ElementList([self, other])
        else:
            raise TypeError("Wrong type of argument for addition in __Element__: " + str(type(other)))

    def __radd__(self, other):
        if isinstance(other, list) :
            l = ElementList(other)
            l.append(self)
            return l
        elif isinstance(other, __Element__):
            return ElementList([other, self])
        else:
            raise TypeError("Wrong type of argument for addition in __Element__: " + str(type(other)))
