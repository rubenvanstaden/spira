from spira.yevon.gdsii.cell import Cell
from spira.yevon.aspects.base import __Aspects__
from spira.yevon.gdsii.elem_list import ElementListParameter, ElementList
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


def get_process_polygons(elements, operation='or'):
    from spira.yevon.gdsii.polygon_group import PolygonGroup
    from spira.yevon.filters.layer_filter import LayerFilterAllow

    elems = ElementList()
    for process in RDD.VMODEL.PROCESS_FLOW.active_processes:
        for layer in RDD.get_physical_layers_by_process(processes=process):
            LF = LayerFilterAllow(layers=[layer])
            el = LF(elements.polygons)
            if operation == 'or':
                pg = PolygonGroup(elements=el, layer=layer).union
            elif operation == 'and':
                pg = PolygonGroup(elements=el, layer=layer).intersect
            elif operation == 'not':
                pg = PolygonGroup(elements=el, layer=layer).difference
            elems += pg
    return elems


class DerivedElements(__Aspects__):
    """ Convert the cell elements into a new set
    of elements for every active process. """

    derived_merged_elements = ElementListParameter()
    derived_overlap_elements = ElementListParameter()
    derived_diff_elements = ElementListParameter()

    def create_derived_merged_elements(self, elems):
        elems += get_process_polygons(self.elements, 'or')
        return elems

    def create_derived_overlap_elements(self, elems):
        elems += get_process_polygons(self.elements, 'and')
        return elems
        
    def create_derived_diff_elements(self, elems):
        elems += get_process_polygons(self.elements, 'not')
        return elems

    def view_derived_merged_elements(self, **kwargs):
        elems = ElementList()
        for pg in self.derived_merged_elements:
            for e in pg.elements:
                elems += e
        name = '{}_{}'.format(self.name, 'DERIVED_MERGED_ELEMENTS')
        D = Cell(name=name, elements=elems)
        D.gdsii_view()

    def view_derived_overlap_elements(self, **kwargs):
        elems = ElementList()
        for pg in self.derived_overlap_elements:
            for e in pg.elements:
                elems += e
        name = '{}_{}'.format(self.name, 'DERIVED_OVERLAP_ELEMENTS')
        D = Cell(name=name, elements=elems)
        D.gdsii_view()


Cell.mixin(DerivedElements)



