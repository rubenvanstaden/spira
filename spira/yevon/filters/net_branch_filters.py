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
from spira.core.parameters.initializer import ParameterInitializer
from spira.yevon.geometry.nets.branch import Branch
from spira.yevon.geometry.nets.branch_list import BranchList
from spira.yevon.process import get_rule_deck
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = ['NetDummyFilter', 'NetBranchFilter', 'NetBranchCircuitFilter']


class __NetlistFilter__(Filter):
    """ Base class for edge filters. """
    pass


class NetBranchFilter(__NetlistFilter__):
    """  """

    _ID = 0
 
    def filter_Net(self, item):
        from spira.yevon.geometry.ports import Port

        NetBranchFilter._ID += 1

        from spira.yevon.utils.netlist import combine_net_nodes
        item = combine_net_nodes(net=item, algorithm=['d2d'])

        branches = BranchList()

        for sg in nx.connected_component_subgraphs(item.g, copy=True):

            for source in item.branch_nodes:
                for target in filter(lambda x: x not in [source], item.branch_nodes):
                    if nx.has_path(item.g, source, target):
                        path = nx.shortest_path(item.g, source=source, target=target)
                        branches += Branch(path=path, net=item)

            for i, b in enumerate(branches):
                for n in b.path:
                    if 'process_polygon' in item.g.node[n]:
                        ply = item.g.node[n]['process_polygon']
                        name = 'B{}{}'.format(i, NetBranchFilter._ID)
                        port = Port(name=name, midpoint=ply.center, process=ply.layer.process)
                        item.g.node[n]['branch_node'] = port

        item.remove_nodes()

        return [item]


class NetDummyFilter(__NetlistFilter__):
    """  """

    def filter_Net(self, item):
        from spira.yevon.geometry.ports import Port

        if len(item.branch_nodes) > 0:
            for sg in nx.connected_component_subgraphs(item.g, copy=True):

                s = item.branch_nodes[0]

                paths = []
                for t in filter(lambda x: x not in [s], item.branch_nodes):
                    if nx.has_path(item.g, s, t):
                        for p in nx.all_simple_paths(item.g, source=s, target=t):
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
                    if 'branch_node' in item.g.node[n]:
                        if 'device_reference' not in item.g.node[n]:
                            N = item.g.node[n]['branch_node']
                            ply = item.g.node[n]['process_polygon']
                            port = Port(
                                name='D{}'.format(i),
                                midpoint=N.midpoint,
                                process=ply.layer.process,
                            )
                            item.g.node[n]['device_reference'] = port
                            item.g.node[n]['display'] = RDD.DISPLAY.STYLE_SET[port.layer]
                            del item.g.node[n]['branch_node']
    
        return [item]


class NetBranchCircuitFilter(__NetlistFilter__):
    """  """

    _ID = 0
 
    def filter_Net(self, item):
        from spira.yevon.geometry.ports import Port

        NetBranchFilter._ID += 1

        from spira.yevon.utils.netlist import combine_net_nodes
        item = combine_net_nodes(net=item, algorithm=['d2d'])

        branches = BranchList()

        for sg in nx.connected_component_subgraphs(item.g, copy=True):

            for source in item.branch_nodes:
                for target in filter(lambda x: x not in [source], item.branch_nodes):
                    if nx.has_path(item.g, source, target):
                        path = nx.shortest_path(item.g, source=source, target=target)
                        branches += Branch(path=path, net=item)

            for i, b in enumerate(branches):
                if b.is_valid is True:
                    for n in b.path:
                        if 'process_polygon' in item.g.node[n]:
                            # ply = item.g.node[b.source]['process_polygon']
                            ply = item.g.node[n]['process_polygon']
                            name = 'B{}'.format(i)
                            port = Port(name=name, process=ply.layer.process)
                            item.g.node[n]['branch_node'] = port
                            item.g.node[n]['display'] = RDD.DISPLAY.STYLE_SET[ply.layer]

        item.remove_nodes()

        return [item]

