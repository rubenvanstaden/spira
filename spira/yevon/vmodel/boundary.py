from spira.yevon.gdsii.cell import Cell
from spira.yevon.aspects.base import __Aspects__
from spira.yevon.gdsii.elem_list import ElementListParameter, ElementList
from spira.yevon.gdsii.polygon import Polygon
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


def reference_metal_blocks(S):
    from copy import deepcopy
    elems = ElementList()
    for layer in RDD.get_physical_layers_by_purpose(purposes=['METAL', 'GND']):
        layer = deepcopy(layer)
        if S.reference.is_layer_in_cell(layer):
            bbox_shape = S.bbox_info.bounding_box()
            layer.purpose = RDD.PURPOSE.BOUNDARY_BOX
            elems += Polygon(shape=bbox_shape, layer=layer)
    return elems


class ReferenceBlocks(__Aspects__):
    """ Create a boundary block around the cell 
    references in the current cell structure. """

    block_elements = ElementListParameter()

    def create_block_elements(self, elems):
        for e in self.elements.sref:
            for layer in RDD.get_physical_layers_by_purpose(purposes=['METAL', 'GND']):
                if e.reference.is_layer_in_cell(layer):
                    bbox_shape = e.bbox_info.bounding_box()
                    elems += Polygon(shape=bbox_shape, layer=layer)
        return elems

    def write_gdsii_blocks(self, **kwargs):
        D = Cell(name=self.name + '_BLOCKS', elements=self.block_elements)
        D.gdsii_output()


Cell.mixin(ReferenceBlocks)



