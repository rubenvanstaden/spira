from spira.yevon.gdsii.cell import Cell
from spira.yevon.structure.containers import __CellContainer__
from spira.yevon.utils import clipping
from spira.yevon.utils import netlist
from spira.yevon.process.gdsii_layer import LayerField
from spira.core.parameters.descriptor import DataField
from spira.yevon.gdsii.elem_list import ElementalListField

from spira.yevon.utils.elementals import *
from spira.core.parameters.variables import *
from spira.yevon.filters.boolean_filter import *

from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = ['PCell', 'Device', 'Circuit']


class PCell(Cell):
    """  """

    pcell = BoolField(default=True)

    routes = ElementalListField()
    structures = ElementalListField()

    def __create_elementals__(self, elems):

        if self.pcell is False:
            el = super().__create_elementals__(elems)
            el += self.routes
            el += self.structures
            elems = el
        else:
            el = self.create_elementals(elems)
            el += self.routes
            el += self.structures
            D = Cell(elementals=el.flat_copy())
            F = ProcessBooleanFilter()
            # F += SimplifyFilter()
            # F += ViaConnectFilter()
            # F += MetalConnectFilter()
            elems = F(D).elementals

        return elems


class Device(PCell):
    
    bot_layer = LayerField()
    top_layer = LayerField()
    via_layer = LayerField()

    lcar = NumberField(default=1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def __repr__(self):
        class_string = "[SPiRA: Device(\'{}\')] (elementals {}, ports {})"
        return class_string.format(self.name, self.elementals.__len__(), self.ports.__len__())

    def __str__(self):
        return self.__repr__()


class Circuit(PCell):
    """  """

    lcar = NumberField(default=1)

    def create_netlist(self):
        net = self.nets(lcar=self.lcar).disjoint()
        # net = netlist.combine_net_nodes(net=net, algorithm=['d2d', 's2s'])
        return net



