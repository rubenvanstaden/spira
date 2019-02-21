import spira
import numpy as np
from spira import param, shapes
from spira.lpe import mask
from demo.pdks import ply
from spira.lpe.containers import __CellContainer__, __NetContainer__, __CircuitContainer__
from spira.lne.net import Net
from copy import copy, deepcopy
from spira.lpe.mask_layers import Metal
from spira.lpe.devices import Device, DeviceLayout
from spira.lpe.devices import Gate
from spira.lpe.pcells import __PolygonOperator__

from spira.lgm.route.manhattan_base import Route
from spira.lgm.route.basic import RouteShape, RouteBasic
from spira.lpe.pcells import  __NetlistCell__
from spira.lpe.boxes import BoundingBox
from halo import Halo


RDD = spira.get_rule_deck()


class Circuit(__CircuitContainer__):
    """ Deconstructs the different hierarchies in the cell. """

    lcar = param.IntegerField(default=0.1)
    algorithm = param.IntegerField(default=6)
    level = param.IntegerField(default=1)

    mask = param.DataField(fdef_name='create_mask')
    terminals = param.ElementalListField()

    def create_mask(self):
        cell = None
        if self.level == 2:
            cell = LayoutConstructor(cell=self)
        elif self.level == 3:
            pass
        elif self.level == 4:
            pass
        return cell

    def create_devices(self, elems):
        # FIXME: Assumes level 1 hierarchical cell.
        if self.cell is None:
            for S in self.elementals.sref:
                if issubclass(type(S.ref), Device):
                    elems += S
        else:
            c2dmap = {}
            deps = self.cell.dependencies()
            for key in RDD.DEVICES.keys:
                DeviceTCell = deepcopy(RDD.DEVICES[key].PCELL)
                DeviceTCell.center = (0,0)
                for C in deps:
                    if 'jj' in C.name:
                        L = DeviceLayout(name=C.name, cell=C, level=1)
                        D = DeviceTCell(metals=L.metals, contacts=L.contacts)
                        c2dmap.update({C: D})
                    elif 'via' in C.name:
                        L = DeviceLayout(name=C.name, cell=C, level=1)
                        D = DeviceTCell(metals=L.metals, contacts=L.contacts)
                        c2dmap.update({C: D})
            for c in self.cell.dependencies():
                self.__cell_swapper__(elems, c, c2dmap)
        return elems

    def create_boxes(self, boxes):
        """ Generate bounding boxes around each Device. """
        # FIXME: Assumes level 1 hierarchical cell.
        for S in self.devices:
            boxes += BoundingBox(
                S=S 
                # cell=S.ref,
                # midpoint=S.midpoint,
                # rotation=S.rotation,
                # reflection=S.reflection,
                # magnification=S.magnification
            )
        return boxes

    def create_routes(self, routes):
        if self.cell is not None:
            elems = spira.ElementList()
            cell = spira.Cell(name='RouteCell')
            for e in self.cell.elementals:
                # print(e)
                if issubclass(type(e), spira.Polygons):
                    cell += e
                    # elems += e
            # R = Route(elementals=elems)
            elems += spira.SRef(cell)
            R = Route(elementals=elems)
            routes += spira.SRef(R)
        return routes

    def create_ports(self, ports):

        # FIXME!!! Needed for terminal detection in the Mesh.
        if self.cell is not None:
            flat_elems = self.cell.flat_copy()
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
                                length=port.dy,
                                # width=port.dy,
                                # length=port.dx,
                                midpoint=label.position
                            )

        return ports

    def create_terminals(self, ports):

        # FIXME!!! Needed for terminal detection in the Mesh.
        if self.cell is not None:
            flat_elems = self.cell.flat_copy()
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
                                length=port.dy,
                                # width=port.dy,
                                # length=port.dx,
                                midpoint=label.position
                            )

        return ports

    def create_netlist(self):

        spinner = Halo(text='Extracting netlist', spinner='dots')
        spinner.start()

        self.mask.netlist

        spinner.succeed('Netlist extracted.')
        spinner.stop()


class LayoutConstructor(__NetlistCell__):
    """ Constructs a single cell from the hierarchical 
    levels generated by the Circuit class. """

    def create_contacts(self, contacts):
        for R in self.cell.routes:
            print(R)
            # pp = R.ref.elementals.polygons
            ps = R.ref.elementals[0]
            pp = ps.ref.elementals.polygons
            print(pp)
            if len(pp) > 0:
                g = pp[0]
                for i, D in enumerate(self.cell.devices):
                    for S in D.ref.elementals:
                        if isinstance(S.ref, Metal):
                            for M in S.ref.elementals:

                                ply = deepcopy(M.polygon)
                                # ply.move(midpoint=ply.center, destination=S.midpoint)
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
                                #     P = M.metal_port._copy()
                                #     P.connect(D, ply)
                                #     d = D.midpoint
                                #     P.move(midpoint=P.midpoint, destination=d)
                                #     P.node_id = '{}_{}'.format(P.node_id, i)
                                #     contacts += P
        return contacts

    def create_elementals(self, elems):
        elems += spira.SRef(Gate(cell=self.cell))
        for e in self.cell.devices:
            elems += e
        return elems

    def create_nets(self, nets):
        # for i, s in enumerate(self.elementals.sref):
        for i, s in enumerate(self.cell.devices):

            if issubclass(type(s.ref), Device):
                g = s.ref.netlist
                if g is not None:
                    for n in g.nodes():
                        if 'device' in g.node[n]:
                            g.node[n]['device'].node_id = '{}_{}_{}'.format(
                                s.ref.name,
                                g.node[n]['device'].node_id,
                                i
                            )
                        else:
                            g.node[n]['surface'].node_id = '{}_{}_{}'.format(
                                s.ref.name,
                                g.node[n]['surface'].node_id,
                                i
                            )
                            g.node[n]['device'] = g.node[n]['surface']

        for i, s in enumerate(self.elementals.sref):
            g = s.ref.netlist
            if g is not None:
                for n in g.nodes():
                    p = np.array(g.node[n]['pos'])
                    m = np.array(s.midpoint)
                    g.node[n]['pos'] = p + m
                nets += g
        return nets

    def create_netlist(self):

        self.g = self.merge

        # self.g = self.nodes_combine(algorithm='d2s')
        # self.g = self.nodes_combine(algorithm='d2d')
        # self.g = self.nodes_combine(algorithm='s2s')

        self.plot_netlist(G=self.g, graphname=self.name, labeltext='id')

    def create_ports(self, ports):

        gate = Gate(cell=self.cell)

        # terminals = spira.ElementList()
        # if self.cell is not None:
        #     flat_elems = self.cell.flat_copy()
        #     port_elems = flat_elems.get_polygons(layer=RDD.PURPOSE.TERM)
        #     label_elems = flat_elems.labels
        #     for port in port_elems:
        #         for label in label_elems:
        #             lbls = label.text.split(' ')
        #             s_p1, s_p2 = lbls[1], lbls[2]
        #             p1, p2 = None, None
        #             for m1 in RDD.PLAYER.get_physical_layers(purposes=['METAL', 'GND']):
        #                 if m1.layer.name == s_p1:
        #                     p1 = spira.Layer(name=lbls[0],
        #                         number=m1.layer.number,
        #                         datatype=RDD.GDSII.TEXT
        #                     )
        #                 if m1.layer.name == s_p2:
        #                     p2 = spira.Layer(name=lbls[0],
        #                         number=m1.layer.number,
        #                         datatype=RDD.GDSII.TEXT
        #                     )
        #             if p1 and p2 :
        #                 if label.encloses(ply=port.polygons[0]):
        #                     terminals += spira.Term(
        #                         name=label.text,
        #                         layer1=p1, layer2=p2,
        #                         width=port.dx,
        #                         length=port.dy,
        #                         # width=port.dy,
        #                         # length=port.dx,
        #                         midpoint=label.position
        #                     )

        for pl in RDD.PLAYER.get_physical_layers(purposes='METAL'):
            # for m in gate.get_metal_polygons(pl):
            for m in gate.get_metal_polygons_for_ports(pl):
                for p in m.ports:
                    for t in self.cell.terminals:

                        edgelayer = deepcopy(p.gdslayer)
                        edgelayer.datatype = 82

                        arrowlayer = deepcopy(p.gdslayer)
                        arrowlayer.datatype = 83

                        if p.encloses_midpoint(polygon=t.edge.polygons):
                            ports += spira.Term(
                                name=t.name,
                                midpoint=p.midpoint,
                                orientation=p.orientation,
                                edgelayer=edgelayer,
                                arrowlayer=arrowlayer,
                                width=p.width,
                                length=p.length
                            )

        return ports
