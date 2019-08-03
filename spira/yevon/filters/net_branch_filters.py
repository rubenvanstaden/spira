from spira.yevon import constants
from spira.log import SPIRA_LOG as LOG
from spira.yevon.filters.filter import Filter
from spira.yevon.gdsii.elem_list import ElementList
from spira.yevon.gdsii.polygon import Polygon
from spira.yevon.gdsii.group import Group
from spira.yevon.geometry.shapes.adapters import ShapeEdge
from spira.core.parameters.variables import *
from spira.yevon.process.purpose_layer import PurposeLayerParameter

from copy import deepcopy
from spira.core.parameters.variables import GraphParameter, StringParameter
from spira.core.parameters.descriptor import Parameter
from spira.yevon.geometry.coord import Coord
from spira.yevon.vmodel.geometry import GeometryParameter
from spira.yevon.geometry.ports.base import __Port__
from spira.yevon.process import get_rule_deck



__all__ = ['NetDummyFilter', 'NetBranchFilter']


class __NetlistFilter__(Filter):
    """ Base class for edge filters. """

    _ID = 0
    g = Parameter()

    __stored_paths__ = []
    __branch_nodes__ = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'g' in kwargs:
            self.g = kwargs['g']
        else:
            self.g = nx.Graph()

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
                if isinstance(D, spira.Port):
                    locked_nodes.append(n)
                elif isinstance(D, spira.ContactPort):
                    locked_nodes.append(n)
        for n in self.g.nodes():
            if n not in locked_nodes:
                remove_nodes.append(n)
        self.g.remove_nodes_from(remove_nodes)

    def __validate_path__(self, path):
        # from spira.netex.devices import Via
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
                # if issubclass(type(D), __Port__):
                #     if not isinstance(D, spira.Port):
                #         valid = False
                if issubclass(type(D), __Port__):
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
            source = 'source: {}'.format(Ds.reference.name)
        elif isinstance(Ds, spira.Port):
            source = 'source: {}'.format(Ds.name)

        if issubclass(type(Dt), spira.SRef):
            target = 'target: {}'.format(Dt.reference.name)
        elif isinstance(Ds, spira.Port):
            target = 'target: {}'.format(Dt.name)

        return "\n".join([ntype, number, source, target])

    @property
    def branch_nodes(self):
        """ Nodes that defines different conducting branches. """
        branch_nodes = list()
        for n in self.g.nodes():
            if 'device_reference' in self.g.node[n]:
                D = self.g.node[n]['device_reference']
                if isinstance(D, spira.SRef):
                    branch_nodes.append(n)
                if isinstance(D, spira.Port):
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
                    if issubclass(type(D.reference), Via):
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
    
    
# FIXME: Maybe convert this to a BranchList class.
class NetDummyFilter(__NetlistFilter__):
    """  """

    def filter_Net(self, item):
        
        self.__branch_nodes__ = self.branch_nodes
        
        if len(self.__branch_nodes__) > 0:
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
                        intersecting_paths = [x for x in p1 if x in set_2]
                        new_paths.append(intersecting_paths)
    
                dummies = set()
                for path in new_paths:
                    p = list(path)
                    dummies.add(p[-1])
    
                for i, n in enumerate(dummies):
                    if 'branch_node' in self.g.node[n]:
                        N = self.g.node[n]['branch_node']
                        ply = self.g.node[n]['process_polygon']
                        port = spira.Port(
                            name='B{}'.format(i),
                            midpoint=N.position,
                            process=ply.layer.process,
                        )
                        self.g.node[n]['device_reference'] = port
                        self.g.node[n]['display'] = RDD.DISPLAY.STYLE_SET[port.layer]
                        del self.g.node[n]['branch_node']
    
    
class NetBranchFilter(__NetlistFilter__):
    """  """

    def filter_Net(self, item):
        """  """

        self.__reset_stored_paths__()
        self.__increment_caller_id__()

        self.__branch_nodes__ = self.branch_nodes

        # print(self.__branch_nodes__)

        for sg in nx.connected_component_subgraphs(self.g, copy=True):

            for s in self.__branch_nodes__:
                # targets = filter(lambda x: x not in [s], self.master_nodes)
                targets = filter(lambda x: x not in [s], self.__branch_nodes__)
                for t in targets:
                    self.__store_branch_paths__(s, t)

            for i, path in enumerate(self.__stored_paths__):
                text = self.__get_called_id__()
                node_id = self.__branch_id__(i, path[0], path[-1])
                # print(path, text)
                # print(node_id)
                # print('')
                for n in path[1:-1]:
                    ply = self.g.node[n]['process_polygon']
                    label = spira.Label(position=ply.center, text=text, layer=ply.layer)
                    # label = spira.Label(position=ply.center, text=node_id, layer=ply.layer)
                    self.g.node[n]['branch_node'] = label

        # self.__remove_nodes__()

        return self.g
