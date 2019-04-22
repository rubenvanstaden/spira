from spira.yevon.gdsii.cell import Cell
from spira.core.elem_list import ElementalListField


__all__ = ['PCell']


class PCell(Cell):
    """  """

    routes = ElementalListField(fdef_name='create_routes')
    structures = ElementalListField(fdef_name='create_structures')

    def create_structures(self, structs):
        return structs

    def create_routes(self, routes):
        return routes

    def create_elementals(self, elems):

        for e in self.structures:
            elems += e

        for e in self.routes:
            elems += e

        return elems




