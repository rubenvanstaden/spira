import spira.all as spira
from spira.yevon.gdsii.base import __Element__
from spira.yevon.gdsii.elem_list import ElementListParameter, ElementList
from spira.core.parameters.initializer import ParameterInitializer
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = ['Group']


class __Group__(ParameterInitializer):

    elements = ElementListParameter(fdef_name='__create_elements__', doc='List of elements added to cell instance.')

    def __create_elements__(self, elems):
        return self.create_elements(elems)

    def create_elements(self, elems):
        return elems

    def __iter__(self):
        return self.elements.__iter__()

    def __iadd__(self, element):
        """ Add element and reduce the class to a simple compound elements. """
        from spira.yevon.geometry.ports.base import __Port__
        if isinstance(element, (list, Group, spira.ElementList)):
            self.extend(element)
        elif issubclass(type(element), __Element__):
            self.append(element)
        elif element is None:
            return self
        else:
            raise TypeError("Invalid type " + str(type(element)) + " in __Group__.__iadd__().")
        return self

    @property
    def bbox_info(self):
        return self.elements.bbox_info

    def append(self, element):
        el = self.elements
        el.append(element)
        self.elements = el

    def extend(self, elems):
        from spira.yevon.gdsii.group import Group
        el = self.elements
        if isinstance(elems, Group):
            el.extend(elems.elemetals)
        else:
            el.extend(elems)
        self.elements = el

    def flatten(self, level=-1, name_tree=[]):
        self.elements = self.elements.flatten(level=level, name_tree=name_tree)
        return self

    def is_empty(self):
        return self.elements.is_empty()


class Group(__Group__, __Element__):

    def __init__(self, transformation=None, **kwargs):
        super().__init__(transformation=transformation, **kwargs)

    def __eq__(self, other):
        return (self.elements == other.elements) and (self.transformation == other.transformation)

    def flat_copy(self, level=-1):
        if not level == 0:
            return self.elements.flat_copy(level).transform(self.transformation)
        else:
            return spira.ElementList(self.elements)

    def transform(self, transformation=None):
        self.elements.transform(transformation)
        return self

    def expand_transform(self):
        if not self.transformation.is_identity():
            self.elements.transform(self.transformation)
            self.transformation = None  

    @property
    def bbox_info(self):
        return self.elements.bbox_info.transform(self.transformation)


           