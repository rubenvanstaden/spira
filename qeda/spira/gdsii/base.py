import spira
from core import param
from core.transformable import Transformable
from core.initializer import FieldInitializer


class __Elemental__(Transformable, FieldInitializer, metaclass=MetaElemental):
    """ Base class for all transformable elementals. """

    def get_node_id(self):
        if self.__id__:
            return self.__id__
        else:
            return self.__str__()

    def set_node_id(self, value):
        self.__id__ = value

    node_id = param.FunctionField(get_node_id, set_node_id)

    # def __init__(self, transformation=None, **kwargs):
    #     super().__init__(self, transformation=transformation, **kwargs)

    def __init__(self, **kwargs):
        # super().__init__(**kwargs)
        Transformable.__init__(self, **kwargs)
        FieldInitializer.__init__(self, **kwargs)
        # ElementalInitializer.__init__(self, **kwargs)

    def flatten(self):
        return [self]

    def commit_to_gdspy(self, cell, gdspy_commit=None):
        return None

    def dependencies(self):
        return None

    def __add__(self, other):
        if isinstance(other, list):
            l = spira.ElementList([self])
            l.extend(other)
            return l
        elif isinstance(other, __Elemental__):
            return spira.ElementList([self, other])
        else:
            raise TypeError("Wrong type of argument for addition in __Elemental__: " + str(type(other)))

    def __radd__(self, other):
        if isinstance(other, list) :
            l = spira.ElementList(other)
            l.append(self)
            return l
        elif isinstance(other, __Elemental__):
            return spira.ElementList([other, self])
        else:
            raise TypeError("Wrong type of argument for addition in __Elemental__: " + str(type(other)))


class __Group__(FieldInitializer):

    elementals = param.ElementalListField(fdef_name='create_elementals', doc='List of elementals to be added to the cell instance.')

    def create_elementals(self, elems):
        result = spira.ElementList()
        return result

    def dependencies(self):
        return self.elements.dependencies()

    def append(self, element):
        el = self.elementals
        el.append(element)
        self.elementals = el

    def extend(self, elems):
        from spira.gdsii.group import Group
        el = self.elementals
        if isinstance(elems, Group):
            el.extend(elems.elemetals)
        else:
            el.extend(elems)
        self.elements = el  

    def __iadd__(self, element):
        """ Add elemental and reduce the class to a simple compound elementals. """
        if isinstance(element, list):
            self.extend(element)
        elif isinstance(element, __Element__):
            self.append(element)
        elif element is None:
            return self
        else:
            raise TypeError("Invalid type " + str(type(element)) + " in __Group__.__iadd__().")
        return self

    def add_el(self, elems):
        self.elementals += elems

    def flatten(self, level = -1):
        self.elementals = self.elementals.flat_copy(level=level)
        return self

    def __iter__(self):
        return self.elementals.__iter__()

    def is_empty(self):
        return self.elementals.is_empty()

    def __eq__(self,other):
        if other == None:
            return False
        if not isinstance(other, spira.Cell):
            return False
        self_el = self.elementals
        other_el = other.elementals
        if len(self_el) != len(other_el):
            return False
        for e1, e2 in zip(self_el, other_el):
            if (e1 != e2):
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)
