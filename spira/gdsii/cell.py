import gdspy
import numpy as np
import networkx as nx
from copy import copy, deepcopy

from spira import param

from spira.core.lists import ElementList
from spira.lne import *
from spira.gdsii import *

from spira.core.initializer import CellInitializer
from spira.core.mixin.property import CellMixin
from spira.core.mixin.gdsii_output import OutputMixin
from spira.gdsii.elemental.port import __Port__
from spira.core.mixin.transform import TranformationMixin
from spira.rdd import get_rule_deck


RDD = get_rule_deck()


class __Cell__(gdspy.Cell, CellInitializer):

    __name_generator__ = RDD.ADMIN.NAME_GENERATOR
    __mixins__ = [OutputMixin, CellMixin, TranformationMixin]

    def __init__(self, elementals=None, ports=None, nets=None, library=None, **kwargs):
        CellInitializer.__init__(self, **kwargs)
        gdspy.Cell.__init__(self, self.name, exclude_from_current=True)

        self.g = nx.Graph()

        if library is not None:
            self.library = library
        if elementals is not None:
            self.elementals = elementals
        if ports is not None:
            self.ports = ports
        if nets is not None:
            self.nets = nets

    def __add__(self, other):
        if other is None:
            return self
        if issubclass(type(other), __Port__):
            self.ports += other
        else:
            self.elementals += other
        return self

    def __deepcopy__(self, memo):
        from copy import deepcopy
        kwargs = {}
        for p in self.__external_fields__():
            if p != 'name':
                kwargs[p] = deepcopy(getattr(self, p), memo)
        return self.__class__(**kwargs)


class Netlist(__Cell__):

    nets = param.ElementalListField(fdef_name='create_nets')
    netlist = param.DataField(fdef_name='create_netlist')
    merge = param.DataField(fdef_name='create_merge_nets')
    connect = param.DataField(fdef_name='create_connect_subgraphs')

    def create_nets(self, nets):
        return nets

    def create_netlist(self):
        pass

    def create_merge_nets(self):
        g = nx.disjoint_union_all(self.nets)
        return g

    def create_connect_subgraphs(self):
        graphs = list(nx.connected_component_subgraphs(self.g))
        g = nx.disjoint_union_all(graphs)
        return g

    def nodes_combine(self, algorithm):
        """ Combine all nodes of the same type into one node. """

        def compare_d2s(u, v):
            if ('device' in self.g.node[u]):
                if ('device' not in self.g.node[v]):
                    # if self.g.node[u]['device'].ply_id == self.g.node[v]['surface'].node_id:
                    if self.g.node[u]['device'].node_id == self.g.node[v]['surface'].node_id:
                    # if self.g.node[u]['device'].id == self.g.node[v]['surface'].node_id:
                        return True
            # if ('device' in self.g.node[v]):
            #     if self.g.node[v]['device'].name == self.g.node[u]['surface'].node_id:
            #         return True

        def compare_s2s(u, v):
            if ('surface' in self.g.node[u]) and ('surface' in self.g.node[v]):
                if ('device' not in self.g.node[u]) and ('device' not in self.g.node[v]):
                    if self.g.node[u]['surface'].node_id == self.g.node[v]['surface'].node_id:
                    # if self.g.node[u]['surface'] == self.g.node[v]['surface']:
                        return True

        def compare_d2d(u, v):
            if ('device' in self.g.node[u]) and ('device' in self.g.node[v]):
                # if self.g.node[u]['device'].id == self.g.node[v]['device'].id:
                if self.g.node[u]['device'] == self.g.node[v]['device']:
                # print(self.g.node[u]['device'])
                # if self.g.node[u]['device'].node_id == self.g.node[v]['device'].node_id:
                    return True

        def sub_nodes(b):
            S = self.g.subgraph(b)

            device = nx.get_node_attributes(S, 'device')
            surface = nx.get_node_attributes(S, 'surface')
            center = nx.get_node_attributes(S, 'pos')
            display = nx.get_node_attributes(S, 'display')

            sub_pos = list()
            for value in center.values():
                sub_pos = [value[0], value[1]]

            return dict(device=device, surface=surface, display=display, pos=sub_pos)

        if algorithm == 'd2s':
            Q = nx.quotient_graph(self.g, compare_d2s, node_data=sub_nodes)
        elif algorithm == 's2s':
            Q = nx.quotient_graph(self.g, compare_s2s, node_data=sub_nodes)
        elif algorithm == 'd2d':
            Q = nx.quotient_graph(self.g, compare_d2d, node_data=sub_nodes)
        else:
            raise ValueError('Compare algorithm not implemented!')

        Pos = nx.get_node_attributes(Q, 'pos')
        Device = nx.get_node_attributes(Q, 'device')
        Display = nx.get_node_attributes(Q, 'display')
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

            for key, value in Display.items():
                if n == list(key)[0]:
                    g1.node[n]['display'] = value[n]

            for key, value in Polygon.items():
                if n == list(key)[0]:
                    g1.node[n]['surface'] = value[n]
        return g1


class CellAbstract(Netlist):

    name = param.DataField(fdef_name='create_name')
    ports = param.ElementalListField(fdef_name='create_ports')
    elementals = param.ElementalListField(fdef_name='create_elementals')

    def create_elementals(self, elems):
        result = ElementList()
        return result

    def create_ports(self, ports):
        return ports

    def create_name(self):
        if not hasattr(self, '__name__'):
            self.__name__ = self.__name_generator__(self)
        return self.__name__

    def flatten(self):
        self.elementals = self.elementals.flatten()
        return self.elementals

    def flat_copy(self, level=-1, commit_to_gdspy=False):
        # print(self.elementals)
        # print('')
        self.elementals = self.elementals.flat_copy(level, commit_to_gdspy)
        return self.elementals

    def dependencies(self):
        deps = self.elementals.dependencies()
        # if hasattr(self, 'routes'):
        #     deps += self.routes.dependencies()
        deps += self
        return deps

    @property
    def pbox(self):
        (a,b), (c,d) = self.bbox
        points = [[[a,b], [c,b], [c,d], [a,d]]]
        return points

    def commit_to_gdspy(self):
        from demo.pdks.ply.base import ProcessLayer
        cell = gdspy.Cell(self.name, exclude_from_current=True)

        for e in self.elementals:
            if not isinstance(e, (SRef, ElementList, Graph, Mesh)):
                e.commit_to_gdspy(cell=cell)


            # if issubclass(type(e), ProcessLayer):
            #     e.polygon.commit_to_gdspy(cell=cell)
            #     for p in e.ports:
            #         p.commit_to_gdspy(cell=cell)
            # elif not isinstance(e, (SRef, ElementList, Graph, Mesh)):
            #     e.commit_to_gdspy(cell=cell)

        # if hasattr(self, 'routes'):
        #     # print(self.routes)
        #     for e in self.routes:
        #         if issubclass(type(e), Cell):
        #             e.polygon.commit_to_gdspy(cell=cell)
        #             for p in e.ports:
        #                 p.commit_to_gdspy(cell=cell)
        #         # elif not isinstance(e, (SRef, ElementList, Graph, Mesh)):
        #         elif isinstance(e, SRef):
        #             e.commit_to_gdspy(cell=e.ref)



        # for p in self.ports:
        #     p.commit_to_gdspy(cell=cell)

        # for e in self.elementals:
        #     # if issubclass(type(e), ProcessLayer):
        #     #     e = SRef(e)

        #     # if not isinstance(e, (SRef, ElementList, Graph, Mesh)):
        #     #     e.commit_to_gdspy(cell=cell)

        #     # if issubclass(type(e), Cell):
        #     #     for elem in e.elementals:
        #     #         elem.commit_to_gdspy(cell=cell)
        #     #     # for port in e.ports:
        #     #     #     port.commit_to_gdspy(cell=cell)
        #     #     for p in e.get_ports():
        #     #         p.commit_to_gdspy(cell=cell)

        #     # if issubclass(type(e), Cell):
        #     if issubclass(type(e), ProcessLayer):
        #         # e.polygon.commit_to_gdspy(cell=cell)
        #         # for p in e.get_ports():
        #         #     p.commit_to_gdspy(cell=cell)
        #         # # e.ports.commit_to_gdspy(cell=cell)
        #     elif not isinstance(e, (SRef, ElementList, Graph, Mesh)):
        #         e.commit_to_gdspy(cell=cell)

        return cell

    def move(self, midpoint=(0,0), destination=None, axis=None):
        """
        Moves elements of the Device from the midpoint point to
        the destination. Both midpoint and destination can be 1x2
        array-like, Port, or a key corresponding to
        one of the Ports in this device
        """

        if destination is None:
            destination = midpoint
            midpoint = [0,0]

        if issubclass(type(midpoint), __Port__):
            o = midpoint.midpoint
        elif np.array(midpoint).size == 2:
            o = midpoint
        elif midpoint in self.ports:
            o = self.ports[midpoint].midpoint
        else:
            raise ValueError('[DeviceReference.move()] ``midpoint`` ' + \
                             'not array-like, a port, or port name')

        if issubclass(type(destination), __Port__):
            d = destination.midpoint
        elif np.array(destination).size == 2:
            d = destination
        elif destination in self.ports:
            d = self.ports[destination].midpoint
        else:
            raise ValueError('[DeviceReference.move()] ``destination`` ' + \
                             'not array-like, a port, or port name')

        if axis == 'x':
            d = (d[0], o[1])
        if axis == 'y':
            d = (o[0], d[1])

        dx, dy = np.array(d) - o

        from demo.pdks.ply.base import ProcessLayer
        for e in self.elementals:
            if issubclass(type(e), (LabelAbstract, PolygonAbstract)):
                e.translate(dx, dy)
            if issubclass(type(e), ProcessLayer):
                e.move(destination=d, midpoint=o)
            if isinstance(e, SRef):
                e.move(destination=d, midpoint=o)

        # if hasattr(self, 'routes'):
        #     for e in self.routes:
        #         if issubclass(type(e), (LabelAbstract, PolygonAbstract)):
        #             e.translate(dx, dy)
        #         if isinstance(e, (Cell, SRef)):
        #             e.move(destination=d, midpoint=o)

        for p in self.ports:
            mc = np.array(p.midpoint) + np.array(d) - np.array(o)
            p.move(midpoint=p.midpoint, destination=mc)

        return self

    def reflect(self, p1=(0,1), p2=(0,0)):
        """ Reflects the cell around the line [p1, p2]. """
        for e in self.elementals:
            if not issubclass(type(e), LabelAbstract):
                e.reflect(p1, p2)
        for p in self.ports:
            p.midpoint = self.__reflect__(p.midpoint, p1, p2)
            phi = np.arctan2(p2[1]-p1[1], p2[0]-p1[0])*180 / np.pi
            p.orientation = 2*phi - p.orientation
        return self

    def rotate(self, angle=45, center=(0,0)):
        """ Rotates the cell with angle around a center. """
        from demo.pdks.ply.base import ProcessLayer
        if angle == 0:
            return self
        for e in self.elementals:
            if issubclass(type(e), PolygonAbstract):
                e.rotate(angle=angle, center=center)
            elif isinstance(e, SRef):
                e.rotate(angle, center)
            elif issubclass(type(e), ProcessLayer):
                e.rotate(angle, center)

        # if hasattr(self, 'routes'):
        #     for e in self.routes:
        #         if issubclass(type(e), PolygonAbstract):
        #             e.rotate(angle=angle, center=center)
        #         elif isinstance(e, SRef):
        #             e.rotate(angle, center)

        ports = self.ports
        self.ports = ElementList()
        for p in ports:
            if issubclass(type(p), __Port__):
                p.midpoint = self.__rotate__(p.midpoint, angle, center)
                p.orientation = np.mod(p.orientation + angle, 360)
                self.ports += p
        return self

    def get_ports(self, level=None):
        """ Returns copies of all the ports of the Device """
        port_list = [p._copy() for p in self.ports]
        if level is None or level > 0:

            # if hasattr(self, 'routes'):
            #     for r in self.routes.sref:
            #         if level is None:
            #             new_level = None
            #         else:
            #             new_level = level - 1

            #         ref_ports = r.ref.get_ports(level=new_level)

            #         tf = {
            #             'midpoint': r.midpoint,
            #             'rotation': r.rotation,
            #             'magnification': r.magnification,
            #             'reflection': r.reflection
            #         }

            #         ref_ports_transformed = []
            #         for rp in ref_ports:
            #             new_port = rp._copy()
            #             new_port = new_port.transform(tf)
            #             ref_ports_transformed.append(new_port)
            #         port_list += ref_ports_transformed

            for r in self.elementals.sref:
                if level is None:
                    new_level = None
                else:
                    new_level = level - 1

                ref_ports = r.ref.get_ports(level=new_level)

                tf = {
                    'midpoint': r.midpoint,
                    'rotation': r.rotation,
                    'magnification': r.magnification,
                    'reflection': r.reflection
                }

                ref_ports_transformed = []
                for rp in ref_ports:
                    new_port = rp._copy()
                    new_port = new_port.transform(tf)
                    ref_ports_transformed.append(new_port)
                port_list += ref_ports_transformed
        return port_list


class Cell(CellAbstract):
    """ A Cell encapsulates a set of elementals that
    describes the layout being generated. """

    def __repr__(self):
        if hasattr(self, 'elementals'):
            elems = self.elementals
            return ("[SPiRA: Cell(\'{}\')] " +
                    "({} elementals: {} sref, {} cells, {} polygons, " +
                    "{} labels, {} ports)").format(
                        self.name,
                        elems.__len__(),
                        elems.sref.__len__(),
                        elems.cells.__len__(),
                        elems.polygons.__len__(),
                        elems.labels.__len__(),
                        self.ports.__len__()
                    )
        else:
            return "[SPiRA: Cell(\'{}\')]".format(self.__class__.__name__)

    # FIXME: Has to be placed here for deepcopy().
    def __str__(self):
        return self.__repr__()

    def _copy(self):
        cell = Cell(
            name=self.name,
            elementals=deepcopy(self.elementals),
            ports=deepcopy(self.ports),
            nets=self.nets
        )
        return cell

    # def transform(self, transform):
    #     if transform['reflection']:
    #         self.reflect(p1=[0,0], p2=[1,0])
    #     if transform['rotation']:
    #         self.rotate(angle=transform['rotation'])
    #     if transform['midpoint']:
    #         self.move(midpoint=self.center, destination=transform['midpoint'])
    #     return self


class PCell(CellAbstract):
    """ A Cell encapsulates a set of elementals that
    describes the layout being generated. """

    def __repr__(self):
        if hasattr(self, 'elementals'):
            elems = self.elementals
            return ("[SPiRA: Parameterized Cell(\'{}\')] " +
                    "({} elementals: {} sref, {} cells, {} polygons, " +
                    "{} labels, {} ports)").format(
                        self.name,
                        elems.__len__(),
                        elems.sref.__len__(),
                        elems.cells.__len__(),
                        elems.polygons.__len__(),
                        elems.labels.__len__(),
                        self.ports.__len__()
                    )
        else:
            return "[SPiRA: Cell(\'{}\')]".format(self.__class__.__name__)

    # FIXME: Has to be placed here for deepcopy().
    def __str__(self):
        return self.__repr__()

    def _copy(self):
        cell = PCell(
            name=self.name,
            elementals=deepcopy(self.elementals),
            ports=deepcopy(self.ports),
            nets=self.nets
        )
        return cell


class Device(CellAbstract):
    pass


class Circuit(CellAbstract):
    """ A Cell encapsulates a set of elementals that
    describes the layout being generated. """

    routes = param.ElementalListField(fdef_name='create_routes')

    def __init__(self, elementals=None, ports=None, nets=None, routes=None, library=None, **kwargs):
        super().__init__(elementals=None, ports=None, nets=None, library=None, **kwargs)

        if routes is not None:
            self.routes = routes

    def create_routes(self, routes):
        return routes

    def __repr__(self):
        if hasattr(self, 'elementals'):
            elems = self.elementals
            return ("[SPiRA: Circuit(\'{}\')] " +
                    "({} elementals: {} sref, {} cells, {} polygons, " +
                    "{} labels, {} ports)").format(
                        self.name,
                        elems.__len__(),
                        elems.sref.__len__(),
                        elems.cells.__len__(),
                        elems.polygons.__len__(),
                        elems.labels.__len__(),
                        self.ports.__len__()
                    )
        else:
            return "[SPiRA: Cell(\'{}\')]".format(self.__class__.__name__)

    # FIXME: Has to be placed here for deepcopy().
    def __str__(self):
        return self.__repr__()

    def _copy(self):
        cell = Circuit(
            name=self.name,
            elementals=deepcopy(self.elementals),
            routes=deepcopy(self.routes),
            ports=deepcopy(self.ports),
            nets=self.nets
        )
        return cell










