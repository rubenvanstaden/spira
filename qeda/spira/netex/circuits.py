import spira
import time
import numpy as np
from core import param
from spira import shapes, pc
from spira.netex.containers import __CellContainer__, __NetContainer__, __CircuitContainer__
from spira.netex.net import Net
from copy import copy, deepcopy
from spira.netex.devices import Device
from spira.netex.structure import Structure

from spira.geometry.route.routing import Route
from spira.geometry.route.route_shaper import RouteSimple, RouteGeneral
from spira.netex.netlist import NetlistSimplifier
from spira.netex.structure import __NetlistCell__
from spira.netex.boxes import BoundingBox
from halo import Halo

import networkx as nx
from spira import utils
from spira.utils import boolean


RDD = spira.get_rule_deck()


class MetalNet(NetlistSimplifier):
    pass


class RouteToStructureConnector(__CircuitContainer__, Structure):
    """  """

    def create_contacts(self, boxes):
        start = time.time()
        # print('[*] Connecting routes with devices')
        self.unlock_ports()
        for D in self.structures:
            if isinstance(D, spira.SRef):
                B = BoundingBox(S=D)
                boxes += B
        end = time.time()
        # print('Block calculation time {}:'.format(end - start))
        return boxes

    def unlock_ports(self):
        for S in self.structures:
            print('\n----------- Main ----------------')
            print(S)
            print('----------- END ----------------\n')
            S.unlock_overlapping_ports(D=self, initial=True)

        # for D in self.structures:
        #     for S in self.structures:
        #         if id(S) != id(D):
        #             for R in S.ref.routes:
        #                 self.__unlock_device_edges__(R, D)

        # for D in self.structures:
        #     for R in self.routes:
        #         # self.__unlock_route_edges__(R, D)
        #         self.__unlock_device_edges__(R, D)

    # def __unlock_route_edges__(self, R, D):
    #     for M in D.ref.metals:
    #         M_ply = M.polygon
    #         M_ply.transform(D.tf)
    #         for key, port in R.instance_ports.items():
    #             for mp in M_ply.shape.points:
    #                 if port.encloses(mp):
    #                     R.port_locks[port.key] = False

    # def __unlock_device_edges__(self, R, D):

    #     def r_func(R, D):
    #         if issubclass(type(R), pc.ProcessLayer):
    #             pp = R
    #             R_ply = pp.polygon
    #             for key, port in D.instance_ports.items():
    #                 if isinstance(port, (spira.Term, spira.EdgeTerm)):
    #                     if port.gds_layer.number == pp.ps_layer.layer.number:
    #                         if port.edge.ply_area != 0:
    #                             if R_ply & port.edge:
    #                                 print('pppppppppppppppppppppp')
    #                                 route_key = (pp.node_id, pp.ps_layer.layer.number)
    #                                 D.port_connects[key] = route_key
    #                                 D.port_locks[key] = False
    #         else:
    #             for pp in R.ref.metals:
    #                 if isinstance(pp, pc.ProcessLayer):
    #                     R_ply = pp.polygon
    #                     for key, port in D.instance_ports.items():
    #                         if isinstance(port, (spira.Term, spira.EdgeTerm)):
    #                             if port.gds_layer.number == pp.ps_layer.layer.number:
    #                                 if port.edge.ply_area != 0:
    #                                     if R_ply & port.edge:
    #                                         route_key = (pp.node_id, pp.ps_layer.layer.number)
    #                                         D.port_connects[key] = route_key
    #                                         D.port_locks[key] = False

    #     if isinstance(R, spira.ElementList):
    #         for r in R:
    #             r_func(r, D)
    #     else:
    #         r_func(R, D)


class Circuit(RouteToStructureConnector):
    """ Deconstructs the different hierarchies in the cell. """

    __mixins__ = [NetlistSimplifier]

    algorithm = param.IntegerField(default=6)
    level = param.IntegerField(default=2)
    lcar = param.FloatField(default=10.0)

    def create_elementals(self, elems):

        # for e in self.routes:
        #     elems += e

        for e in self.structures:
            elems += e

        for e in self.route_layers:
            elems += e

        # for e in self.merged_layers:
        #     elems += e

        return elems

    # def create_ports(self, elems):
    #     self.unlock_ports()
    #     for D in self.structures:
    #         for name, port in D.instance_ports.items():
    #             if port.locked is False:
    #                 edgelayer = deepcopy(port.gds_layer)
    #                 edgelayer.datatype = 100
    #                 elems += port.modified_copy(edgelayer=edgelayer)
    #     for R in self.routes:
    #         for name, port in R.instance_ports.items():
    #             if port.locked is False:
    #                 edgelayer = deepcopy(port.gds_layer)
    #                 edgelayer.datatype = 101
    #                 elems += port.modified_copy(edgelayer=edgelayer)
    #     for p in self.ports:
    #         elems += p
    #     for p in self.terminals:
    #         elems += p
    #     return elem

    def create_primitives(self, elems):
        # self.unlock_ports()
        # for D in self.structures:
        #     for name, port in D.instance_ports.items():
        #         if port.locked is False:
        #             edgelayer = deepcopy(port.gds_layer)
        #             edgelayer.datatype = 100
        #             elems += port.modified_copy(edgelayer=edgelayer)
        # for R in self.routes:
        #     for name, port in R.instance_ports.items():
        #         if port.locked is False:
        #             edgelayer = deepcopy(port.gds_layer)
        #             edgelayer.datatype = 101
        #             elems += port.modified_copy(edgelayer=edgelayer)
        for p in self.ports:
            elems += p
        for p in self.terminals:
            elems += p
        return elems

    def create_structures(self, structs):
        if self.cell is not None:
            for S in self.cell.elementals:
                if isinstance(S, spira.SRef):
                    structs += S
        # else:
        #     for e in self.elementals.sref:
        #         if issubclass(type(e), (Device, Circuit)):
        #             structs += e
        return structs

    def create_routes(self, routes):
        if self.cell is not None:
            r = Route(cell=self.cell)
            routes += spira.SRef(r)
        # else:
        #     for e in self.elementals.sref:
        #         if issubclass(type(e.ref), Route):
        #             routes += e
        return routes

    def create_metals(self, elems):
        R = self.routes.flat_copy()
        B = self.contacts.flat_copy()
        for ps_layer in RDD.PLAYER.get_physical_layers(purposes='METAL'):
            Rm = R.get_polygons(layer=ps_layer.layer)
            Bm = B.get_polygons(layer=ps_layer.layer)
            for i, e in enumerate([*Rm, *Bm]):
                alias = 'ply_{}_{}_{}'.format(ps_layer.layer.number, self.__class__.__name__, i)
                elems += pc.Polygon(name=alias, ps_layer=ps_layer, points=e.polygons, level=self.level)
        return elems

    def create_terminals(self, ports):

        # FIXME!!! Needed for terminal detection in the Mesh.
        if self.cell is not None:
            cell = deepcopy(self.cell)
            flat_elems = cell.flat_copy()
            port_elems = flat_elems.get_polygons(layer=RDD.PURPOSE.TERM)
            label_elems = flat_elems.labels
            for port in port_elems:
                for label in label_elems:
                    lbls = label.text.split(' ')
                    s_p1, s_p2 = lbls[1], lbls[2]
                    p1, p2 = None, None
                    for m1 in RDD.PLAYER.get_physical_layers(purposes=['METAL', 'GND']):
                        if m1.layer.name == s_p1:
                            p1 = spira.Layer(name=lbls[0],
                                number=m1.layer.number,
                                datatype=RDD.GDSII.TEXT
                            )
                        if m1.layer.name == s_p2:
                            p2 = spira.Layer(name=lbls[0],
                                number=m1.layer.number,
                                datatype=RDD.GDSII.TEXT
                            )
                    if p1 and p2 :
                        for pts in port.polygons:
                            # if label.encloses(ply=port.polygons[0]):
                            if label.encloses(ply=pts):
                                ports += spira.Term(
                                    name=label.text,
                                    layer1=p1, layer2=p2,
                                    width=port.dx,
                                    midpoint=label.position
                                )

        return ports

    def create_nets(self, nets):

        # print('Generating circuit netlist')

        graphs = []
        for m in self.merged_layers:
            # graphs.append(m.graph)

            MNet = MetalNet()
            MNet.g = utils.nodes_combine(m.graph, algorithm='d2d')
            gm = MNet.generate_branches()
            gm = MNet.detect_dummy_nodes()
            gm = MNet.generate_branches()
            gm = utils.nodes_combine(gm, algorithm='b2b')
            graphs.append(gm)
            # graphs.append(MNet.g)

        g = nx.disjoint_union_all(graphs)

        # Required for connection between cell-to-cell.
        g = utils.nodes_combine(g, algorithm='d2d')

        nets += g




        reference_nodes = {}
        neighbour_nodes = {}
        for S in self.structures:

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
                    # Loop over all the subject device nodes.
                    for m in gs.nodes:
                        if 'connect' in gs.node[m]:
                            for i, R in enumerate(gs.node[m]['connect']):
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
                elif 'device' in g.node[n]:
                    print('DEVICE detected!!!')
                    print('subj: {}'.format(S))
                    print('obj: {}'.format(g.node[n]['device']))

                    D = g.node[n]['device']
                    obj_graph = D.netlist
                    
                    for no in obj_graph.nodes:
                        obj_id = obj_graph.node[no]['surface'].node_id
                        for m in gs.nodes:
                            if 'connect' in gs.node[m]:
                                for i, R in enumerate(gs.node[m]['connect']):
                                    subj_connect_id = R[1]
                                    print('YESSSSSSSSS')
                                    print(R)
                                    print(subj_connect_id)
                                    print(obj_id)
                                    print('')
                                    if subj_connect_id == obj_id:
                                        print('bwekjfwejfbewjkbwebfk')
                                        uid = '{}_{}_{}'.format(i, n, m, nn, S.midpoint)
                                        if n in reference_nodes.keys():
                                            reference_nodes[n].append(uid)
                                        else:
                                            reference_nodes[n] = [uid]
                                        if m in struct_nodes.keys():
                                            struct_nodes[m].append(uid)
                                        else:
                                            struct_nodes[m] = [uid]

                    # for node in list(gd.nodes(data='branch')):
                    #     if node[1] is not None:
                    #         nn = node[0]
                    #         for m in gs.nodes:
                    #             if 'connect' in gs.node[m]:
                    #                 for i, R in enumerate(gs.node[m]['connect']):
                    #                     # if gd.node[i]['branch'].route == R[0]:
                    #                     subj_route = R[1]
                    #                     obj_route = node[1].route
                    #                     print('YESSSSSSSSS')
                    #                     print(node[nn])
                    #                     print(R)
                    #                     print(subj_route)
                    #                     print(obj_route)
                    #                     print('')
                    #                     if subj_route == obj_route:
                    #                         print('bwekjfwejfbewjkbwebfk')
                    #                         uid = '{}_{}_{}'.format(i, n, m, nn, S.midpoint)
                    #                         if n in reference_nodes.keys():
                    #                             reference_nodes[n].append(uid)
                    #                         else:
                    #                             reference_nodes[n] = [uid]
                    #                         if m in struct_nodes.keys():
                    #                             struct_nodes[m].append(uid)
                    #                         else:
                    #                             struct_nodes[m] = [uid]

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
                    gds_layer=b.gds_layer,
                    color=b.color,
                    node_id=v
                )
                g.node[n]['branch'] = value
                g.node[n]['connected_structures'].append(value)



        return nets

    def create_netlist(self):

        # print('Generating mask netlist')

        self.g = nx.disjoint_union_all(self.nets)

        for r in self.g.nodes(data='connected_structures'):
            if r[1] is not None:
                if isinstance(r[1], list):
                    for c1 in r[1]:
                        for d in self.g.nodes(data='connect'):
                            if d[1] is not None:
                                for c2 in d[1]:
                                    if not isinstance(c1, tuple):
                                        if not isinstance(c2, tuple):
                                            if c1.node_id == c2.node_id:
                                                self.g.add_edge(r[0], d[0])

        remove_nodes = []
        for S in self.structures:
            for n in self.g.nodes():
                if 'device' in self.g.node[n]:
                    D = self.g.node[n]['device']
                    if isinstance(D, spira.SRef):
                        if D.node_id == S.node_id:
                            remove_nodes.append(n)

        # self.g.remove_nodes_from(remove_nodes)

        for n in self.g.nodes:
            if 'connect' in self.g.node[n]:
                del self.g.node[n]['connect']

        self.plotly_netlist(G=self.g, graphname=self.name, labeltext='id')

        return self.g

