from spira.gdsii.cell import Cell
from spira.gdsii.elemental.sref import SRef
from spira import param


class __CellContainer__(Cell):

    cell = param.CellField()
    # boxes = param.ElementalListField(fdef_name='create_boxes')

    # def create_boxes(self, boxes):
    #     return boxes

    def create_elementals(self, elems):
        elems += SRef(structure=self.cell)
        return elems


class __CellContainerWithTerminals__(__CellContainer__):

    # terms = param.TerminalListField()

    def create_terminals(self, terms):
        return terms


class __CellContainerWithPorts__(__CellContainer__):

    # ports = param.PortListField()

    def create_ports(self, ports):
        return ports


class __CellContainerWithPlanes__(__CellContainer__):
    """ Extending a Cell with Ground/Sky Planes. """

    # planes = param.PlaneListField()

    def create_planes(self, planes):
        return planes


class __ElementalContainer__(Cell):

    received_elementals = param.ElementalListField()

    def create_elementals(self, elems):
        return elems

