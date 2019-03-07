import spira
import numpy as np
from spira import param, shapes
from demo.pdks import ply
from spira.lpe.containers import __CellContainer__
from copy import copy, deepcopy

from spira.gdsii.utils import scale_polygon_down as spd
from spira.gdsii.utils import scale_polygon_up as spu
from spira.lpe.pcells import  __NetlistCell__
from demo.pdks.components.mitll.via import Via


RDD = spira.get_rule_deck()


class Mask(__NetlistCell__):
    """  """

    def create_elementals(self, elems):
        elems = super().create_elementals(elems)

        Ds = spira.Cell(name='Structures')
        for e in self.cell.structures:
            Ds += e

        Dr = spira.Cell(name='Routes')
        for e in self.cell.routes:
            Dr += e

        elems += spira.SRef(Ds)
        elems += spira.SRef(Dr)

        return elems

    def create_nets(self, nets):

        print('[*] Connecting Circuit and Device nets')

        # g = deepcopy(self.cell.netlist)
        g = self.cell.netlist

        reference_nodes = {}
        neighbour_nodes = {}
        for S in self.cell.structures:

            print(S)

            if not issubclass(type(S.ref), Via):
                neighbour_nodes[S.node_id] = []
                for n in g.nodes():
                    if 'device' in g.node[n]:
                        D = g.node[n]['device']
                        if isinstance(D, spira.SRef):
                            if D.node_id == S.node_id:
                                nn = [i for i in g[n]]
                                neighbour_nodes[S.node_id].extend(nn)

                gs = S.netlist

                struct_nodes = {}
                for n in neighbour_nodes[S.node_id]:
                    if 'branch' in g.node[n]:
                        for m in gs.nodes:
                            if 'connect' in gs.node[m]:
                                for i, R in enumerate(gs.node[m]['connect']):
                                    print(i, R[0])
                                    if g.node[n]['branch'].route == R[0]:
                                        uid = '{}_{}_{}'.format(i, n, S.midpoint)
                                        if n in reference_nodes.keys():
                                            reference_nodes[n].append(uid)
                                        else:
                                            reference_nodes[n] = [uid]
                                        if m in struct_nodes.keys():
                                            struct_nodes[m].append(uid)
                                        else:
                                            struct_nodes[m] = [uid]
    
                for m, connections in struct_nodes.items():
                    gs.node[m]['connect'] = []
                    for v in connections:
                        s_copy = gs.node[m]['device'].modified_copy(node_id=v)
                        gs.node[m]['device'] = s_copy
                        gs.node[m]['connect'].append(s_copy)

                nets += gs

        for n, structures in reference_nodes.items():
            g.node[n]['connected_structures'] = []
            for v in structures:
                b = g.node[n]['branch']
                value = spira.Label(
                    position=b.position,
                    text=b.text,
                    route=b.route,
                    gdslayer=b.gdslayer,
                    color=b.color,
                    node_id=v
                )
                g.node[n]['branch'] = value
                g.node[n]['connected_structures'].append(value)

        nets += g

        return nets

    def create_netlist(self):

        self.g = self.merge

        for r in self.g.nodes(data='connected_structures'):
            if r[1] is not None:
                if isinstance(r[1], list):
                    for c1 in r[1]:
                        for d in self.g.nodes(data='connect'):
                            if d[1] is not None:
                                for c2 in d[1]:
                                    if c1.node_id == c2.node_id:
                                        self.g.add_edge(r[0], d[0])

        remove_nodes = []
        for S in self.cell.structures:
            if not issubclass(type(S.ref), Via):
                for n in self.g.nodes():
                    if 'device' in self.g.node[n]:
                        D = self.g.node[n]['device']
                        if isinstance(D, spira.SRef):
                            if D.node_id == S.node_id:
                                remove_nodes.append(n)

        self.g.remove_nodes_from(remove_nodes)

        self.plot_netlist(G=self.g, graphname=self.name, labeltext='id')

    def create_ports(self, ports):

        # ports = self.cell.ports

    #     # for D in self.cell.structures:
    #     #     for name, port in D.ports.items():
    #     #         if port.locked is False:
    #     #             # print(D)
    #     #             edgelayer = deepcopy(port.gdslayer)
    #     #             edgelayer.datatype = 100
    #     #             m_term = spira.Term(
    #     #                 name=port.name,
    #     #                 gdslayer=deepcopy(port.gdslayer),
    #     #                 midpoint=deepcopy(port.midpoint),
    #     #                 orientation=deepcopy(port.orientation),
    #     #                 reflection=port.reflection,
    #     #                 edgelayer=edgelayer,
    #     #                 width=port.width,
    #     #             )
    #     #             ports += m_term

    #     # for R in self.cell.routes:
    #     #     for name, port in R.ports.items():
    #     #         if port.locked is False:
    #     #             edgelayer = deepcopy(port.gdslayer)
    #     #             edgelayer.datatype = 101
    #     #             m_term = spira.Term(
    #     #                 name=port.name,
    #     #                 gdslayer=deepcopy(port.gdslayer),
    #     #                 midpoint=deepcopy(port.midpoint),
    #     #                 orientation=deepcopy(port.orientation),
    #     #                 reflection=port.reflection,
    #     #                 edgelayer=edgelayer,
    #     #                 width=port.width,
    #     #             )
    #     #             ports += m_term

        return ports


