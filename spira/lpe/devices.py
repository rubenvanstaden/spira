import spira 
from spira import param, shapes
from spira.lpe.mask import Metal, Native
from spira.lne.net import Net
from demo.pdks import ply
import numpy as np
from copy import copy, deepcopy
from spira.lpe.pcells import __PolygonOperator__
from spira.gdsii.elemental.port import __Port__
from spira.core.mixin.netlist import NetlistSimplifier
from spira.lpe.containers import __CellContainer__


RDD = spira.get_rule_deck()


class Device(__PolygonOperator__):
    """ A Cell encapsulates a set of elementals that
    describes the layout being generated. """

    level = param.IntegerField(default=1)
    lcar = param.IntegerField(default=0.00001)

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

    # def create_ports(self, ports):
    #     for e in self.elementals.flat_copy():
    #         print(e)
    #     return ports

    def create_netlist(self):
        self.g = self.merge

        # self.g = self.nodes_combine(algorithm='d2d')
        # self.g = self.nodes_combine(algorithm='s2s')

        # self.plot_netlist(G=self.g, graphname=self.name, labeltext='id')

        return self.g


# class DeviceLayout(__CellContainer__):

#     metals = param.ElementalListField()
#     contacts = param.ElementalListField()
#     level = param.IntegerField(default=2)

#     def generate_physical_polygons(self, pl):
#         elems = spira.ElementList()
#         R = self.cell.elementals.flat_copy()
#         Rm = R.get_polygons(layer=pl.layer)
#         for i, e in enumerate(Rm):
#             if len(e.polygons[0]) == 4:
#                 alias = 'box_{}_{}_{}'.format(pl.layer.number, self.cell.id, i)
#                 poly = spira.Polygons(shape=e.polygons)
#                 elems += ply.Box(name=alias, player=pl, center=poly.center, w=poly.dx, h=poly.dy, level=self.level)
#             else:
#                 alias = 'ply_{}_{}_{}'.format(pl.layer.number, self.cell.id, i)
#                 elems += ply.Polygon(name=alias, player=pl, points=e.polygons, level=self.level)
#         return elems

#     def create_metals(self, elems):
#         for player in RDD.PLAYER.get_physical_layers(purposes='METAL'):
#             for e in self.generate_physical_polygons(player):
#                 elems += e
#         return elems

#     def create_contacts(self, elems):
#         for player in RDD.PLAYER.get_physical_layers(purposes=['VIA', 'JJ']):
#             for e in self.generate_physical_polygons(player):
#                 elems += e
#         return elems


class DeviceLayout(__CellContainer__):

    metals = param.ElementalListField()
    contacts = param.ElementalListField()
    level = param.IntegerField(default=2)

    def generate_physical_polygons(self, pl):
        elems = spira.ElementList()
        R = self.cell.elementals.flat_copy()
        Rm = R.get_polygons(layer=pl.layer)
        for i, e in enumerate(Rm):
            if len(e.polygons[0]) == 4:
                alias = 'box_{}_{}_{}'.format(pl.layer.number, self.cell.id, i)
                poly = spira.Polygons(shape=e.polygons)
                elems += ply.Box(name=alias, player=pl, center=poly.center, w=poly.dx, h=poly.dy, level=self.level)
            else:
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

        # for name, player in RDD.PLAYER.items:
        #     print(player)
        #     R = self.cell.elementals.flat_copy()
        #     Rm = R.get_polygons(layer=player.layer)

        return elems

    def create_elementals(self, elems):

        metals = Metal(elementals=self.metals, level=self.level)
        natives = Native(elementals=self.contacts, level=self.level)

        elems += spira.SRef(metals)
        elems += spira.SRef(natives)

        for key in RDD.VIAS.keys:
            RDD.VIAS[key].PCELL.create_elementals(elems)

        return elems

    def determine_type(self):
    # def what_type(self):
        self.__type__ = None

        # for key in RDD.VIAS.keys:
        #     # print(key)
        #     default_via = RDD.VIAS[key].DEFAULT()
        #     # print(default_via)

        #     is_possibly_match = True
        #     if len(self.contacts) != len(default_via.contacts):
        #         is_possibly_match = False
        #     if len(self.metals) != len(default_via.metals):
        #         is_possibly_match = False
        #     print(is_possibly_match)
        #     # print(default_via.ports)

        #     if is_possibly_match:
        #         default_ports = spira.ElementList()
        #         for e in default_via.elementals.flatten():
        #             if isinstance(e, spira.Port):
        #                 if e.name != 'P_metal':
        #                     default_ports += e.gdslayer.node_id
        #         print(default_ports)
        #         print('--------------------------')

        #         self_ports = spira.ElementList()
        #         for e in self.elementals.flatten():
        #             if isinstance(e, spira.Port):
        #                 if e.name != 'P_metal':
        #                     self_ports += e.gdslayer.node_id
        #         print(self_ports)

        #         # for p1 in defa
        #         if set(default_ports) == set(self_ports):
        #             print('YESSSSSSSSSSSSSSSSSSSSS')
        #             print(RDD.VIAS[key].DEFAULT.__name_prefix__)
                    # self.__type__ = RDD.VIAS[key].DEFAULT.__name_prefix__
        #             self.__type__ = key

        #         print('')



        for key in RDD.DEVICES.keys:
            print(key)
            default_via = RDD.DEVICES[key].PCELL()
            is_possibly_match = True
            
            # if len(self.contacts) != len(default_via.contacts):
            #     is_possibly_match = False
            # if len(self.metals) != len(default_via.metals):
            #     is_possibly_match = False
            # print(is_possibly_match)

            if is_possibly_match:
                default_ports = spira.ElementList()
                for e in default_via.elementals.flatten():
                    if isinstance(e, spira.Port):
                        if e.name != 'P_metal':
                            default_ports += e.gdslayer.node_id
                # print(default_ports)
                # print('--------------------------')

                self_ports = spira.ElementList()
                for e in self.elementals.flatten():
                    if isinstance(e, spira.Port):
                        if e.name != 'P_metal':
                            self_ports += e.gdslayer.node_id
                # print(self_ports)

                # # for p1 in defa
                # if set(default_ports) != set(self_ports):
                #     is_possibly_match = False

            if is_possibly_match:
                default_ports = spira.ElementList()
                for e in default_via.contacts:
                    print(e.player)
                    default_ports += e.player

                print('--------------------------')

                self_ports = spira.ElementList()
                for e in self.contacts:
                    print(e.player)
                    self_ports += e.player

                if set(default_ports) != set(self_ports):
                    is_possibly_match = False

            if is_possibly_match:
                print('YESSSSSSSSSSSSSSSSSSSSS')
                self.__type__ = key
            print('')




class Gate(__PolygonOperator__):

    __mixins__ = [NetlistSimplifier]
    lcar = param.IntegerField(default=0.1)

    def create_metals(self, elems):

        for player in RDD.PLAYER.get_physical_layers(purposes='METAL'):

            metal_elems = spira.ElementList()
            R = self.cell.routes.flat_copy()
            B = self.cell.boxes.flat_copy()
            Rm = R.get_polygons(layer=player.layer)
            Bm = B.get_polygons(layer=player.layer)

            for i, e in enumerate([*Rm, *Bm]):
            # for i, e in enumerate([*Rm]):
                alias = 'ply_{}_{}_{}'.format(player.layer.number, self.cell.id, i)
                elems += ply.Polygon(name=alias, player=player, points=e.polygons, level=self.level)

        return elems

    def get_local_devices(self):
        ports = deepcopy(self.ports)
        # for p in self.cell.terms:
        for p in self.cell.terminals:
            ports += p
        return ports

    def create_boxes(self, boxes):
        return self.cell.boxes

    def create_elementals(self, elems):
        for e in self.merged_layers:
            elems += e
        return elems

    def create_ports(self, ports):
        # for p in self.contacts:
        #     ports += p
        # for p in self.cell.terms:
        #     ports += p
        return ports

    def create_netlist(self):
        self.g = self.merge

        # Algorithm 1
        self.g = self.nodes_combine(algorithm='d2d')
        # Algorithm 2
        # self.g = self.generate_branches()
        # # Algorithm 3
        # self.detect_dummy_nodes()
        # # Algorithm 4
        # self.g = self.generate_branches()
        # # Algorithm 5
        # self.g = self.nodes_combine(algorithm='d2d')

        self.plot_netlist(G=self.g, graphname=self.name, labeltext='id')
        return self.g



