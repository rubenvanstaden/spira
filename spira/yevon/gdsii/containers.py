from spira.yevon.gdsii.cell import Cell, CellParameter
from spira.yevon.gdsii.sref import SRef
from copy import deepcopy
from spira.core.parameters.descriptor import Parameter
from spira.yevon.gdsii.elem_list import ElementListParameter


class __CellContainer__(Cell):

    cell = CellParameter(allow_none=True, default=None)

    def create_elements(self, elems):
        elems += SRef(reference=self.cell)
        return elems

#     def __cell_swapper__(self, new_cell, c, c2dmap):
#         for e in c.elements.sref:
#             S = deepcopy(e)
#             if e.reference in c2dmap.keys():
#                 S.ref = c2dmap[e.reference]
#                 new_cell += S

