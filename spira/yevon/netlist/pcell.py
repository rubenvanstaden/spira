import spira.all as spira
from spira.yevon.gdsii.cell import Cell
from spira.yevon.gdsii.elem_list import ElementalListField
from spira.yevon.netlist.containers import __CellContainer__
from spira.yevon.utils.elementals import *
from spira.core.parameters.variables import *
from spira.yevon.geometry.route import Route
from spira.yevon.properties.base import __Property__
from spira.yevon.utils import clipping


__all__ = ['PCell', 'Device', 'Circuit']


class PCell(__CellContainer__):
    """  """

    raw_version = BoolField(default=True)

    blocks = ElementalListField(fdef_name='create_blocks')
    routes = ElementalListField(fdef_name='create_routes')
    structures = ElementalListField(fdef_name='create_structures')

    def create_blocks(self, blocks):
        for e in self.structures:
            pass
        return blocks

    def create_structures(self, structs):
        if self.cell is not None:
            for S in self.cell.elementals:
                if isinstance(S, spira.SRef):
                    structs += S
        else:
            for e in self.create_elementals([]):
                if isinstance(e, spira.SRef):
                    if issubclass(type(e), (Device, Circuit)):
                        structs += e
        return structs

    def create_routes(self, routes):
        if self.cell is not None:
            r = Route(cell=self.cell)
            routes += spira.SRef(r)
        else:
            el = spira.ElementalList()
            elems = self.create_elementals(el)
            for e in elems:
                if isinstance(e, spira.SRef):
                    if issubclass(type(e.ref), Route):
                        routes += e
            metals = clipping.union_polygons(elems)
            R = Route(metals=metals)
            routes += spira.SRef(R)
        return routes

    # def create_metals(self, elems):
    #     R = self.routes.flat_copy()
    #     elems = convert_polygons_to_processlayers(R)
    #     return elems

    def __create_elementals__(self, elems):

        print('PCell __create_elementals__')

        # for e in self.structures:
        #     elems += e

        print('Adding routes...')
        for e in self.routes:
            elems += e

        return elems


class Device(PCell):
    pass


class Circuit(PCell):
    pass



