from spira.yevon.gdsii.cell import Cell
from spira.yevon.utils import netlist
from spira.yevon.gdsii.elem_list import ElementListParameter

from spira.core.parameters.variables import *
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = ['PCell', 'Device', 'Circuit']


class PCell(Cell):
    """  """

    pcell = BoolParameter(default=True)
    routes = ElementListParameter(doc='List of `Route` elements connected to the cell.')
    structures = ElementListParameter(doc='List of cell structures that coalesces the top-level cell.')


class Device(PCell):
    """  """

    # lcar = NumberParameter(default=RDD.PCELLS.LCAR_DEVICE)
    # lcar = NumberParameter(default=0.5)
    lcar = NumberParameter(default=10)
    # lcar = NumberParameter(default=100)

    def __init__(self, pcell=True, **kwargs):
        super().__init__(**kwargs)
        self.pcell = pcell

    def __repr__(self):
        class_string = "[SPiRA: Device(\'{}\')] (elements {}, ports {})"
        return class_string.format(self.name, self.elements.__len__(), self.ports.__len__())

    def __str__(self):
        return self.__repr__()

    def __create_elements__(self, elems):

        F = RDD.PCELLS.FILTERS
        # F['boolean'] = False
        # F['simplify'] = False
        F['via_contact'] = False
        # F['metal_connect'] = False

        elems = self.create_elements(elems)
        elems += self.structures
        elems += self.routes

        if self.pcell is True:
            D = Cell(elements=elems.flat_copy())
            elems = F(D).elements

        return elems

    def create_netlist(self):
        print('Device netlist')
        net = super().create_netlist()
        # net = netlist.combine_net_nodes(net=net, algorithm=['d2d', 's2s'])

        # net = self.nets(lcar=self.lcar).disjoint(connect=True)
        # import networkx as nx
        # from spira.yevon.geometry.nets.net import Net
        # graphs = list(nx.connected_component_subgraphs(net.g))
        # net = Net(g=nx.disjoint_union_all(graphs))
        return net


class Circuit(PCell):
    """  """

    corners = StringParameter(default='miter', doc='Define the type of path joins.')
    bend_radius = NumberParameter(allow_none=True, default=None, doc='Bend radius of path joins.')

    lcar = NumberParameter(default=RDD.PCELLS.LCAR_CIRCUIT)
    # lcar = NumberParameter(default=10)
    # lcar = NumberParameter(default=1)

    def __repr__(self):
        class_string = "[SPiRA: Circuit(\'{}\')] (elements {}, ports {})"
        return class_string.format(self.name, self.elements.__len__(), self.ports.__len__())

    def __str__(self):
        return self.__repr__()

    def __create_elements__(self, elems):

        F = RDD.PCELLS.FILTERS
        # F['boolean'] = False
        # F['simplify'] = False
        F['via_contact'] = False
        # F['metal_connect'] = False

        elems = self.create_elements(elems)
        elems += self.structures
        elems += self.routes

        if self.pcell is True:
            D = Cell(elements=elems).expand_flat_copy(exclude_devices=True)
            elems = F(D).elements

        return elems

    def create_netlist(self):
        print('Circuit netlist')
        net = super().create_netlist()
        net = netlist.combine_net_nodes(net=net, algorithm=['d2d'])
        # net = netlist.combine_net_nodes(net=net, algorithm=['d2d', 's2s'])
        return net



