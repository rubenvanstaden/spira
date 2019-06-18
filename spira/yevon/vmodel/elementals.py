from spira.yevon.gdsii.cell import Cell
from spira.yevon.aspects.base import __Aspects__
from spira.yevon.gdsii.elem_list import ElementalListField, ElementalList
from spira.yevon.filters.layer_filter import LayerFilterAllow
from spira.yevon.gdsii.polygon import Polygon
from spira.yevon.gdsii.polygon_group import PolygonGroup
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


def get_process_polygons(elementals, operation='or'):
    elems = ElementalList()
    for process in RDD.VMODEL.PROCESS_FLOW.active_processes:
        for layer in RDD.get_physical_layers_by_process(processes=process):
            LF = LayerFilterAllow(layers=[layer])
            el = LF(elementals.polygons)
            if operation == 'or':
                pg = PolygonGroup(elementals=el, layer=layer).merge
            elif operation == 'and':
                pg = PolygonGroup(elementals=el, layer=layer).intersect
            elems += pg
    return elems


class ElementalsForModelling(__Aspects__):
    """
    Convert the cell elementals into a new set
    of elements for every active process.
    """

    process_elementals = ElementalListField()
    overlap_elementals = ElementalListField()

    def create_process_elementals(self, elems):
        elems += get_process_polygons(self.elementals, 'or')
        return elems

    def create_overlap_elementals(self, elems):
        elems += get_process_polygons(self.elementals, 'and')
        return elems

    def write_gdsii_mask(self, **kwargs):
        elems = ElementalList()
        for pg in self.process_elementals:
            for e in pg.elementals:
                elems += e
        D = Cell(name=self.name + '_VMODEL', elementals=elems)
        D.gdsii_output()


Cell.mixin(ElementalsForModelling)



