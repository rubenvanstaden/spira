import spira.all as spira
import networkx as nx
from spira.yevon.geometry import shapes
from spira.yevon.visualization import color
from spira.yevon.geometry.ports.base import __Port__


class __NetlistSimplifier__(object):

    _ID = 0

    __stored_paths__ = []
    __branch_nodes__ = None

    def __remove_nodes__(self):
        """
        Nodes to be removed:
        1. Are not a branch node.
        2. Are not a device node.
        3. Branch nodes must equal the branch id.
        """
        locked_nodes = []
        remove_nodes = []
        text = self.__get_called_id__()
        for n in self.g.nodes():
            if 'branch_node' in self.g.node[n]:
                if isinstance(self.g.node[n]['branch_node'], spira.Label):
                    if self.g.node[n]['branch_node'].text == text:
                        locked_nodes.append(n)
            elif 'device_reference' in self.g.node[n]:
                D = self.g.node[n]['device_reference']
                if not isinstance(D, spira.spira.Port):
                    locked_nodes.append(n)
        for n in self.g.nodes():
            if n not in locked_nodes:
                remove_nodes.append(n)
        self.g.remove_nodes_from(remove_nodes)

    def __validate_path__(self, path):
        from spira.netex.devices import Via
        """ Test if path contains masternodes. """
        valid = True
        s, t = path[0], path[-1]
        if self.__is_path_stored__(s, t):
            valid = False
        if s not in self.__branch_nodes__:
            valid = False
        if t not in self.__branch_nodes__:
            valid = False
        for n in path[1:-1]:
            if 'device_reference' in self.g.node[n]:
                D = self.g.node[n]['device_reference']
                if issubclass(type(D), __Port__):
                    if not isinstance(D, spira.spira.Port):
                        valid = False
                if issubclass(type(D), spira.SRef):
                    valid = False
        return valid

    def __store_branch_paths__(self, s, t):
        if nx.has_path(self.g, s, t):
            p = nx.shortest_path(self.g, source=s, target=t)
            if self.__validate_path__(p):
                self.__stored_paths__.append(p)

    def __is_path_stored__(self, s, t):
        for path in self.__stored_paths__:
            if (s in path) and (t in path):
                return True
        return False

    def __reset_stored_paths__(self):
        self.__stored_paths__ = []

    def __increment_caller_id__(self):
        self._ID += 1

    def __get_called_id__(self):
        return '__{}__'.format(self._ID)

    def __branch_id__(self, i, s, t):
        ntype = 'nodetype: {}'.format('branch_node')
        number = 'number: {}'.format(i)

        Ds = self.g.node[s]['device_reference']
        Dt = self.g.node[t]['device_reference']

        if issubclass(type(Ds), spira.SRef):
            source = 'source: {}'.format(Ds.ref.name)
        elif issubclass(type(Ds), __Port__):
            if not isinstance(Ds, spira.spira.Port):
                source = 'source: {}'.format(Ds.name)

        if issubclass(type(Dt), spira.SRef):
            target = 'target: {}'.format(Dt.ref.name)
        elif issubclass(type(Dt), __Port__):
            if not isinstance(Dt, spira.spira.Port):
                target = 'target: {}'.format(Dt.name)

        return "\n".join([ntype, number, source, target])


class NetlistSimplifier(__NetlistSimplifier__):

    @property
    def branch_nodes(self):
        """ Nodes that defines different conducting branches. """
        branch_nodes = list()
        for n in self.g.nodes():
            if 'device_reference' in self.g.node[n]:
                D = self.g.node[n]['device_reference']
                if isinstance(D, spira.Dummy):
                    branch_nodes.append(n)
                if issubclass(type(D), (__Port__, spira.SRef)):
                    if not isinstance(D, spira.spira.Port):
                        branch_nodes.append(n)
        return branch_nodes

    @property
    def master_nodes(self):
        """ Excludes via devices with only two edges (series). """
        from spira.netex.devices import Via
        branch_nodes = list()
        for n in self.g.nodes():
            if 'device_reference' in self.g.node[n]:
                D = self.g.node[n]['device_reference']
                if issubclass(type(D), spira.SRef):
                    if issubclass(type(D.ref), Via):
                        if len([i for i in self.g[n]]) > 2:
                            branch_nodes.append(n)
                    else:
                        branch_nodes.append(n)
                if issubclass(type(D), __Port__):
                    branch_nodes.append(n)
        return branch_nodes

    @property
    def terminal_nodes(self):
        """ Nodes that defines different conducting branches. """
        branch_nodes = list()
        for n in self.g.nodes():
            if 'device_reference' in self.g.node[n]:
                D = self.g.node[n]['device_reference']
                if issubclass(type(D), spira.Port):
                    if not isinstance(D, spira.spira.Port):
                        branch_nodes.append(n)
        return branch_nodes

    def detect_dummy_nodes(self):

        for sg in nx.connected_component_subgraphs(self.g, copy=True):
            s = self.__branch_nodes__[0]

            paths = []
            for t in filter(lambda x: x not in [s], self.__branch_nodes__):
                # if nx.has_path(self.g, s, t):
                #     p = nx.shortest_path(self.g, source=s, target=t)
                #     paths.append(p)
                if nx.has_path(self.g, s, t):
                    for p in nx.all_simple_paths(self.g, source=s, target=t):
                        paths.append(p)

            new_paths = []
            for p1 in paths:
                for p2 in filter(lambda x: x not in [p1], paths):
                    set_2 = frozenset(p2)
                    intersection = [x for x in p1 if x in set_2]
                    new_paths.append(intersection)

            dummies = set()
            for path in new_paths:
                p = list(path)
                dummies.add(p[-1])

            for n in dummies:
                if 'branch_node' in self.g.node[n]:
                    N = self.g.node[n]['branch_node']
                    self.g.node[n]['device_reference'] = spira.Dummy(
                        name='Dummy',
                        midpoint=N.position,
                        color=color.COLOR_DARKSEA_GREEN,
                        node_id=self.g.node[n]['position']
                    )
                    del self.g.node[n]['branch_node']

    def generate_branches(self):
        """  """

        self.__reset_stored_paths__()
        self.__increment_caller_id__()

        self.__branch_nodes__ = self.branch_nodes

        for sg in nx.connected_component_subgraphs(self.g, copy=True):
            for s in self.__branch_nodes__:
                # targets = filter(lambda x: x not in [s], self.master_nodes)
                targets = filter(lambda x: x not in [s], self.__branch_nodes__)
                for t in targets:
                    self.__store_branch_paths__(s, t)

            for i, path in enumerate(self.__stored_paths__):
                text = self.__get_called_id__()
                node_id = self.__branch_id__(i, path[0], path[-1])
                for n in path[1:-1]:
                    lbl = self.g.node[n]['process_polygon']
                    self.g.node[n]['branch_node'] = spira.Label(
                        position=lbl.center,
                        text=text,
                        route=self.g.node[n]['route'].node_id,
                        gds_layer=lbl.ps_layer.layer,
                        # gds_layer=lbl.gds_layer,
                        color=lbl.color,
                        node_id=node_id
                    )

        self.__remove_nodes__()

        return self.g

