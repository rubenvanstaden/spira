import spira.all as spira
from spira.yevon.gdsii.base import __Elemental__
from spira.yevon.gdsii.elem_list import ElementalListField
from spira.core.parameters.initializer import FieldInitializer


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

    # elementals = ElementalListField(fdef_name='create_elementals', doc='List of elementals to be added to the cell instance.')

    # def create_elementals(self, elems):
    #     result = spira.ElementalList()
    #     return result

    # FIXME: For some reason this interferes with the spira.Cell commit.
    # def commit_to_gdspy(self, cell, transformation=None):
    #     for e in self.elementals:
    #         e.commit_to_gdspy(cell=cell, transformation=transformation)
    #     return cell

    # def __eq__(self,other):
    #     if other == None:
    #         return False
    #     if not isinstance(other, spira.Cell):
    #         return False
    #     self_el = self.elementals
    #     other_el = other.elementals
    #     if len(self_el) != len(other_el):
    #         return False
    #     for e1, e2 in zip(self_el, other_el):
    #         if (e1 != e2):
    #             return False
    #     return True

    # def __ne__(self, other):
    #     return not self.__eq__(other)

    # def generate_physical_polygons(self, pl):
    #     elems = spira.ElementalList()
    #     R = self.cell.elementals.flat_copy()
    #     Rm = R.get_polygons(layer=pl.layer)
    #     for i, e in enumerate(Rm):
    #         if len(e.polygons[0]) == 4:
    #             alias = 'devices_box_{}_{}_{}'.format(pl.layer.number, self.cell.node_id, i)
    #             poly = spira.Polygons(shape=e.polygons)
    #             elems += pc.Box(name=alias, player=pl, center=poly.center, w=poly.dx, h=poly.dy, level=self.level)
    #         else:
    #             alias = 'ply_{}_{}_{}'.format(pl.layer.number, self.cell.node_id, i)
    #             elems += pc.Polygon(name=alias, player=pl, points=e.polygons, level=self.level)
    #     return elems

    # def create_metals(self, elems):
    #     for player in RDD.PLAYER.get_physical_layers(purposes='METAL'):
    #         for e in self.generate_physical_polygons(player):
    #             elems += e
    #     return elems

    # def create_contacts(self, elems):
    #     for player in RDD.PLAYER.get_physical_layers(purposes=['VIA', 'JJ']):
    #         for e in self.generate_physical_polygons(player):
    #             elems += e
    #     return elem


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


           