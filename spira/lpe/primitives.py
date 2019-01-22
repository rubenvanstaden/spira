import gdspy
import networkx as nx

from copy import copy, deepcopy
from spira import settings

import spira
from spira import param
from spira import settings
from spira.gdsii import utils
from spira.rdd import get_rule_deck

from spira.gdsii.cell import Cell
from spira.gdsii.layer import Layer
from spira.gdsii.elemental.polygons import Polygons
from spira.gdsii.elemental.label import Label
from spira.gdsii.elemental.port import Port
from spira.gdsii.elemental.sref import SRef
from spira.lne.graph import Graph
from spira.lne.mesh import Mesh
from spira.lne.geometry import Geometry
from spira.core.lists import ElementList

from spira.lpe.layers import *
from spira.lpe.structure import __StructureCell__
from spira.lpe.containers import __CellContainer__


RDD = get_rule_deck()


class __Device__(__StructureCell__):

    level = param.IntegerField(default=1)
    lcar = param.IntegerField(default=0.1)
    algorithm = param.IntegerField(default=6)

    dev = param.CellField()

    def create_elementals(self, elems):
        super().create_elementals(elems)
        return elems

    def create_nets(self, nets):

        print('\n---------------- Nets --------------------')

        ports = self.ports
        elems = self.elementals

        prim_elems = ElementList()
        for S in elems.sref:
            if isinstance(S.ref, (CNLayers, spira.Port, spira.Term)):
                for N in S.ref.elementals:
                    prim_elems += N

        if ports is not None:
            for P in ports:
                prim_elems += P

        print(self.cell.elementals)
        # print(elems)
        # print(ports)
        # print(prim_elems)

        # device_elems = ElementList()
        # flat_elems = self.dev.flat_copy()
        # # for e in self.cell.elementals.sref:
        # for e in flat_elems:
        #     # if isinstance(e.ref, BoundingDevice):
        #     print(e)
        #     # if isinstance(e, spira.Polygons):
        #     #     print(e)
        #         # print(e.ref.elementals.sref)
        #         # # (0, [SPiRA: SRef] ("DLayer-2", at [0, 0], srefs 0, cells 0, polygons 3, ports 0, labels 0))
        #         # for s in e.ref.elementals.sref:
        #         #     for p in s.ref.elementals:
        #         #         # p.center = p.center + s.midpoint
        #         #         p.move(midpoint=p.center, destination=e.midpoint)
        #         #         p.move(midpoint=p.center, destination=s.midpoint)
        #         #         device_elems += p

        device_elems = ElementList()
        for e in self.dev.elementals:
            print(e)
            device_elems += e
            self.elementals += e

        print('--- Device Elementals ===')
        print(device_elems)
        print('')

        for pl in RDD.PLAYER.get_physical_layers(purposes='METAL'):
            ply_elems = ElementList()
            for S in elems.sref:
                if isinstance(S.ref, CMLayers):
                    for M in S.ref.elementals:
                        if M.layer.is_equal_number(pl.layer):
                            if M.polygon.gdslayer.datatype == 2:
                            # if M.polygon.gdslayer.datatype == 1:
                                ply_elems += M.polygon

            if ply_elems:
                geom = Geometry(
                    name='{}'.format(pl.layer.number),
                    lcar=self.lcar,
                    algorithm=self.algorithm,
                    layer=pl.layer,
                    polygons=ply_elems
                )

                mesh_data = geom.create_mesh

                params = {
                    'name': '{}_{}'.format(pl.layer.name, pl.layer),
                    'layer': pl.layer,
                    'point_data': [mesh_data[2]],
                    'cell_data': [mesh_data[3]],
                    'field_data': [mesh_data[4]]
                }

                mesh = Mesh(
                    polygons=ply_elems,
                    device_polygon=device_elems,
                    primitives=prim_elems,
                    points=mesh_data[0],
                    cells=mesh_data[1],
                    **params
                )
                nets += mesh.g
        return nets


class Device(__Device__):
    pass


class Gate(__Device__):
    pass


class Circuit(__Device__):
    pass


class DeviceMLayers(__CellContainer__):
    """
    Add a GROUND bbox to Device for primitive and
    DRC detection, since GROUND is only in Mask Cell.
    """

    level = param.IntegerField(default=1)

    device_elems = param.ElementListField()

    devices = param.DataField(fdef_name='create_device_layers')

    def create_device_layers(self):
        # box = self.cell.bbox
        # box.move(midpoint=box.center, destination=(0,0))

        B = DLayer(points=self.cell.pbox, device_elems=self.cell.elementals.flat_copy())
        Bs = SRef(B)
        # Bs.move(midpoint=(0,0), destination=self.cell.bbox.center)

        return Bs

    def create_elementals(self, elems):
        # super().create_elementals(elems)
        elems += self.devices
        return elems


class BoundingDevice(__CellContainer__):
    """
    Add a GROUND bbox to Device for primitive and
    DRC detection, since GROUND is only in Mask Cell.
    """

    level = param.IntegerField(default=1)

    device_elems = param.ElementListField()

    devices = param.DataField(fdef_name='create_device_layers')

    def create_device_layers(self):
        # box = self.cell.bbox
        # box.move(midpoint=box.center, destination=(0,0))

        B = DLayer(points=self.cell.pbox, device_elems=self.cell.elementals.flat_copy())
        Bs = SRef(B)
        # Bs.move(midpoint=(0,0), destination=self.cell.bbox.center)

        return Bs

    def create_elementals(self, elems):
        elems += self.devices
        return elems


class __Generator__(__CellContainer__):

    level = param.IntegerField(default=1)
    # lcar = param.IntegerField(default=0.01)
    # algorithm = param.IntegerField(default=6)

    generate_devices = param.DataField(fdef_name='create_devices')
    device_layers = param.DataField(fdef_name='create_device_layers')

    dev = param.CellField()

    def wrap_references(self, c, c2dmap):
        for e in c.elementals:
            if isinstance(e, SRef):
                print(e)
                print(e.midpoint)
                print('')
                if e.ref in c2dmap:
                    e.ref = c2dmap[e.ref]

    def create_devices(self):
        deps = self.cell.dependencies()
        c2dmap = {}

        for key in RDD.DEVICES.keys:
            DeviceTCell = RDD.DEVICES[key].PCELL
            for C in deps:
                D = Device(cell=C, cell_elems=C.elementals, level=1)
                for P in DeviceTCell.elementals.sref:
                    P.ref.create_elementals(D.elementals)
                c2dmap.update({C: D})
                # D.netlist

        for c in self.cell.dependencies():
            self.wrap_references(c, c2dmap)

        return SRef(self.cell)

    def create_device_layers(self):
        c2dmap = {}
        self.dev = deepcopy(self.cell)
        deps = self.dev.dependencies()

        for key in RDD.DEVICES.keys:
            for C in deps:
                B = BoundingDevice(cell=C)
                c2dmap.update({C: B})

        for c in self.dev.dependencies():
            print(c)
            self.wrap_references(c, c2dmap)

        return SRef(self.dev)

    def create_bounding_layers(self):
        cell = spira.Cell(name='Box')
        print(self.cell.elementals.sref)
        for s in self.cell.elementals.sref:

            # setter = {}

            # for p in self.cell.elementals.polygons:
            #     layer = p.gdslayer.number
            #     setter[layer] = 'not_set'

            # for p in self.cell.elementals.polygons:
            #     for pl in RDD.PLAYER.get_physical_layers(purposes=['METAL', 'GND']):
            #         if pl.layer == p.gdslayer:
            #             if setter[pl.layer.number] == 'not_set':
            #                 l1 = Layer(name='BoundingBox', number=pl.layer.number, datatype=9)
            #                 # l1 = Layer(name='BoundingBox', number=pl.layer.number, datatype=8)
            #                 elems += Polygons(shape=self.points, gdslayer=l1)
            #                 setter[pl.layer.number] = 'already_set'

            ply = spira.Polygons(
                shape=s.ref.pbox,
                gdslayer=spira.Layer(name='Boundary', number=80)
            )
            # FIXME:Why from the origin?
            ply.move(midpoint=(0,0), destination=s.midpoint)
            # ply.move(midpoint=ply.center, destination=s.midpoint)
            cell += ply
        return cell


def add_ports_to_bounding_device(cell, gate):

    # flat_elems = cell.elementals.flat_copy()
    # for pl in RDD.PLAYER.get_physical_layers(purposes='METAL'):
    #     metal_elems = flat_elems.get_polygons(layer=pl.layer)
    #     if metal_elems:
    #         for e in metal_elems:
    #             print(e)

    for g in cell.elementals:
        if isinstance(g, spira.Polygons):
            print(g)
            for c in cell.elementals.sref:
                for S in c.ref.elementals:
                    if isinstance(S.ref, CMLayers):
                        for M in S.ref.elementals:
                            if (M.polygon & g) and (g.is_equal_layers(M.polygon)):
                                gate.ports += spira.Port(
                                    name=M.polygon.gdslayer.name, 
                                    midpoint=M.polygon.center + c.midpoint,
                                    gdslayer=spira.Layer(number=g.gdslayer.number, datatype=100)
                                )
                                print(M.polygon)
            print('')

    # for c in cell.elementals.sref:
    #     print(c)
    #     for S in c.ref.elementals:
    #         if isinstance(S.ref, CMLayers):
    #             for M in S.ref.elementals:
    #                 print(M)


class GateGenerator(__Generator__):
    """
    Connect to the current library and get the
    primitive metadata from the Rule Deck.
    The pcell device is updated after parsing the
    elementals in the via pcell class.
    """

    structure_gate = param.DataField(fdef_name='create_structure_gate')

    def create_structure_gate(self):

        dev = self.create_device_layers()
        mask = self.create_devices()
        cell = self.create_bounding_layers()

        self.cell.name += 'gate'

        gate = Gate(dev=cell, cell=dev.ref, cell_elems=dev.ref.elementals, level=2)

        # for e in mask.ref.elementals:
        #     if isinstance(e, SRef):
        #         gate += e

        add_ports_to_bounding_device(self.cell, gate)

        gate.netlist

        return SRef(gate)
        # return SRef(dev.ref)
        # return SRef(self.dev)


class CircuitGenerator(GateGenerator):

    structure_circuit = param.DataField(fdef_name='create_structure_circuit')

    def create_structure_circuit(self):
        self.structure_gate

        mask = Circuit(cell=self.cell, cell_elems=self.cell.elementals)
        return SRef(mask)


class MaskGenerator(CircuitGenerator):

    structure_mask = param.DataField(fdef_name='create_structure_mask')

    def create_structure_mask(self):
        self.structure_circuit

        mask = Mask(cell=self.cell, cell_elems=self.cell.elementals)
        return SRef(mask)

    def create_elementals(self, elems):
        return elems


class SLayout(MaskGenerator):
    """ The StructureLayout is a converted layout
    that takes designed elementals and wraps them
    with different generators.

    Examples
    --------
    >>> sl = SLayout()
    """

    def create_elementals(self, elems):

        # Primitives
        if self.level == 0:
            elems += SRef(self.cell)
        # Devices
        elif self.level == 1:
            elems += self.generate_devices
        # Gates
        elif self.level == 2:
            elems += self.structure_gate
        # Circuits
        elif self.level == 3:
            elems += self.structure_circuit
        # Mask
        elif self.level == 4:
            elems += self.structure_mask

        return elems









