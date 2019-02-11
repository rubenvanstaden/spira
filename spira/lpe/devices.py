import spira 
from spira import param, shapes
from spira.lpe.mask import Metal, Native
from spira.lne.net import Net
from demo.pdks import ply
import numpy as np
from copy import copy, deepcopy
from spira.lpe.pcells import __PCell__
import networkx as nx
from spira.gdsii.elemental.port import __Port__
# from spira.param.field.typed_graph import PathList


RDD = spira.get_rule_deck()


class __Device__(__PCell__):
    """ A Cell encapsulates a set of elementals that
    describes the layout being generated. """

    level = param.IntegerField(default=1)
    lcar = param.IntegerField(default=0.000001)

    def get_primitives_function(self):
        prim_elems = spira.ElementList()

        contacts = self.contacts
        for N in contacts:
            prim_elems += N

        # # FIXME: Works for ytron, fails for junction.
        ports = self.ports
        for P in ports:
            prim_elems += P

        return prim_elems

    def create_boxes(self, boxes):
        return boxes

    def create_elementals(self, elems):

        metals = Metal(elementals=self.merged_layers, level=1)
        natives = Native(elementals=self.contacts, level=1)

        elems += spira.SRef(metals)
        elems += spira.SRef(natives)

        for key in RDD.VIAS.keys:
            RDD.VIAS[key].PCELL.create_elementals(elems)

        # for key in RDD.VIAS.keys:
        #     elems += spira.SRef(RDD.VIAS[key].PCELL, midpoint=(0,0))

        # if len(elems) == 0:
        #     metals = Metal(elementals=self.merged_layers, level=1)
        #     natives = Native(elementals=self.contacts, level=1)

        #     elems += spira.SRef(metals)
        #     elems += spira.SRef(natives)

        #     for key in RDD.VIAS.keys:
        #         RDD.VIAS[key].PCELL.create_elementals(elems)
        # else:
        #     print('----')
        #     print(elems)
        #     for key in RDD.VIAS.keys:
        #         C = spira.SRef(RDD.VIAS[key].PCELL, midpoint=(0,0))
        #         elems += C

        return elems

    def create_netlist(self):
        self.g = self.merge
        # self.g = self.nodes_combine(algorithm='d2d')
        # self.g = self.nodes_combine(algorithm='s2s')
        self.plot_netlist(G=self.g, graphname=self.name, labeltext='id')
        return self.g


class __Via__(__Device__):
    pass


class DeviceLayout(__Device__):

    def create_metals(self, elems):

        for player in RDD.PLAYER.get_physical_layers(purposes='METAL'):

            alias = '{}_{}'.format(
                player.layer.number,
                self.cell.id
            )

            metal_elems = spira.ElementList()
            R = self.cell.elementals.flat_copy()
            Rm = R.get_polygons(layer=player.layer)

            for i, e in enumerate(Rm):
                elems += ply.Polygon(
                    name='ply_{}_{}'.format(alias, i),
                    player=player,
                    points=e.polygons,
                    level=self.level
                )

        return elems

    def create_contacts(self, elems):

        for player in RDD.PLAYER.get_physical_layers(purposes=['VIA', 'JJ']):

            alias = '{}_{}'.format(
                player.layer.number,
                self.cell.id
            )

            metal_elems = spira.ElementList()
            R = self.cell.elementals.flat_copy()
            Rm = R.get_polygons(layer=player.layer)

            for i, e in enumerate(Rm):
                elems += ply.Polygon(
                    name='ply_{}_{}'.format(alias, i),
                    player=player,
                    points=e.polygons,
                    level=self.level
                )

        return elems


class Gate(__PCell__):

    device_ports = param.DataField(fdef_name='create_device_ports')

    __stored_paths__ = []

    def create_device_ports(self):

        print('--- Adding Device ports to Gate')

        ports = spira.ElementList()
        for R in self.cell.routes:
            # print(R.ref)
            # FIXME! Have to do this for Layouts.
            pp = R.polygons
            # FIXME! Have to do this for PCells.
            # pp = R.ref.elementals.polygons
            # print(pp)
            if len(pp) > 0:
                # g = R.ref.elementals.polygons[0]
                pp = R.polygons[0]
                for i, D in enumerate(self.cell.devices):
                    for S in D.ref.elementals:
                        if isinstance(S.ref, Metal):
                            for M in S.ref.elementals:

                                ply = deepcopy(M.polygon)
                                ply.move(midpoint=ply.center, destination=S.midpoint)

                                P = M.metal_port._copy()
                                P.connect(D, ply)
                                d = D.midpoint
                                P.move(midpoint=P.midpoint, destination=d)
                                P.node_id = '{}_{}'.format(P.node_id, i)
                                ports += P

                # for D in self.cell.elementals.sref:
                #     if issubclass(type(D.ref), __Device__):
                #         for S in D.ref.elementals:
                #             if isinstance(S.ref, Metal):
                #                 for M in S.ref.elementals:

                #                     ply = deepcopy(M.polygon)
                #                     ply.move(midpoint=ply.center, destination=S.midpoint)

                #                     P = M.metal_port._copy()
                #                     P.connect(D, ply)
                #                     d = D.midpoint
                #                     P.move(midpoint=P.midpoint, destination=d)
                #                     ports += P

        return ports

    def create_metals(self, elems):

        for player in RDD.PLAYER.get_physical_layers(purposes='METAL'):

            alias = '{}_{}'.format(
                player.layer.number,
                self.cell.id
            )

            metal_elems = spira.ElementList()
            R = self.cell.routes.flat_copy()
            B = self.cell.boxes.flat_copy()
            Rm = R.get_polygons(layer=player.layer)
            Bm = B.get_polygons(layer=player.layer)

            # for i, e in enumerate([*Rm]):
            for i, e in enumerate([*Rm, *Bm]):
                elems += ply.Polygon(
                    name='ply_{}_{}'.format(alias, i),
                    player=player,
                    points=e.polygons,
                    level=self.level
                )

        return elems

    def get_primitives_function(self):
        return self.ports

    def create_boxes(self, boxes):
        return self.cell.boxes

    
    # ----------------- Netlist Generator ---------------------


    def __remove_nodes__(self, text):
        remove = list()
        for n in self.g.nodes():
            # if 'device' in self.g.node[n]:
            #     # e = tuple([i for i in self.g[n]])
            #     # self.g.add_edge(*e, label=None)
            #     if not issubclass(type(self.g.node[n]['device']), __Port__):
            #         remove.append(n)
            if 'device' not in self.g.node[n]:
                # if 'path' not in self.g.node[n]:
                remove.append(n)
            elif isinstance(self.g.node[n]['device'], spira.Label):
                if self.g.node[n]['device'].text != text:
                    remove.append(n)

        self.g.remove_nodes_from(remove)

    def __is_path_stored__(self, s, t):
        for path in self.__stored_paths__:
            if (s in path) and (t in path):
                return True
        return False

    def __validate_path__(self, path):
        """ Test if path contains masternodes. """
        valid = True
        s, t = path[0], path[-1]
        if self.__is_path_stored__(s, t):
            valid = False
        if s not in self.master_nodes:
            valid = False
        if t not in self.master_nodes:
            valid = False
        for n in path[1:-1]:
            if 'device' in self.g.node[n]:
                # valid = False
                if issubclass(type(self.g.node[n]['device']), __Port__):
                    valid = False
        return valid

    def __store_branch_paths__(self, s, t):
        if nx.has_path(self.g, s, t):
            for p in nx.all_simple_paths(self.g, source=s, target=t):
                if self.__validate_path__(p):
                    self.__stored_paths__.append(p)

    @property
    def master_nodes(self):
        master_nodes = list()
        for n in self.g.nodes():
            if 'device' in self.g.node[n]:
                # if isinstance(self.g.node[n]['device'], spira.Dummy):
                #     master_nodes.append(n)
                if issubclass(type(self.g.node[n]['device']), __Port__):
                    master_nodes.append(n)
            # if 'device' in self.g.node[n]:
            #     if isinstance(self.g.node[n]['device'], BaseVia):
            #         master_nodes.append(n)
        return master_nodes

    # def detect_dummy_nodes(self):
    #     dummies = set()
    #     for p1 in self.__stored_paths__:
    #         ip = list()
    #         print(p1)
    #         print('-----------------')
    #         for p2 in filter(lambda x: x not in [p1], self.__stored_paths__):
    #         # for p2 in self.__stored_paths__:
    #             print(p2)
    #             intersections = set(p1[1:-1]).intersection(p2[1:-1])
    #             print(intersections)
    #             print('.')
    #             if intersections:
    #                 ip.append(intersections)
    #         # print(ip)
    #         print('')
    #         # if len(ip) > 1:
    #         #     print(ip)
    #         #     u = set.intersection(*ip)
    #     #         dummies.add(list(u)[0])

    #     # dummies = list(dummies)
    #     # print(dummies)

    #     # for d in dummies:
    #     #     N = self.g.nodes[d]['device']
    #     #     self.g.nodes[d]['device'] = spira.Dummy(
    #     #         name='Dummy',
    #     #         midpoint=N.position,
    #     #         color='#90EE90'
    #     #     )

    #     return dummies

    def detect_dummy_nodes(self):

        # T = nx.minimum_spanning_tree(self.g)
        # print(sorted(T))

        for sg in nx.connected_component_subgraphs(self.g, copy=True):
            s = self.master_nodes[0]
            print(s)
            # print(list(targets))
            # print('')
            paths = []
            for t in filter(lambda x: x not in [s], self.master_nodes):
                if nx.has_path(self.g, s, t):
                    for p in nx.all_simple_paths(self.g, source=s, target=t):
                        paths.append(p)

            new_paths = []
            for p1 in paths:
                print(p1)
                print('------------------------')
                # for p2 in paths:
                for p2 in filter(lambda x: x not in [p1], paths):
                    print(p2)
                    set_2 = frozenset(p2)
                    intersection = [x for x in p1 if x in set_2]
                    # intersections = frozenset(p2).intersection(p1)
                    new_paths.append(intersection)
                    print('{} {}'.format('Inter: ', intersection))
                    # print('.')
                print('')
                # print(new_paths)

            dummies = set()
            for path in new_paths:
                p = list(path)
                print(p)
                dummies.add(p[-1])
            print('Dummies:')
            print(dummies)

            for d in dummies:
                N = self.g.nodes[d]['device']
                # N = self.g.nodes[d]['path']
                if isinstance(N, spira.Label):
                    self.g.nodes[d]['device'] = spira.Dummy(
                        name='Dummy',
                        midpoint=N.position,
                        color='#90EE90'
                    )


        # dummies = set()
        # for p1 in self.__stored_paths__:
        #     ip = list()
        #     print(p1)
        #     print('-----------------')
        #     for p2 in filter(lambda x: x not in [p1], self.__stored_paths__):
        #     # for p2 in self.__stored_paths__:
        #         print(p2)
        #         intersections = set(p1).intersection(p2)
        #         print(intersections)
        #         print('.')
        #         if intersections:
        #             ip.append(intersections)
        #     # print(ip)
        #     print('')
        #     # if len(ip) > 1:
        #     #     print(ip)
        #     #     u = set.intersection(*ip)
        # #         dummies.add(list(u)[0])

        # # dummies = list(dummies)
        # # print(dummies)

        # # for d in dummies:
        # #     N = self.g.nodes[d]['device']
        # #     self.g.nodes[d]['device'] = spira.Dummy(
        # #         name='Dummy',
        # #         midpoint=N.position,
        # #         color='#90EE90'
        # #     )

        # return dummies

    def create_branches(self, text):
        """  """

        print('------- Branches ---------')

        for sg in nx.connected_component_subgraphs(self.g, copy=True):
            for s in self.master_nodes:
                print(s)
                targets = filter(lambda x: x not in [s], self.master_nodes)
                for t in targets:
                    self.__store_branch_paths__(s, t)
            for i, path in enumerate(self.__stored_paths__):

                source = self.g.node[path[-1]]['device'].__str__()

                for n in path[1:-1]:
                    lbl = self.g.node[n]['surface']
                    self.g.node[n]['device'] = spira.Label(
                    # self.g.node[n]['path'] = spira.Label(
                        position=lbl.position,
                        # text='path',
                        text=text,
                        gdslayer=lbl.gdslayer,
                        color='#FFFFFF',
                        node_id='{}_{}'.format(i, source)
                    )

        self.__remove_nodes__(text)
        # self.detect_dummy_nodes()

        return self.g



    def create_netlist(self):
        self.g = self.merge
        self.g = self.nodes_combine(algorithm='d2d')

        self.g = self.create_branches(text='A')
        self.detect_dummy_nodes()
        self.__stored_paths__ = []
        self.g = self.create_branches(text='B')

        self.g = self.nodes_combine(algorithm='d2d')
        # self.g = self.nodes_combine(algorithm='s2s')

        self.plot_netlist(G=self.g, graphname=self.name, labeltext='id')
        return self.g

    def create_elementals(self, elems):
        # for e in self.metals:
        #     elems += e
        for e in self.merged_layers:
            # print(e)
            elems += e

        # metals = Metal(elementals=self.merged_layers, level=2)
        # elems += spira.SRef(metals)

        return elems

    def create_ports(self, ports):
        for p in self.device_ports:
            ports += p
        for p in self.cell.terms:
            ports += p
        return ports


class GateLayout(Gate):

    def create_routes(self, routes):

        return routes

