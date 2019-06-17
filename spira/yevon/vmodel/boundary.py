from spira.yevon.gdsii.cell import Cell
from spira.yevon.aspects.base import __Aspects__
from spira.yevon.gdsii.elem_list import ElementalListField, ElementalList
from spira.yevon.gdsii.polygon import Polygon
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


def reference_metal_blocks(S):
    from copy import deepcopy
    elems = ElementalList()
    for layer in RDD.get_physical_layers_by_purpose(purposes=['METAL', 'GND']):
        layer = deepcopy(layer)
        if S.ref.is_layer_in_cell(layer):
            bbox_shape = S.bbox_info.bounding_box()
            layer.purpose = RDD.PURPOSE.BOUNDARY_BOX
            elems += Polygon(shape=bbox_shape, layer=layer)
    return elems


class ReferenceBlocks(__Aspects__):
    """ Create a boundary block around the cell 
    references in the current cell structure. """

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


Cell.mixin(ReferenceBlocks)



