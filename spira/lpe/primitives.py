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

    def create_elementals(self, elems):
        super().create_elementals(elems)

        # TODO: Do DRC and ERC checking here.
        # sref_elems = self.cell.get_srefs()
#         for S in self.cell.get_srefs():
#             if isinstance(S.ref, DLayer):
#                 elems += S

#         for S in self.cell.elementals:
#             if isinstance(S.ref, TLayer):
#                 elems += S

        return elems


class Device(__Device__):
    pass


class Gate(__Device__):
    pass


class Circuit(__Device__):
    pass


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
        # super().create_elementals(elems)
        elems += self.devices
        return elems


class __Generator__(__CellContainer__):

    level = param.IntegerField(default=1)
    lcar = param.IntegerField(default=0.01)
    algorithm = param.IntegerField(default=6)

    generate_devices = param.DataField(fdef_name='create_devices')
    device_layers = param.DataField(fdef_name='create_device_layers')

    dev = param.CellField()

    def create_graph(self, elems):

        prim_elems = ElementList()
        for S in elems.sref:
            if isinstance(S.ref, CNLayers):
                for N in S.ref.elementals:
                    prim_elems += N
                    # print(e.ports)
                    # if issubclass(type(e.ref), (NLayer, DLayer, spira.Term)):
                    #     prim_elems += e

        # print(prim_elems)

        for pl in RDD.PLAYER.get_physical_layers(purposes='METAL'):
            # L = Cell(name='{}'.format(pl.layer))
            ply_elems = ElementList()
            for S in elems.sref:
                if isinstance(S.ref, CMLayers):
                    # print(S.ref.elementals)
                    for M in S.ref.elementals:
                        if M.layer == pl.layer:
                            ply_elems += M.polygon
                            # for p in M.elementals:
                            #     if isinstance(p.player, Polygons):
                            #         ply_elems += p.player

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
                    'name': '{}'.format(pl.layer),
                    'layer': pl.layer,
                    'point_data': [mesh_data[2]],
                    'cell_data': [mesh_data[3]],
                    'field_data': [mesh_data[4]]
                }

                mesh = Mesh(
                    polygons=ply_elems,
                    primitives=prim_elems,
                    points=mesh_data[0],
                    cells=mesh_data[1],
                    **params
                )

                # sg = {}
                # sg[pl.layer.name] = mesh.g
                # ng = Graph(subgraphs=sg)
                # # ng.write_graph(graphname='{}'.format(pl.layer.name))
                # ng._plotly_graph(mesh.g, pl.layer.name, 'id')
                # elems += ng



                # L += mesh
                # elems += SRef(L)

                # sg = {}
                # subgraphs = elems.subgraphs
                # for name, g in subgraphs.items():
                #     graph = Graph(subgraphs={name:g})
                #     sg[name] = graph.g
                # ng = Graph(subgraphs=sg)
                # ng.write_graph(graphname='{}'.format(pl.layer.name))
                # elems += ng

    def wrap_references(self, c, c2dmap):
        for e in c.elementals:
            if isinstance(e, SRef):
                if e.ref in c2dmap:
                    e.ref = c2dmap[e.ref]

    def create_devices(self):
        deps = self.cell.dependencies()
        c2dmap = {}

        for key in RDD.DEVICES.keys:
            DeviceTCell = RDD.DEVICES[key].PCELL
            for C in deps:
                print(C)
                print('---------------------\n')

                # plane_elems = ElementList()
                # # # from spira.gdsii import utils
                # # # players = RDD.PLAYER.get_physical_layers(purposes='GROUND')
                # # # plane_elems += utils.get_purpose_layers(self.cell, players)
                # # # # plane_elems += self.cell.elementals[(RDD.GDSII.GPLAYER, 0)]

                # D = Device(cell=C, cell_elems=C.elementals, plane_elems=plane_elems, level=1)

                # print('------ Begin -----------------------------')
                # for e1 in D.elementals:
                #     for e2 in e1.ref.elementals:
                #         print(e2)
                #         if isinstance(e2, spira.SRef):
                #             print(e2.ref.ports)

                # D = Device(cell=C, cell_elems=C.elementals, level=1)
                # for P in DeviceTCell.elementals.sref:
                #     P.ref.create_elementals(D.elementals)

                # print('----- End ------------------------------')
                # for e1 in D.elementals:
                #     for e2 in e1.ref.elementals:
                #         if isinstance(e2, spira.SRef):
                #             print(e2.ref)
                #             print(e2.ref.ports)
                # print('')

                D = Device(cell=C, cell_elems=C.elementals, level=1)
                for P in DeviceTCell.elementals.sref:
                    P.ref.create_elementals(D.elementals)

                c2dmap.update({C: D})

                # self.create_graph(elems=D.elementals)

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
            self.wrap_references(c, c2dmap)

        return SRef(self.dev)

        # new_cell = spira.Cell(name='DLayers')
        # for c in self.cell.dependencies():
        #     self.w2c(c, c2dmap, new_cell)
        # print(new_cell.elementals)

        # return SRef(new_cell)


class GateGenerator(__Generator__):
    """
    Connect to the current library and get the
    primitive metadata from the Rule Deck.
    The pcell device is updated after parsing the
    elementals in the via pcell class.
    """

    structure_gate = param.DataField(fdef_name='create_structure_gate')

    def create_structure_gate(self):
        # self.generate_devices

        # mask = Gate(cell=self.cell, cell_elems=self.cell.elementals)

        dev = self.create_device_layers()
        mask = self.create_devices()

        self.cell.name += 'gate'

        gate = Gate(cell=self.dev, cell_elems=self.dev.elementals)

        for e in mask.ref.elementals:
            if isinstance(e, SRef):
                gate += e

        return SRef(gate)
        # return SRef(dev.ref)
        # return SRef(mask.ref)


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









