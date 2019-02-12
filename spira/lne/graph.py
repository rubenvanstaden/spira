import networkx as nx
from spira.gdsii.elemental.label import Label
from spira.param.field.typed_graph import PathList
from spira import param
from spira.core.initializer import ElementalInitializer
import spira
from spira import log as LOG
from spira.core.mixin.gdsii_output import OutputMixin


def _loops(g):
    """

    """

    def _is_valid_cycle(g, cycle, devices):
        if len(cycle) > 2:
            for n in cycle:
                if 'device' in g.node[n]:
                    lbl = g.node[n]['device']
                    if _is_device(lbl):
                        devices.append(lbl)

            if len(devices) < 2:
                return True
        return False

    H = g.to_directed()
    cycles = list(nx.simple_cycles(H))

    if len(cycles) < 3:
        return g

    valid_cycle_count = 0
    for cycle in cycles:
        devices = []
        if _is_valid_cycle(g, cycle, devices):
            for n in cycle:
                if len(devices) > 0:
                    g.node[n]['device'] = devices[0]
            valid_cycle_count += 1

    if valid_cycle_count != 0:
        g = _loops(g)
    else:
        return g

    return g


# def _is_master(g, n):
#     lbl = g.node[n]['device']

#     if lbl.text.startswith('via'):
#         if len([i for i in g[n]]) > 2:
#             return True

#     masternodes = ['C', 'P', 'ntron', 'user', 'jj', 'gnd', 'shunt']
#     for key in masternodes:
#         if lbl.text.startswith(key):
#             return True

#     return False


# def _is_device(lbl):
#     devicenodes = ['jj', 'ntron']
#     for key in devicenodes:
#         if lbl.text.startswith(key): return True
#     return False


# def _make_usernode(lbl):
#     usernodes = ['via', 'C', 'P', 'ntron', 'user', 'jj', 'gnd', 'shunt']
#     for key in usernodes:
#         if lbl.text.startswith(key): return True
#     return False


def _valid_path(g, path, branch_nodes):
    """
    Test if path contains masternodes.
    """
    valid = True

    if path[0] not in branch_nodes: valid = False
    if path[-1] not in branch_nodes: valid = False

    for n in path[1:-1]:
        if 'device' in g.node[n]:
            # if _is_master(g, n):
            # masternodes = (spira.JunctionDevice, spira.UserNode, spira.PortNode)
            if isinstance(g.node[n]['device'], BaseVia):
                valid = False
    return valid


def store_master_nodes(g):
    branch_nodes = list()
    for n in g.nodes():
        if 'device' in g.node[n]:
            # if _is_master(g, n):
            # masternodes = (spira.JunctionDevice, spira.UserNode, spira.PortNode)
            # if issubclass(type(g.node[n]['device']), masternodes):
            if isinstance(g.node[n]['device'], BaseVia):
                branch_nodes.append(n)
    return branch_nodes


def subgraphs(lgraph):
    # logger = logging.getLogger(__name__)
    # logger.info('Merging subgraphs')

    graphs = list(nx.connected_component_subgraphs(lgraph.g))

    gg = list()
    for graph in graphs:
        save = False
        for n in graph.nodes():
            if 'device' in graph.node[n]:
                label = graph.node[n]['device']
                if isinstance(label, Terminal):
                    save = True

        if save is True:
            gg.append(graph)

    lgraph.g = nx.disjoint_union_all(gg)


class __Graph__(ElementalInitializer):

    __mixins__ = [OutputMixin]

    def __init__(self, subgraphs, data=None, val=None, **kwargs):

        ElementalInitializer.__init__(self, **kwargs)

        self.g = nx.Graph()

        self.subgraphs = subgraphs

        self.union_subgraphs
        # self.combine_nodes
        # self.connect_subgraphs

        self.usernodes = []
        self.seriesnodes = []
        self.branch_nodes = []

    def __repr__(self):
        return ("[SPiRA: Graph] ({} nodes, {} edges)").format(self.g.number_of_nodes(),
                                                              self.g.number_of_edges())

    def __str__(self):
        return self.__repr__()


class GraphAbstract(__Graph__):

    union_subgraphs = param.DataField(fdef_name='create_union_subgraphs')
    connect_subgraphs = param.DataField(fdef_name='create_connect_subgraphs')
    combine_nodes = param.DataField(fdef_name='create_combine_nodes')

    def __init__(self, subgraphs, data=None, val=None, **kwargs):
        super().__init__(subgraphs, data=None, val=None, **kwargs)

    def create_union_subgraphs(self):
        # self.g = nx.disjoint_union_all(self.subgraphs.values())
        # print(self.subgraphs)
        self.g = nx.disjoint_union_all(self.subgraphs)

    def create_connect_subgraphs(self):
        graphs = list(nx.connected_component_subgraphs(self.g))
        self.g = nx.disjoint_union_all(graphs)

    def create_combine_nodes(self):
        """
        Combine all nodes of the same type into one node.
        """

        def partition_nodes(u, v):

            if ('surface' in self.g.node[u]) and ('surface' in self.g.node[v]):
                if ('device' not in self.g.node[u]) and ('device' not in self.g.node[v]):
                    if self.g.node[u]['surface'].node_id == self.g.node[v]['surface'].node_id:
                    # if self.g.node[u]['surface'] == self.g.node[v]['surface']:
                        return True

            if ('device' in self.g.node[u]) and ('device' in self.g.node[v]):
                # if self.g.node[u]['device'].node_id == self.g.node[v]['device'].node_id:
                if self.g.node[u]['device'] == self.g.node[v]['device']:
                    return True

        def sub_nodes(b):
            S = self.g.subgraph(b)

            device = nx.get_node_attributes(S, 'device')
            surface = nx.get_node_attributes(S, 'surface')
            center = nx.get_node_attributes(S, 'pos')

            sub_pos = list()
            for key, value in center.items():
                sub_pos = [value[0], value[1]]

            return dict(device=device, surface=surface, pos=sub_pos)

        Q = nx.quotient_graph(self.g, partition_nodes, node_data=sub_nodes)

        Pos = nx.get_node_attributes(Q, 'pos')
        Device = nx.get_node_attributes(Q, 'device')
        Polygon = nx.get_node_attributes(Q, 'surface')

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

            for key, value in Polygon.items():
                if n == list(key)[0]:
                    g1.node[n]['surface'] = value[n]

        self.g = g1

    def flat_copy(self, level=-1, commit_to_gdspy=False):
        return self

    def flatten(self):
        return [self]

    def commit_to_gdspy(self, cell):
        pass

    def transform(self, transform):
        pass


class UserGraph(GraphAbstract):

    user_nodes = param.DataField(fdef_name='create_label_user_nodes')
    convert_nodes = param.DataField(fdef_name='create_convert_user_nodes')

    def __init__(self, subgraphs, data=None, val=None, **kwargs):
        super().__init__(subgraphs, data=None, val=None, **kwargs)

        # self.user_nodes
        # self.convert_nodes

    def create_label_user_nodes(self):

        def _usernode_label(position, node_id=None):
            params = {}
            params['node_id'] = node_id
            params['text'] = 'user'
            params['color'] = '#CC99CC'

            label = Label(position, **params)

            D = spira.UserNode()
            D.color = '#1ea8df'

            D += label

            return D

        for n in self.g.nodes():
            if len([i for i in self.g[n]]) > 2:
                if 'device' not in self.g.node[n]:

                    self.g.node[n]['device'] = _usernode_label(
                        position=self.g.node[n]['pos'],
                        node_id=self.g.node[n]['surface'].id
                    )

                    self.usernodes.append(n)
                else:
                    if not issubclass(type(self.g.node[n]['device']), spira.Cell):

                        self.g.node[n]['device'] = _usernode_label(
                            position=self.g.node[n]['pos'],
                            node_id=self.g.node[n]['surface'].id
                        )

                        self.usernodes.append(n)

        # self.create_combine_nodes()

    def create_convert_user_nodes(self):

        LOG.header('Converting usernodes')

        if len(self.usernodes) == 0:
            raise ValueError('please run label_user_nodes first')

        changed = dict()
        for n in self.usernodes:
            neighbor_nodes = [i for i in self.g[n]]
            for nn in neighbor_nodes:
                if 'device' in self.g.node[nn]:
                    if issubclass(type(self.g.node[nn]['device']), spira.JunctionDevice):
                        changed[n] = self.g.node[nn]['device']

        for n, usernode in changed.items():
            self.g.node[n]['device'] = usernode

        self.create_combine_nodes()

        self.branch_nodes = store_master_nodes(self.g)


class SeriesGraph(UserGraph):

    series_nodes = param.DataField(fdef_name='create_label_series_nodes')
    remove_lonely = param.DataField(fdef_name='create_remove_lonely_nodes')
    remove_series = param.DataField(fdef_name='create_remove_series_nodes')

    def __init__(self, subgraphs, data=None, val=None, **kwargs):
        super().__init__(subgraphs, data=None, val=None, **kwargs)

        # self.series_nodes
        # self.remove_lonely
        # self.remove_series

    def create_label_series_nodes(self, algo=None):
        print('running series graph node filtering')
        sub_graphs = nx.connected_component_subgraphs(self.g, copy=True)

        self.branch_nodes = store_master_nodes(self.g)

        def _remove_label(lbl, node_id=None):
            params = {}
            params['node_id'] = node_id
            params['text'] = 'remove'
            params['gdslayer'] = lbl.gdslayer
            params['color'] = '#FFFFFF'

            label = Label(lbl.position, **params)

            D = spira.RemoveNode()
            D.color = '#FFFFFF'

            return D

        def _none_label(lbl, node_id=None):
            params = {}
            params['node_id'] = node_id
            params['text'] = 'remove'
            params['gdslayer'] = lbl.gdslayer
            params['color'] = '#FFFFFF'

            label = Label(lbl.position, **params)

            D = spira.RemoveNode()
            D.color = '#FFF000'

            return D

        def _update_paths(g, paths, s, t):
            if nx.has_path(g, s, t):
                for p in nx.all_simple_paths(g, source=s, target=t):
                    if _valid_path(g, p, self.branch_nodes):
                        paths.append(p)

        for sg in sub_graphs:
            paths = PathList()
            for s in self.branch_nodes:
                targets = filter(lambda x: x not in [s], self.branch_nodes)
                for t in targets:
                    _update_paths(self.g, paths, s, t)

            # print(paths)
            for i, path in enumerate(paths):
                if i == 2:
                    for n in path[1:-1]:
                        lbl = self.g.node[n]['surface']
                        if not issubclass(type(lbl), spira.RemoveNode):
                            self.g.node[n]['device'] = _none_label(lbl, node_id=i)

    def create_remove_lonely_nodes(self):
        remove = list()
        for n in self.g.nodes():
            if len([i for i in self.g[n]]) == 1:
                if 'device' not in self.g.node[n]:
                    remove.append(n)
        self.g.remove_nodes_from(remove)

    def create_remove_series_nodes(self):
        self.create_combine_nodes()

        remove = list()
        for n in self.g.nodes():
            if 'device' in self.g.node[n]:
                lbl = self.g.node[n]['device']
                # if lbl.text.startswith('remove'):
                if issubclass(type(lbl), spira.RemoveNode):
                    e = tuple([i for i in self.g[n]])
                    self.g.add_edge(*e, label=None)
                    remove.append(n)
        self.g.remove_nodes_from(remove)


class Graph(SeriesGraph):
    pass
