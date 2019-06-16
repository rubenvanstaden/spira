from spira.yevon.gdsii.cell import Cell
from spira.yevon.structure.containers import __CellContainer__
from spira.yevon.utils import clipping
from spira.yevon.utils import netlist
from spira.yevon.process.gdsii_layer import LayerField
from spira.core.parameters.descriptor import DataField

from spira.yevon.utils.elementals import *
from spira.core.parameters.variables import *
from spira.yevon.filters.boolean_filter import *

from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = ['PCell', 'Device', 'Circuit']


class PCell(Cell):
    """  """

    pcell = BoolField(default=True)

    def __create_elementals__(self, elems):

        if self.pcell is False:
            elems = super().__create_elementals__(elems)
        else:
            el = self.create_elementals(elems)
            D = Cell(elementals=el.flat_copy())
            F = ProcessBooleanFilter()
            F += SimplifyFilter()
            F += ViaConnectFilter()
            # F += MetalConnectFilter()
            elems = F(D).elementals

        return elems


# from spira.yevon.utils.elementals import get_generated_elementals
# def label_vias(symbol, cell, process_cell, contact_cell, mapping):
#     output_elems = get_generated_elementals(elements=cell.elementals, mapping=mapping)

#     # for i, e in enumerate(output_elems):
#     #     if e.purpose == 'METAL':
#     #         process_cell += e
#     #     else:
#     #         contact_cell += e

#     # ll = []
#     # for e in cell.elementals:
#     #     # if e.purpose != 'METAL':
#     #     if e not in output_elems:
#     #         ll.append(e)
#     #     else:
#     #         print('YES')

#     # cell.elementals.clear()
#     # for e in ll:
#     #     cell += e

#     # for e in output_elems:
#     #     if e.purpose == 'METAL':
#     #         cell.elementals += e

#     for e in output_elems:
#         if e.purpose == 'METAL':
#             process_cell += e
#         else:
#             contact_cell += e

#     return cell


class Device(PCell):
    
    bot_layer = LayerField()
    top_layer = LayerField()
    via_layer = LayerField()

    lcar = NumberField(default=1)

    # clayer_map = DictField(fdef_name='create_contructor_layer_map')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def __repr__(self):
        class_string = "[SPiRA: Device(\'{}\')] (elementals {}, ports {})"
        return class_string.format(self.name, self.elementals.__len__(), self.ports.__len__())

    def __str__(self):
        return self.__repr__()

    # def create_contructor_layer_map(self):
    #     cl1 = self.bot_layer & self.top_layer & self.via_layer
    #     cl2 = self.bot_layer ^ cl1
    #     cl3 = self.top_layer ^ cl1
    #     via = RDD.PLAYER[self.via_layer.process.symbol]
    #     mapping = {
    #         cl1 : RDD.PLAYER[self.via_layer.process.symbol].VIA,
    #         cl2 : RDD.PLAYER[self.bot_layer.process.symbol].METAL,
    #         cl3 : RDD.PLAYER[self.top_layer.process.symbol].METAL
    #     }
    #     return mapping

    # def create_ports(self, ports):

    #     # mask_cell = Cell(name='MaskCell')
    #     # process_cell = Cell(name='ProcessLayerCell')
    #     # contact_cell = Cell(name='ContactLayerCell')

    #     # for k1 in RDD.VIAS.keys:
    #     #     V = RDD.VIAS[k1].PCELLS.DEFAULT(
    #     #         bot_layer=RDD.VIAS[k1].LAYER_STACK['BOT_LAYER'],
    #     #         top_layer=RDD.VIAS[k1].LAYER_STACK['TOP_LAYER'],
    #     #         via_layer=RDD.VIAS[k1].LAYER_STACK['VIA_LAYER'],
    #     #     )
    #     #     j1 = label_vias(
    #     #         symbol=k1,
    #     #         cell=j1,
    #     #         process_cell=process_cell,
    #     #         contact_cell=contact_cell,
    #     #         mapping=V.clayer_map
    #     #     )
    
    #     # for e in process_cell.elementals:
    #     #     mask_cell += e
    #     # mask_cell += spira.SRef(reference=contact_cell)

    #     return ports


class Circuit(PCell):

    lcar = NumberField(default=1)

    def create_netlist(self):
        net = self.nets(lcar=1).disjoint()
        # net = netlist.combine_net_nodes(net=net, algorithm=['d2d', 's2s'])
        return net



