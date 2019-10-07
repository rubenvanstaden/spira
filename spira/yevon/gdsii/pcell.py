from spira.yevon.gdsii.cell import Cell
from spira.yevon.utils import netlist
from spira.yevon.gdsii.elem_list import ElementListParameter, ElementList
from spira.yevon.geometry.ports import PortList
from spira.core.parameters.descriptor import Parameter
from copy import deepcopy

from spira.core.parameters.variables import *
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = ['PCell', 'Device', 'Circuit']


class PCell(Cell):
    """  """

    pcell = BoolParameter(default=True)
    routes = ElementListParameter(doc='List of `Route` elements connected to the cell.')
    structures = ElementListParameter(doc='List of cell structures that coalesces the top-level cell.')
    extract_netlist = Parameter(fdef_name='create_extract_netlist')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Device(PCell):
    """  """

    # lcar = NumberParameter(default=RDD.PCELL.LCAR_DEVICE)
    lcar = NumberParameter(default=1)

    def __init__(self, pcell=True, **kwargs):
        super().__init__(**kwargs)
        self.pcell = pcell

    def __repr__(self):
        class_string = "[SPiRA: Device(\'{}\')] (elements {}, ports {})"
        return class_string.format(self.name, self.elements.__len__(), self.ports.__len__())

    def __str__(self):
        return self.__repr__()

    def __create_elements__(self, elems):

        elems = self.create_elements(elems)
        elems += self.structures
        elems += self.routes

        if self.pcell is True:
            D = Cell(elements=elems.flat_copy())
            elems = RDD.FILTERS.PCELL.DEVICE(D).elements

        return elems

    def create_netlist(self):

        print('[*] Generating device netlist')

        net = super().create_netlist()
        # net = netlist.combine_net_nodes(net=net, algorithm=['d2d'])
        # net = netlist.combine_net_nodes(net=net, algorithm=['s2s'])

        return net

    def create_extract_netlist(self):
        return self.netlist


class Circuit(PCell):
    """  """

    corners = StringParameter(default='miter', doc='Define the type of path joins.')
    bend_radius = NumberParameter(allow_none=True, default=None, doc='Bend radius of path joins.')

    # lcar = NumberParameter(default=RDD.LCAR_CIRCUIT)
    lcar = NumberParameter(default=100)

    def __repr__(self):
        class_string = "[SPiRA: Circuit(\'{}\')] (elements {}, ports {})"
        return class_string.format(self.name, self.elements.__len__(), self.ports.__len__())

    def __str__(self):
        return self.__repr__()

    def __create_elements__(self, elems):
        from spira.yevon.gdsii.sref import SRef

        elems = self.create_elements(elems)
        elems += self.structures
        elems += self.routes

        def wrap_references(cell, c2dmap, devices):
            for e in cell.elements.sref:
                if isinstance(e.reference, Device):
                    D = deepcopy(e.reference)
                    D.elements.transform(e.transformation)
                    D.ports.transform(e.transformation)
                    devices[D] = D.elements

                    D.elements = ElementList()
                    S = deepcopy(e)
                    S.reference = D
                    c2dmap[cell] += S
                else:
                    S = deepcopy(e)
                    S.reference = c2dmap[e.reference]
                    c2dmap[cell] += S

        if self.pcell is True:

            ex_elems = elems.expand_transform()

            C = Cell(elements=ex_elems)

            c2dmap, devices = {}, {}

            for cell in C.dependencies():
                D = Cell(name=cell.name,
                    elements=deepcopy(cell.elements.polygons),
                    ports=deepcopy(cell.ports))
                c2dmap.update({cell: D})

            for cell in C.dependencies():
                wrap_references(cell, c2dmap, devices)

            D = c2dmap[C]
            
            # for e in D.elements.polygons:
            #     if e.layer.purpose.symbol == 'METAL':
            #         e.layer.purpose = RDD.PURPOSE.CIRCUIT_METAL

            F = RDD.FILTERS.PCELL.CIRCUIT

            # from spira.yevon import filters
            # F = filters.ToggledCompositeFilter(filters=[])
            # F += filters.ProcessBooleanFilter(name='boolean')

            Df = F(D)

            # NOTE: Add devices back into the circuit.
            for d in Df.dependencies():
                if d in devices.keys():
                    d.elements = devices[d]
                    # for e in d.elements.polygons:
                    #     if e.layer.purpose.symbol == 'METAL':
                    #         e.layer.purpose = RDD.PURPOSE.DEVICE_METAL

            elems = Df.elements

        return elems

    def create_netlist(self):
        from spira.yevon import filters

        print('[*] Generating circuit netlist')

        net = super().create_netlist()
        net = netlist.combine_net_nodes(net=net, algorithm=['d2d'])
        net = netlist.combine_net_nodes(net=net, algorithm=['s2s'])

        return net

    def create_extract_netlist(self):

        net = self.netlist

        # net = net.convert_pins()
        # net = net.del_branch_attrs()

        # from spira.yevon import filters
        # f = filters.ToggledCompositeFilter(filters=[])
        # f += filters.NetBranchCircuitFilter()
        # f += filters.NetDummyFilter()
        # f += filters.NetBranchCircuitFilter()

        # net = f(net)[0]

        # from spira.yevon.utils import netlist
        # net = netlist.combine_net_nodes(net=net, algorithm=['b2b'])

        return net

