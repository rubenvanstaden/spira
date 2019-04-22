from spira.yevon.gdsii.cell import Cell, CellField
from spira.yevon.gdsii.sref import SRef
from spira.core import param
from copy import deepcopy
from spira.core.descriptor import DataField
from spira.core.elem_list import ElementalListField


class __CellContainer__(Cell):

    cell = CellField(allow_none=True, default=None)

    def create_elementals(self, elems):
        elems += SRef(structure=self.cell)
        return elems


class __NetContainer__(__CellContainer__):
    netlist = DataField(fdef_name='create_netlist')
    nets = ElementalListField(fdef_name='create_nets')

    def create_netlist(self):
        return None

    def create_nets(self, nets):
        return nets


class __CircuitContainer__(__NetContainer__):
    """ Circuit topology description: routes, devcies and boudning boxes. """

    boxes = ElementalListField(fdef_name='create_boxes')
    devices = ElementalListField(fdef_name='create_devices')
    routes = ElementalListField(fdef_name='create_routes')
    structures = ElementalListField(fdef_name='create_structures')

    def create_structures(self, structs):
        return structs

    def create_routes(self, routes):
        return routes

    def create_devices(self, devices):
        return devices

    def create_boxes(self, boxes):
        return boxes

    def __cell_swapper__(self, new_cell, c, c2dmap):
        for e in c.elementals.sref:
            S = deepcopy(e)
            if e.ref in c2dmap.keys():
                S.ref = c2dmap[e.ref]
                new_cell += S

