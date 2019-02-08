import spira 
from spira import param, shapes
from spira.lpe.mask import Metal, Native
from spira.lne.net import Net
from demo.pdks import ply
import numpy as np
from copy import copy, deepcopy
from spira.lpe.pcells import __PCell__


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

        # ports = self.ports
        # for P in ports:
        #     prim_elems += P

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
        self.g = self.nodes_combine(algorithm='d2d')
        self.g = self.nodes_combine(algorithm='s2s')
        self.plot_netlist(G=self.g, graphname=self.name, labeltext='id')
        return self.g


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

    def create_device_ports(self):
        ports = spira.ElementList()
        for R in self.cell.routes:
            pp = R.ref.elementals.polygons
            if len(pp) > 0:
                g = R.ref.elementals.polygons[0]
                for D in self.cell.elementals.sref:
                    if issubclass(type(D.ref), __Device__):
                        for S in D.ref.elementals:
                            if isinstance(S.ref, Metal):
                                for M in S.ref.elementals:

                                    ply = deepcopy(M.polygon)
                                    ply.move(midpoint=ply.center, destination=S.midpoint)

                                    P = M.metal_port._copy()
                                    P.connect(D, ply)
                                    d = D.midpoint
                                    P.move(midpoint=P.midpoint, destination=d)
                                    ports += P

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

            print(self.boxes)

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

    def create_netlist(self):
        self.g = self.merge
        self.g = self.nodes_combine(algorithm='d2d')
        # self.g = self.nodes_combine(algorithm='s2s')
        self.plot_netlist(G=self.g, graphname=self.name, labeltext='id')
        return self.g

    def create_elementals(self, elems):
        # for e in self.metals:
        #     elems += e
        for e in self.merged_layers:
            elems += e

        # metals = Metal(elementals=self.merged_layers, level=2)
        # elems += spira.SRef(metals)

        return elems

    def create_ports(self, ports):
        # for p in self.device_ports:
        #     ports += p
        for p in self.cell.terms:
            ports += p
        return ports


class GateLayout(Gate):

    def create_routes(self, routes):

        return routes

