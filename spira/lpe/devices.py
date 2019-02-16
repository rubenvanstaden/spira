import spira 
from spira import param, shapes
from spira.lpe.mask import Metal, Native
from spira.lne.net import Net
from demo.pdks import ply
import numpy as np
from copy import copy, deepcopy
from spira.lpe.pcells import __PolygonOperator__
from spira.gdsii.elemental.port import __Port__
# from spira.param.field.typed_graph import PathList
from spira.core.mixin.netlist import NetlistSimplifier
from spira.lpe.containers import __CellContainer__


RDD = spira.get_rule_deck()


class Device(__PolygonOperator__):
    """ A Cell encapsulates a set of elementals that
    describes the layout being generated. """

    level = param.IntegerField(default=1)

    def __init__(self, name=None, elementals=None, ports=None, nets=None, metals=None, contacts=None, library=None, **kwargs):
        super().__init__(name=None, elementals=None, ports=None, nets=None, library=None, **kwargs)

        if metals is not None:
            self.metals = metals
        if contacts is not None:
            self.contacts = contacts

    def get_local_devices(self):
        prim_elems = spira.ElementList()
        for N in self.contacts:
            prim_elems += N
        # FIXME: Works for ytron, fails for junction.
        # for P in self.ports:
        #     prim_elems += P
        return prim_elems

    def create_elementals(self, elems):

        metals = Metal(elementals=self.merged_layers, level=self.level)
        natives = Native(elementals=self.contacts, level=self.level)

        elems += spira.SRef(metals)
        elems += spira.SRef(natives)

        for key in RDD.VIAS.keys:
            RDD.VIAS[key].PCELL.create_elementals(elems)

        return elems

    def create_netlist(self):
        self.g = self.merge

        self.g = self.nodes_combine(algorithm='d2d')
        self.g = self.nodes_combine(algorithm='s2s')

        # self.plot_netlist(G=self.g, graphname=self.name, labeltext='id')

        return self.g


class DeviceLayout(__CellContainer__):

    metals = param.ElementalListField()
    contacts = param.ElementalListField()
    level = param.IntegerField(default=2)

    def generate_physical_polygons(self, pl):
        elems = spira.ElementList()
        metal_elems = spira.ElementList()
        R = self.cell.elementals.flat_copy()
        Rm = R.get_polygons(layer=pl.layer)
        for i, e in enumerate(Rm):
            alias = 'ply_{}_{}_{}'.format(pl.layer.number, self.cell.id, i)
            elems += ply.Polygon(name=alias, player=pl, points=e.polygons, level=self.level)
        return elems

    def create_metals(self, elems):
        for player in RDD.PLAYER.get_physical_layers(purposes='METAL'):
            for e in self.generate_physical_polygons(player):
                elems += e
        return elems

    def create_contacts(self, elems):
        for player in RDD.PLAYER.get_physical_layers(purposes=['VIA', 'JJ']):
            for e in self.generate_physical_polygons(player):
                elems += e
        return elems


class Gate(__PolygonOperator__):

    __mixins__ = [NetlistSimplifier]

    def create_contacts(self, contacts):
        print('--- Adding Device ports to Gate')
        for R in self.cell.routes:
            pp = R.ref.elementals.polygons
            if len(pp) > 0:
                g = R.ref.elementals.polygons[0]
                for i, D in enumerate(self.cell.devices):
                    for S in D.ref.elementals:
                        if isinstance(S.ref, Metal):
                            for M in S.ref.elementals:
                                ply = deepcopy(M.polygon)
                                ply.move(midpoint=ply.center, destination=S.midpoint)
                                # P = copy(M.metal_port)
                                # P = deepcopy(M.metal_port)
                                P = M.metal_port._copy()
                                P.connect(D, ply)
                                d = D.midpoint
                                P.move(midpoint=P.midpoint, destination=d)
                                P.node_id = '{}_{}'.format(P.node_id, i)
                                contacts += P

                                # if (M.polygon & g) and (g.is_equal_layers(M.polygon)):
                                #     ply = deepcopy(M.polygon)
                                #     ply.move(midpoint=ply.center, destination=S.midpoint)
                                #     P = M.metal_port._copy()
                                #     P.connect(D, ply)
                                #     d = D.midpoint
                                #     P.move(midpoint=P.midpoint, destination=d)
                                #     P.node_id = '{}_{}'.format(P.node_id, i)
                                #     contacts += P
        return contacts

    def create_metals(self, elems):

        for player in RDD.PLAYER.get_physical_layers(purposes='METAL'):

            metal_elems = spira.ElementList()
            R = self.cell.routes.flat_copy()
            B = self.cell.boxes.flat_copy()
            Rm = R.get_polygons(layer=player.layer)
            Bm = B.get_polygons(layer=player.layer)

            for i, e in enumerate([*Rm, *Bm]):
                alias = 'ply_{}_{}_{}'.format(player.layer.number, self.cell.id, i)
                elems += ply.Polygon(name=alias, player=player, points=e.polygons, level=self.level)

        return elems

    def get_local_devices(self):
        return self.ports

    def create_boxes(self, boxes):
        return self.cell.boxes

    def create_elementals(self, elems):
        for e in self.merged_layers:
            elems += e
        return elems

    def create_ports(self, ports):
        for p in self.contacts:
            ports += p
        for p in self.cell.terms:
            ports += p
        return ports

    def create_netlist(self):
        self.g = self.merge

        self.g = self.nodes_combine(algorithm='d2d')
        self.g = self.generate_branches()
        self.detect_dummy_nodes()
        self.g = self.generate_branches()
        self.g = self.nodes_combine(algorithm='d2d')

        # self.plot_netlist(G=self.g, graphname=self.name, labeltext='id')
        return self.g



