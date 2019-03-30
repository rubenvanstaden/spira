import spira
import numpy as np
from spira import param, shapes
from spira import pc
from spira.lpe.containers import __CellContainer__, __NetContainer__
from spira.lne.net import Net
from copy import copy, deepcopy
import networkx as nx
from spira import utils
from spira.core.mixin.netlist import NetlistSimplifier


RDD = spira.get_rule_deck()


class MetalNet(NetlistSimplifier):
    pass


class __NetlistCell__(__NetContainer__):

    @property
    def merge(self):

        # self.g = nx.disjoint_union_all(self.nets)
        # return self.g

        # graphs = []
        # for net in self.nets:
        #     graphs.append(net.graph)

        # graphs = []
        # for net in self.nets:
        #     MNet = MetalNet()
        #     G = net.graph
        #     MNet.g = utils.nodes_combine(G, algorithm='d2d')
        #     g = MNet.generate_branches()
        #     g = MNet.detect_dummy_nodes()
        #     g = MNet.generate_branches()
        #     # g = utils.nodes_combine(g, algorithm='b2b')
        #     graphs.append(g)
        #     # graphs.append(MNet.g)

        graphs = []
        for m in self.merged_layers:
            # graphs.append(m.graph)
            
            MNet = MetalNet()
            MNet.g = utils.nodes_combine(m.graph, algorithm='d2d')
        #    g = MNet.generate_branches()
            # g = MNet.detect_dummy_nodes()
            # g = MNet.generate_branches()
            # g = utils.nodes_combine(g, algorithm='b2b')
            # graphs.append(g)
            graphs.append(MNet.g)

        self.g = nx.disjoint_union_all(graphs)
        return self.g

    @property
    def connect(self):
        graphs = list(nx.connected_component_subgraphs(self.g))
        self.g = nx.disjoint_union_all(graphs)
        return self.g

    def nodes_combine(self, algorithm):
        """ Combine all nodes of the same type into one node. """

        def compare_d2s(u, v):
            if ('device' in self.g.node[u]):
                if ('device' not in self.g.node[v]):
                    if self.g.node[u]['device'].node_id == self.g.node[v]['surface'].node_id:
                        return True
            if ('device' in self.g.node[v]):
                if ('device' not in self.g.node[u]):
                    if self.g.node[v]['device'].node_id == self.g.node[u]['surface'].node_id:
                        return True
                        
        def compare_s2s(u, v):
            if ('surface' in self.g.node[u]) and ('surface' in self.g.node[v]):
                if ('device' not in self.g.node[u]) and ('device' not in self.g.node[v]):
                    if self.g.node[u]['surface'].node_id == self.g.node[v]['surface'].node_id:
                        return True

        def compare_d2d(u, v):
            if ('device' in self.g.node[u]) and ('device' in self.g.node[v]):
                if self.g.node[u]['device'].node_id == self.g.node[v]['device'].node_id:
                    return True

        def compare_b2b(u, v):
            if ('branch' in self.g.node[u]) and ('branch' in self.g.node[v]):
                if self.g.node[u]['branch'].node_id == self.g.node[v]['branch'].node_id:
                    return True

        def sub_nodes(b):
            S = self.g.subgraph(b)

            device = nx.get_node_attributes(S, 'device')
            surface = nx.get_node_attributes(S, 'surface')
            center = nx.get_node_attributes(S, 'pos')
            route = nx.get_node_attributes(S, 'route')
            branch = nx.get_node_attributes(S, 'branch')

            sub_pos = list()
            for value in center.values():
                sub_pos = [value[0], value[1]]

            # return dict(device=device, surface=surface, branch=branch, pos=sub_pos)
            return dict(device=device, surface=surface, branch=branch, route=route, pos=sub_pos)

        if algorithm == 'd2s':
            Q = nx.quotient_graph(self.g, compare_d2s, node_data=sub_nodes)
        elif algorithm == 's2s':
            Q = nx.quotient_graph(self.g, compare_s2s, node_data=sub_nodes)
        elif algorithm == 'd2d':
            Q = nx.quotient_graph(self.g, compare_d2d, node_data=sub_nodes)
        elif algorithm == 'b2b':
            Q = nx.quotient_graph(self.g, compare_b2b, node_data=sub_nodes)
        else:
            raise ValueError('Compare algorithm not implemented!')

        Pos = nx.get_node_attributes(Q, 'pos')
        Device = nx.get_node_attributes(Q, 'device')
        Polygon = nx.get_node_attributes(Q, 'surface')
        Route = nx.get_node_attributes(Q, 'route')
        Branches = nx.get_node_attributes(Q, 'branch')

        Edges = nx.get_edge_attributes(Q, 'weight')

        g1 = nx.Graph()

        for key, value in Edges.items():
            n1, n2 = list(key[0]), list(key[1])
            g1.add_edge(n1[0], n2[0])

        for n in g1.nodes():
            for key, value in Pos.items():
                if n == list(key)[0]:
                    g1.node[n]['pos'] = [value[0], value[1]]

            for key, value in Device.items():
                if n == list(key)[0]:
                    if n in value:
                        g1.node[n]['device'] = value[n]

            for key, value in Branches.items():
                if n == list(key)[0]:
                    if n in value:
                        g1.node[n]['branch'] = value[n]

            for key, value in Polygon.items():
                if n == list(key)[0]:
                    g1.node[n]['surface'] = value[n]

            for key, value in Route.items():
                if n == list(key)[0]:
                    if n in value:
                        g1.node[n]['route'] = value[n]

        self.g = g1

        return g1


class Structure(__NetlistCell__):
    """ Decorates all elementas with purpose metal with
    LCells and add them as elementals to the new class. """
    
    um = param.FloatField(default=1e+6)
    layout = param.BoolField(default=False)

    metals = param.ElementalListField()
    contacts = param.ElementalListField()

    terminals = param.ElementalListField()
    primitives = param.ElementalListField()
    merged_layers = param.ElementalListField()
    route_layers = param.ElementalListField()
    
    edge_datatype = param.IntegerField(default=103)
    arrow_datatype = param.IntegerField(default=81)

    level = param.IntegerField(default=2)
    algorithm = param.IntegerField(default=6)
    lcar = param.FloatField(default=0.0)

    def __metal_name__(self, uid, pl):
        name = 'metal_{}_{}_{}'.format(self.name, pl.layer.number, uid)
        return name

    def create_metals(self, elems):
        return elems

    def create_contacts(self, elems):
        return elems

    def create_primitives(self, elems):
        return elems

    def get_metals(self, pl):
        ply_elems = spira.ElementList()
        for M in self.merged_layers:
            if M.layer.is_equal_number(pl.layer):
                ply_elems += M
        return ply_elems

    def get_routes(self):
        elems = spira.ElementList()
        R = self.routes.flat_copy()
        for ps_layer in RDD.PLAYER.get_physical_layers(purposes='METAL'):
            Rm = R.get_polygons(layer=ps_layer.layer)
            for i, e in enumerate(Rm):
                alias = 'ply_{}_{}_{}'.format(ps_layer.layer.number, self.__class__.__name__, i)
                elems += pc.Polygon(name=alias, ps_layer=ps_layer, points=e.polygons, level=self.level)
        return elems
        
    def create_route_layers(self, elems):
        params = {}
        for M in self.get_routes():
            if isinstance(M, pc.ProcessLayer):
                if M.ps_layer not in params.keys():
                    params[M.ps_layer] = list(M.polygon.polygons)
                else:
                    for pp in M.polygon.polygons:
                        params[M.ps_layer].append(pp)
        for ps_layer, points in params.items():
            shape = shapes.Shape(points=points)
            shape.apply_merge
            for uid, pts in enumerate(shape.points):
                name = self.__metal_name__(uid, ps_layer)
                elems += pc.Polygon(
                    name=name,
                    ps_layer=ps_layer,
                    points=[pts],
                    level=self.level,
                    lcar=self.lcar,
                    algorithm=self.algorithm,
                    route_nodes=self.routes,
                    primitives=self.primitives,
                    bounding_boxes=self.contacts
                )
        return elems

    def create_merged_layers(self, elems):
        params = {}
        if self.level > 1:
            for M in self.metals:
                if isinstance(M, pc.ProcessLayer):
                    if M.ps_layer not in params.keys():
                        params[M.ps_layer] = list(M.polygon.polygons)
                    else:
                        for pp in M.polygon.polygons:
                            params[M.ps_layer].append(pp)
            for ps_layer, points in params.items():
                shape = shapes.Shape(points=points)
                shape.apply_merge
                for uid, pts in enumerate(shape.points):
                    name = self.__metal_name__(uid, ps_layer)
                    elems += pc.Polygon(
                        name=name,
                        ps_layer=ps_layer,
                        points=[pts],
                        level=self.level,
                        lcar=self.lcar,
                        algorithm=self.algorithm,
                        route_nodes=self.routes,
                        primitives=self.primitives,
                        bounding_boxes=self.contacts
                    )
        else:
            for M in self.metals:
                if isinstance(M, pc.ProcessLayer):
                    if M.ps_layer not in params.keys():
                        params[M.ps_layer] = list(M.polygon.polygons)
                    else:
                        for pp in M.polygon.polygons:
                            params[M.ps_layer].append(pp)
            for i, (ps_layer, points) in enumerate(params.items()):
                shape = shapes.Shape(points=points)
                shape.apply_merge
                for uid, pts in enumerate(shape.points):
                    name = self.__metal_name__(uid, ps_layer)
                    elems += pc.Polygon(
                        name=name,
                        ps_layer=ps_layer,
                        points=[pts],
                        level=self.level,
                        lcar=(self.lcar-0.01*i),
                        # lcar=self.lcar,
                        algorithm=self.algorithm,
                        route_nodes=self.routes,
                        primitives=self.primitives,
                        bounding_boxes=self.contacts
                    )

        return elems

    def create_ports(self, ports):
        """ Activate the edge ports to be used in
        the Device for metal connections. """

        for m in self.merged_layers:
        # for m in self.metals:
            for p in m.ports:
                if isinstance(p, (spira.Term, spira.EdgeTerm)):
                    edgelayer = deepcopy(p.gds_layer)
                    arrowlayer = deepcopy(p.gds_layer)
                    edgelayer.datatype = self.edge_datatype
                    arrowlayer.datatype = self.arrow_datatype
                    term = p.modified_copy(
                        name=p.name,
                        gds_layer=deepcopy(m.ps_layer.layer),
                        edgelayer=edgelayer,
                        arrowlayer=arrowlayer,
                        width=p.width
                    )
                    # print(term)
                    ports += term
        return ports

    def create_nets(self, nets):
        for pl in RDD.PLAYER.get_physical_layers(purposes='METAL'):
            polygons = self.get_metals(pl)
            if len(polygons) > 0:
                nets += Net(
                    name='{}'.format(pl.layer),
                    lcar=self.lcar,
                    level=self.level,
                    algorithm=self.algorithm,
                    layer=pl.layer,
                    polygons=polygons,
                    route_nodes=self.routes,
                    primitives=self.primitives,
                    bounding_boxes=self.contacts
                )
        return nets

