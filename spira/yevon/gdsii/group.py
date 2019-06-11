import spira.all as spira
from spira.yevon.gdsii.base import __Elemental__
from spira.yevon.gdsii.elem_list import ElementalListField, ElementalList
from spira.core.parameters.initializer import FieldInitializer
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = ['Group']


class __Group__(FieldInitializer):

    elementals = ElementalListField(fdef_name='__create_elementals__', doc='List of ports to be added to the cell instance.')

    def __create_elementals__(self, elems):
        el = self.create_elementals(elems)
        if hasattr(self, 'disable_edge_ports'):
            if self.disable_edge_ports:
                for e in el:
                    if isinstance(e, spira.Polygon):
                        e.disable_edge_ports = True
        return el

    def create_elementals(self, elems):
        return elems

    def append(self, elemental):
        el = self.elementals
        el.append(elemental)
        self.elementals = el

    def extend(self, elems):
        from spira.yevon.gdsii.group import Group
        el = self.elementals
        if isinstance(elems, Group):
            el.extend(elems.elemetals)
        else:
            el.extend(elems)
        self.elementals = el  

    def __iadd__(self, elemental):
        from spira.yevon.geometry.ports.base import __Port__
        """ Add elemental and reduce the class to a simple compound elementals. """
        if isinstance(elemental, (list, spira.ElementalList)):
            self.extend(elemental)
        elif isinstance(elemental, __Elemental__):
            self.append(elemental)
        elif elemental is None:
            return self
        elif issubclass(type(elemental), __Port__):
            self.ports += elemental
        else:
            raise TypeError("Invalid type " + str(type(elemental)) + " in __Group__.__iadd__().")
        return self

    def flatten(self, level=-1):
        self.elementals = self.elementals.flat_copy(level=level)
        return self

    def __iter__(self):
        return self.elementals.__iter__()

    def is_empty(self):
        return self.elementals.is_empty()

    @property
    def bbox_info(self):
        return self.elementals.bbox_info
    

class Group(__Group__, __Elemental__):

    def __init__(self, transformation=None, **kwargs):
        super().__init__(transformation=transformation, **kwargs)
    
    def flat_copy(self, level=-1):
        if not level == 0:
            return self.elementals.flat_copy(level).transform(self.transformation)
        else:
            return spira.ElementalList(self.elementals)

    def expand_transform(self):
        if not self.transformation.is_identity():
            self.elementals.transform(self.transformation)
            self.transformation = None  

    def __eq__(self, other):
            return (self.elementals == other.elementals) and (self.transformation == other.transformation)


           