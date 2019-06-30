import spira.all as spira
from spira.yevon.gdsii.base import __Element__
from spira.yevon.gdsii.elem_list import ElementListParameter, ElementList
from spira.core.parameters.initializer import ParameterInitializer
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = ['Group']


class __Group__(ParameterInitializer):

    elements = ElementListParameter(fdef_name='__create_elements__', doc='List of ports to be added to the cell instance.')

    def __create_elements__(self, elems):
        el = self.create_elements(elems)
        if hasattr(self, 'disable_edge_ports'):
            if self.disable_edge_ports:
                for e in el:
                    if isinstance(e, spira.Polygon):
                        e.disable_edge_ports = True
        return el

    def create_elements(self, elems):
        return elems

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

    def __iadd__(self, element):
        from spira.yevon.geometry.ports.base import __Port__
        """ Add element and reduce the class to a simple compound elements. """
        if isinstance(element, (list, spira.ElementList)):
            self.extend(element)
        elif isinstance(element, __Element__):
            self.append(element)
        elif element is None:
            return self
        elif issubclass(type(element), __Port__):
            self.ports += element
        else:
            raise TypeError("Invalid type " + str(type(element)) + " in __Group__.__iadd__().")
        return self

    def flatten(self, level=-1):
        self.elements = self.elements.flatcopy(level=level)
        return self

    def __iter__(self):
        return self.elements.__iter__()

    def is_empty(self):
        return self.elements.is_empty()

    @property
    def bbox_info(self):
        return self.elements.bbox_info
    

class Group(__Group__, __Element__):

    def __init__(self, transformation=None, **kwargs):
        super().__init__(transformation=transformation, **kwargs)
    
    def flatcopy(self, level=-1):
        if not level == 0:
            return self.elements.flatcopy(level).transform(self.transformation)
        else:
            return spira.ElementList(self.elements)

    def expand_transform(self):
        if not self.transformation.is_identity():
            self.elements.transform(self.transformation)
            self.transformation = None  

    def __eq__(self, other):
            return (self.elements == other.elements) and (self.transformation == other.transformation)


           