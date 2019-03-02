import spira
import time
import numpy as np
from spira import param, shapes
from spira.lpe import mask
from demo.pdks import ply
from spira.lpe.containers import __CellContainer__, __NetContainer__, __CircuitContainer__
from spira.lne.net import Net
from copy import copy, deepcopy
from spira.lpe.devices import Device
from spira.lpe.pcells import Structure

from spira.lgm.route.manhattan_base import Route
from spira.lgm.route.basic import RouteShape, RouteBasic
from spira.core.mixin.netlist import NetlistSimplifier
from spira.lpe.pcells import __NetlistCell__
from spira.lpe.boxes import BoundingBox
from halo import Halo


RDD = spira.get_rule_deck()


class RouteToStructureConnector(__CircuitContainer__, Structure):
    """  """

    def create_contacts(self, boxes):
        start = time.time()
        print('[*] Connecting routes with devices')
        self.unlock_ports()
        for D in self.structures:
            B = BoundingBox(S=D)
            boxes += B
        end = time.time()
        print('Block calculation time {}:'.format(end - start))
        return boxes

    def unlock_ports(self):
        for R in self.routes:
            for D in self.structures:
                self._activate_route_edges(R, D)
                self._activate_device_edges(R, D)

    def _activate_route_edges(self, R, D):
        for S in D.ref.metals:
            M = deepcopy(S)
            M_ply = M.polygon
            tf = {
                'midpoint': D.midpoint,
                'rotation': D.rotation,
                'magnification': D.magnification,
                'reflection': D.reflection
            }
            M_ply.transform(tf)
            for key, port in R.ports.items():
                for mp in M_ply.shape.points:
                    if port.encloses(mp):
                        R.port_locks[port.key] = False

    def _activate_device_edges(self, R, D):
        for S in R.ref.metals:
        # for S in R.ref.merged_layers:
            R_ply = S.polygon
            for key, port in D.ports.items():
                if isinstance(port, spira.Term):
                    # print(port)
                    # print(key)
                    # print('')
                    if port.gdslayer.number == R_ply.gdslayer.number:
                        if R_ply & port.edge:
                            D.port_locks[key] = False
                            D.port_connects[key] = S
                            # print(port.connections)
                            # print(S)
                            # print(key)
                            # print('')


class Circuit(RouteToStructureConnector):
    """ Deconstructs the different hierarchies in the cell. """

    __mixins__ = [NetlistSimplifier]

    lcar = param.IntegerField(default=0.1)
    # lcar = param.IntegerField(default=100)
    algorithm = param.IntegerField(default=6)
    level = param.IntegerField(default=1)

    def create_elementals(self, elems):
        for e in self.merged_layers:
            elems += e
        return elems

    def create_structures(self, structs):
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
        for player in RDD.PLAYER.get_physical_layers(purposes='METAL'):
            Rm = R.get_polygons(layer=player.layer)
            Bm = B.get_polygons(layer=player.layer)
            for i, e in enumerate([*Rm, *Bm]):
                alias = 'ply_{}_{}_{}'.format(player.layer.number, self.cell.node_id, i)
                elems += ply.Polygon(name=alias, player=player, points=e.polygons, level=self.level)
        return elems

    def create_primitives(self, elems):
        elems = deepcopy(self.ports)
        for p in self.terminals:
            elems += p
        return elems

    def create_ports(self, ports):

        print('\n[*] Calculate Layout ports')

        start = time.time()

        self.unlock_ports()

        for D in self.structures:
            for name, port in D.ports.items():
                if port.locked is False:
                    edgelayer = deepcopy(port.gdslayer)
                    edgelayer.datatype = 100
                    ports += port.modified_copy(edgelayer=edgelayer)

        for R in self.routes:
            for name, port in R.ports.items():
                if port.locked is False:
                    edgelayer = deepcopy(port.gdslayer)
                    edgelayer.datatype = 101
                    ports += port.modified_copy(edgelayer=edgelayer)

        # -------------------------------------------------------------------

        # for p in self.terminals:
        #     ports += p

        # for pl in RDD.PLAYER.get_physical_layers(purposes='METAL'):
        #     for m in self.get_metals(pl):
        #         for p in m.ports:
        #             for t in self.terminals:
        #                 edgelayer = deepcopy(p.gdslayer)
        #                 edgelayer.datatype = 82
        #                 arrowlayer = deepcopy(p.gdslayer)
        #                 arrowlayer.datatype = 83
        #                 if p.encloses_midpoint(points=t.edge.polygons):
        #                     ports += spira.Term(
        #                         name=t.name,
        #                         midpoint=p.midpoint,
        #                         orientation=p.orientation,
        #                         edgelayer=edgelayer,
        #                         arrowlayer=arrowlayer,
        #                         width=p.width,
        #                     )

        end = time.time()
        print('Layout port calculation time {}:'.format(end - start))

        return ports

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
                        if label.encloses(ply=port.polygons[0]):
                            ports += spira.Term(
                                name=label.text,
                                layer1=p1, layer2=p2,
                                width=port.dx,
                                # length=port.dy,
                                midpoint=label.position
                            )

        return ports

    def create_netlist(self):
        self.g = self.merge

        # Algorithm 1
        self.g = self.nodes_combine(algorithm='d2d')
        # Algorithm 2
        self.g = self.generate_branches()
        # Algorithm 3
        self.detect_dummy_nodes()
        # Algorithm 4
        self.g = self.generate_branches()
        # Algorithm 5
        self.g = self.nodes_combine(algorithm='b2b')

        self.plot_netlist(G=self.g, graphname=self.name, labeltext='id')

        return self.g


    def create_nets(self, nets):
        for pl in RDD.PLAYER.get_physical_layers(purposes='METAL'):
            polygons = self.get_metals(pl)
            if len(polygons) > 0:
                net = Net(
                    name='{}_{}'.format(self.name, pl.layer.number),
                    lcar=self.lcar,
                    level=self.level,
                    algorithm=self.algorithm,
                    layer=pl.layer,
                    polygons=polygons,
                    route_nodes=self.routes,
                    primitives=self.primitives,
                    bounding_boxes=self.contacts
                )
                nets += net.graph
        return nets


