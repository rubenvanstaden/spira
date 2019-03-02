from spira.gdsii.cell import Cell
from spira.gdsii.elemental.sref import SRef
from spira import param
from copy import deepcopy


class __CellContainer__(Cell):

    cell = param.CellField()

    def create_elementals(self, elems):
        elems += SRef(structure=self.cell)
        return elems


class __NetContainer__(__CellContainer__):
    netlist = param.DataField(fdef_name='create_netlist')
    nets = param.ElementalListField(fdef_name='create_nets')

    def create_netlist(self):
        return None

    def create_nets(self, nets):
        return nets


class __CircuitContainer__(__NetContainer__):
    """ Circuit topology description: routes, devcies and boudning boxes. """

    boxes = param.ElementalListField(fdef_name='create_boxes')
    routes = param.ElementalListField(fdef_name='create_routes')
    structures = param.ElementalListField(fdef_name='create_structures')
    devices = param.ElementalListField(fdef_name='create_devices')
    
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

