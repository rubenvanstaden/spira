from spira.yevon.gdsii.cell import Cell
from spira.yevon.aspects.base import __Aspects__
from spira.yevon.gdsii.elem_list import ElementListParameter, ElementList
from spira.yevon.filters.layer_filter import LayerFilterAllow
from spira.yevon.gdsii.polygon import Polygon
from spira.yevon.gdsii.polygon_group import PolygonGroup
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


def get_process_polygons(elements, operation='or'):
    elems = ElementList()
    for process in RDD.VMODEL.PROCESS_FLOW.active_processes:
        for layer in RDD.get_physical_layers_by_process(processes=process):
            LF = LayerFilterAllow(layers=[layer])
            el = LF(elements.polygons)
            if operation == 'or':
                pg = PolygonGroup(elements=el, layer=layer).merge
            elif operation == 'and':
                pg = PolygonGroup(elements=el, layer=layer).intersect
            elems += pg
    return elems


class DerivedElements(__Aspects__):
    """ Convert the cell elements into a new set
    of elements for every active process. """

    derived_merged_elements = ElementListParameter()
    derived_overlap_elements = ElementListParameter()

    def create_derived_merged_elements(self, elems):
        elems += get_process_polygons(self.elements, 'or')
        return elems

    def create_derived_overlap_elements(self, elems):
        elems += get_process_polygons(self.elements, 'and')
        return elems

    def gdsii_output_derived(self, derived_type, **kwargs):
        elems = ElementList()
        for pg in self.derived_merged_elements:
            for e in pg.elements:
                elems += e
        name = '{}_{}'.format(self.name, derived_type)
        D = Cell(name=name, elements=elems)
        D.gdsii_output(file_name=derived_type)


Cell.mixin(DerivedElements)



