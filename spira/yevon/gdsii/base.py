import spira.all as spira

from spira.core.transformable import Transformable
from spira.core.parameters.initializer import FieldInitializer
from spira.core.parameters.initializer import MetaElemental
from spira.core.parameters.descriptor import FunctionField
# from spira.yevon.gdsii.elem_list import ElementalListField
from spira.yevon.rdd import get_rule_deck


RDD = get_rule_deck()


class __Elemental__(Transformable, FieldInitializer, metaclass=MetaElemental):
    """ Base class for all transformable elementals. """

    def get_node_id(self):
        if self.__id__:
            return self.__id__
        else:
            return self.__str__()

    def set_node_id(self, value):
        self.__id__ = value

    node_id = FunctionField(get_node_id, set_node_id)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __add__(self, other):
        if isinstance(other, list):
            l = spira.ElementalList([self])
            l.extend(other)
            return l
        elif isinstance(other, __Elemental__):
            return spira.ElementalList([self, other])
        else:
            raise TypeError("Wrong type of argument for addition in __Elemental__: " + str(type(other)))

    def __radd__(self, other):
        if isinstance(other, list):
            l = spira.ElementalList(other)
            l.append(self)
            return l
        elif isinstance(other, __Elemental__):
            return spira.ElementalList([other, self])
        else:
            raise TypeError("Wrong type of argument for addition in __Elemental__: " + str(type(other)))

    def flatten(self):
        return [self]

    def dependencies(self):
        return None

    # def commit_to_gdspy(self, cell, transformation=None):
    #     return None

