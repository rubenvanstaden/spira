import time
import numpy as np
import spira.all as spira
from spira.yevon.geometry import shapes
from spira.yevon import process as pc
from spira.netex.containers import __CellContainer__, __NetContainer__, __CircuitContainer__
from copy import copy, deepcopy
from spira.netex.structure import Structure

from spira.yevon.geometry.route.routing import Route
from spira.yevon.geometry.route.route_shaper import RouteSimple, RouteGeneral
from spira.netex.netlist import NetlistSimplifier
from spira.netex.structure import __NetlistCell__
from spira.netex.boxes import BoundingBox
from halo import Halo

import networkx as nx
from spira.yevon import utils
from spira.yevon.utils import boolean
from spira.yevon.rdd import get_rule_deck

from spira.core.param.variables import *


__all__ = ['Circuit']


RDD = get_rule_deck()


class MetalNet(NetlistSimplifier):
    pass


class RouteToStructureConnector(__CircuitContainer__, Structure):
    """  """

    def create_contacts(self, boxes):
        # start = time.time()
        # self.unlock_ports()
        # for D in self.structures:
        #     if isinstance(D, spira.SRef):
        #         B = BoundingBox(S=D)
        #         boxes += B
        # end = time.time()
        return boxes

    def unlock_ports(self):
        for S in self.structures:
            print('\n----------- Main ----------------')
            print(S)
            print('----------- END ----------------\n')
            S.unlock_overlapping_ports(D=self, initial=True)

        # for D in self.structures:
        #     for S in self.structures:
        #         if id(S) != id(D):
        #             for R in S.ref.routes:
        #                 self.__unlock_device_edges__(R, D)

        # for D in self.structures:
        #     for R in self.routes:
        #         # self.__unlock_route_edges__(R, D)
        #         self.__unlock_device_edges__(R, D)

    # def __unlock_route_edges__(self, R, D):
    #     for M in D.ref.metals:
    #         M_ply = M.polygon
    #         M_ply.transform(D.tf)
    #         for key, port in R.instance_ports.items():
    #             for mp in M_ply.shape.points:
    #                 if port.encloses(mp):
    #                     R.port_locks[port.key] = False

    # def __unlock_device_edges__(self, R, D):

    #     def r_func(R, D):
    #         if issubclass(type(R), pc.ProcessLayer):
    #             pp = R
    #             R_ply = pp.polygon
    #             for key, port in D.instance_ports.items():
    #                 if isinstance(port, (spira.Terminal, spira.spira.EdgeTerminal)):
    #                     if port.gds_layer.number == pp.ps_layer.layer.number:
    #                         if port.edge.ply_area != 0:
    #                             if R_ply & port.edge:
    #                                 print('pppppppppppppppppppppp')
    #                                 route_key = (pp.node_id, pp.ps_layer.layer.number)
    #                                 D.port_connects[key] = route_key
    #                                 D.port_locks[key] = False
    #         else:
    #             for pp in R.ref.metals:
    #                 if isinstance(pp, pc.ProcessLayer):
    #                     R_ply = pp.polygon
    #                     for key, port in D.instance_ports.items():
    #                         if isinstance(port, (spira.Terminal, spira.spira.EdgeTerminal)):
    #                             if port.gds_layer.number == pp.ps_layer.layer.number:
    #                                 if port.edge.ply_area != 0:
    #                                     if R_ply & port.edge:
    #                                         route_key = (pp.node_id, pp.ps_layer.layer.number)
    #                                         D.port_connects[key] = route_key
    #                                         D.port_locks[key] = False

    #     if isinstance(R, spira.ElementList):
    #         for r in R:
    #             r_func(r, D)
    #     else:
    #         r_func(R, D)


class Circuit(RouteToStructureConnector):
    """ Deconstructs the different hierarchies in the cell. """

    __mixins__ = [NetlistSimplifier]

    algorithm = IntegerField(default=6)
    level = IntegerField(default=2)
    lcar = FloatField(default=10.0)

    def create_elementals(self, elems):

        # for e in self.routes:
        #     elems += e

        for e in self.structures:
            elems += e

        for e in self.route_layers:
            elems += e

        # for e in self.merged_layers:
        #     elems += e

        return elems

    def create_primitives(self, elems):
        for p in self.ports:
            elems += p
        for p in self.terminals:
            elems += p
        return elems

    def create_structures(self, structs):
        if self.cell is not None:
            for S in self.cell.elementals:
                if isinstance(S, spira.SRef):
                    structs += S
        return structs

    def create_routes(self, routes):
        if self.cell is not None:
            r = Route(cell=self.cell)
            routes += spira.SRef(r)
        return routes

    def create_metals(self, elems):
        R = self.routes.flat_copy()
        B = self.contacts.flat_copy()
        for ps_layer in RDD.PLAYER.get_physical_layers(purposes='METAL'):
            Rm = R.get_polygons(layer=ps_layer.layer)
            Bm = B.get_polygons(layer=ps_layer.layer)
            for i, e in enumerate([*Rm, *Bm]):
                alias = 'ply_{}_{}_{}'.format(ps_layer.layer.number, self.__class__.__name__, i)
                elems += pc.Polygon(name=alias, ps_layer=ps_layer, points=e.polygons, level=self.level)
        return elems

    def create_terminals(self, ports):

        # FIXME!!! Needed for terminal detection in the Mesh.
        if self.cell is not None:
            cell = deepcopy(self.cell)
            flat_elems = cell.flat_copy()
            port_elems = flat_elems.get_polygons(layer=RDD.PURPOSE.TERM)
            label_elems = flat_elems.labels
            for port in port_elems:
                for label in label_elems:
                    lbls = label.text.split(' ')
                    s_p1, s_p2 = lbls[1], lbls[2]
                    p1, p2 = None, None
                    for m1 in RDD.PLAYER.get_physical_layers(purposes=['METAL', 'GND']):
                        if m1.layer.name == s_p1:
                            p1 = spira.Layer(name=lbls[0],
                                number=m1.layer.number,
                                datatype=RDD.GDSII.TEXT
                            )
                        if m1.layer.name == s_p2:
                            p2 = spira.Layer(name=lbls[0],
                                number=m1.layer.number,
                                datatype=RDD.GDSII.TEXT
                            )
                    if p1 and p2 :
                        for pts in port.polygons:
                            # if label.encloses(ply=port.polygons[0]):
                            if label.encloses(ply=pts):
                                ports += spira.Terminal(
                                    name=label.text,
                                    layer1=p1, layer2=p2,
                                    width=port.dx,
                                    midpoint=label.position
                                )

        return ports
