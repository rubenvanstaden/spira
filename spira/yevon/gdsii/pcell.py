from spira.yevon.gdsii.cell import Cell
from spira.yevon.utils import netlist
from spira.yevon.gdsii.elem_list import ElementalListField

from spira.core.parameters.variables import *
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = ['PCell', 'Device', 'Circuit']


class PCell(Cell):
    """  """

    pcell = BoolField(default=True)
    routes = ElementalListField(doc='List of `Route` elementals connected to the cell.')
    structures = ElementalListField(doc='List of cell structures that coalesces the top-level cell.')

    def __create_elementals__(self, elems):

        F = RDD.PCELLS.FILTERS
        F['simplify'] = False
        F['via_contact'] = False
        # F['metal_connect'] = False

        elems = self.create_elementals(elems)
        elems += self.structures
        elems += self.routes

        if self.pcell is True:
            D = Cell(elementals=elems).expand_flat_copy(exclude_devices=True)
            # D = Cell(elementals=el.flat_copy())
            elems = F(D).elementals

        return elems


class Device(PCell):

    lcar = NumberField(default=RDD.PCELLS.LCAR_DEVICE)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def __repr__(self):
        class_string = "[SPiRA: Device(\'{}\')] (elementals {}, ports {})"
        return class_string.format(self.name, self.elementals.__len__(), self.ports.__len__())

    def __str__(self):
        return self.__repr__()


class Circuit(PCell):
    """  """

    lcar = NumberField(default=RDD.PCELLS.LCAR_CIRCUIT)

    def create_netlist(self):
        net = self.nets(lcar=self.lcar).disjoint()
        # net = netlist.combine_net_nodes(net=net, algorithm=['d2d', 's2s'])
        return net



