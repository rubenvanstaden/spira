from spira.yevon.gdsii.cell import Cell, CellField
from spira.yevon.gdsii.sref import SRef
from copy import deepcopy
from spira.core.parameters.descriptor import DataField
from spira.yevon.gdsii.elem_list import ElementalListField


class __CellContainer__(Cell):

    cell = CellField(allow_none=True, default=None)

    def create_elementals(self, elems):
        elems += SRef(reference=self.cell)
        return elems

#     def __cell_swapper__(self, new_cell, c, c2dmap):
#         for e in c.elementals.sref:
#             S = deepcopy(e)
#             if e.ref in c2dmap.keys():
#                 S.ref = c2dmap[e.ref]
#                 new_cell += S

