from spira.yevon.gdsii.cell import Cell
from spira.yevon.aspects.base import __Aspects__
from spira.yevon.gdsii.elem_list import ElementalListField, ElementalList
from spira.yevon.filters.layer_filter import LayerFilterAllow
from spira.yevon.utils import clipping
from spira.yevon.gdsii.polygon import Polygon, PolygonGroup
from copy import deepcopy
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


def reference_metal_blocks(S):
    elems = ElementalList()
    for layer in RDD.get_physical_layers_by_purpose(purposes=['METAL', 'GND']):
        layer = deepcopy(layer)
        if S.ref.is_layer_in_cell(layer):
            bbox_shape = S.bbox_info.bounding_box()
            layer.purpose = RDD.PURPOSE.BOUNDARY_BOX
            elems += Polygon(shape=bbox_shape, layer=layer)
    return elems


def get_process_elementals(elems):
    el = ElementalList()
    for process in RDD.VMODEL.PROCESS_FLOW.active_processes:
        for layer in RDD.get_physical_layers_by_process(processes=process):
            LF = LayerFilterAllow(layers=[layer])
            el += PolygonGroup(elementals=LF(elems.polygons), layer=layer).merge
    return el


class ElementalsForModelling(__Aspects__):
    """
    Convert the cell elementals into a new set
    of elements for every active process.
    """

    process_elementals = ElementalListField()

    def create_process_elementals(self, elems):
        return get_process_elementals(self.elementals)

    @property
    def pcell(self):
        from spira.yevon.filters.boolean_filter import ProcessBooleanFilter
        D = self.expand_flat_copy()
        # D = self.flat_copy()
        F = ProcessBooleanFilter()
        D = F(D)

        # elems = ElementalList()
        # for pg in self.process_elementals:
        #     for e in pg.elementals:
        #         D += e
        # for e in self.elementals.sref:
        #     D += e
        # for e in self.elementals.labels:
        #     D += e
        # D = Cell(
        # D = self.__class__(
        #     name=self.name + '_PCELL', 
        #     elementals=elems, 
        #     ports=self.ports
        # )

        return D

    def write_gdsii_mask(self, **kwargs):
        elems = ElementalList()
        for pg in self.process_elementals:
            for e in pg.elementals:
                elems += e
        D = Cell(name=self.name + '_VMODEL', elementals=elems)
        D.gdsii_output()


class ReferenceBlocks(__Aspects__):

    block_elementals = ElementalListField()

    def create_block_elementals(self, elems):
        for e in self.elementals.sref:
            for layer in RDD.get_physical_layers_by_purpose(purposes=['METAL', 'GND']):
                if e.ref.is_layer_in_cell(layer):
                    bbox_shape = e.bbox_info.bounding_box()
                    elems += Polygon(shape=bbox_shape, layer=layer)
        return elems

    def write_gdsii_blocks(self, **kwargs):
        D = Cell(name=self.name + '_BLOCKS', elementals=self.block_elementals)
        D.gdsii_output()


Cell.mixin(ElementalsForModelling)
Cell.mixin(ReferenceBlocks)



