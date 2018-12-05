
# import spira
import gdspy
import networkx as nx

from copy import copy, deepcopy
from spira import settings

from spira.rdd import get_rule_deck
from spira.kernel.elemental.polygons import UnionPolygons
from spira.kernel import parameters as param
from spira.kernel import utils

from spira.kernel.cell import Cell
from spira.kernel.layer import Layer
from spira.kernel.elemental.polygons import Polygons
from spira.kernel.elemental.label import Label
from spira.kernel.elemental.port import Port
from spira.kernel.elemental.sref import SRef
from spira.lne.graph import Graph
from spira.lne.mesh import Mesh
from spira.lne.geometry import Geometry
from spira.kernel.parameters.field.element_list import ElementList

from spira.lpe.containers import __CellContainer__
from spira.lpe.layers import *
from spira.lgm.booleans import merge
from spira.lpe.structure import __StructureCell__
from spira import settings


RDD = get_rule_deck()


class __Device__(__StructureCell__):

    def create_elementals(self, elems):
        super().create_elementals(elems)

        # # TODO: Do DRC and ERC checking here.
        # # sref_elems = self.cell.get_srefs()
        # for S in self.cell.get_srefs():
        #     if isinstance(S.ref, DLayer):
        #         elems += S

        # for S in self.cell.elementals:
        #     if isinstance(S.ref, TLayer):
        #         elems += S

        return elems

    
class Device(__Device__):
    pass


class Gate(__Device__):
    pass


class Circuit(__Device__):
    pass


class __Generator__(__CellContainer__):

    level = param.IntegerField(default=1)
    lcar = param.IntegerField(default=0.01)
    algorithm = param.IntegerField(default=6)

    generate_devices = param.DataField(fdef_name='create_devices')

    def create_graph(self, elems):

        prim_elems = ElementList()
        for S in elems.sref:
            if isinstance(S.ref, (NLayer, TLayer, DLayer)):
                prim_elems += S

        for layer in RDD.METALS.layers:
            L = Cell(name='{}'.format(layer))

            # ply_elems = D.get_mlayers(layer=layer)

            ply_elems = ElementList()
            for S in elems.sref:
                if isinstance(S.ref, CMLayers):
                    # print(S.ref.layer)
                    if S.ref.layer.number == layer:
                        # print(S)
                        for p in S.ref.elementals:
                            # print(p.ref.player)
                            # FIXME!!!
                            # if isinstance(p, ELayers):
                                # raise Errors
                            if isinstance(p.ref.player, Polygons):
                                ply_elems += p.ref.player

            if ply_elems:
                geom = Geometry(name='{}'.format(layer), lcar=self.lcar, algorithm=self.algorithm, layer=layer, polygons=ply_elems)

                mesh_data = geom.create_mesh

                params = {'name': '{}'.format(layer),
                            'layer': Layer(number=layer),
                            'point_data': [mesh_data[2]],
                            'cell_data': [mesh_data[3]],
                            'field_data': [mesh_data[4]]}

                mesh = Mesh(polygons=ply_elems,
                            primitives=prim_elems,
                            points=mesh_data[0],
                            cells=mesh_data[1],
                            **params)

                L += mesh
                elems += SRef(L)

                sg = {}
                subgraphs = elems.subgraphs
                for name, g in subgraphs.items():
                    graph = Graph(subgraphs={name:g})
                    sg[name] = graph.g
                ng = Graph(subgraphs=sg)
                ng.write_graph(graphname='{}'.format(layer))
                elems += ng

    def wrap_references(self, c, c2dmap):
        from spira.kernel.utils import scale_coord_down as scd
        for e in c.elementals:
            if isinstance(e, SRef):
                if e.ref in c2dmap:
                    e.ref = c2dmap[e.ref]

    def create_devices(self):
        deps = self.cell.dependencies()
        c2dmap = {}
        for T in self.library.pcells:
            for D in deps:

                plane_elems = ElementList()
                plane_elems += self.cell.elementals[(RDD.GDSII.GPLAYER, 0)]

                C = Device(cell=D, cell_elems=D.elementals, plane_elems=plane_elems)

                for S in T.elementals.sref:
                    S.ref.create_elementals(C.elementals)

                c2dmap.update({D: C})

        for c in self.cell.dependencies():
            self.wrap_references(c, c2dmap)

        return SRef(self.cell)


class GateGenerator(__Generator__):
    """
    Connect to the current library and get the
    primitive metadata from the Rule Deck.
    The pcell device is updated after parsing the
    elementals in the via pcell class.
    """

    structure_gate = param.DataField(fdef_name='create_structure_gate')

    def create_structure_gate(self):
        self.generate_devices

        self.cell.name += 'gate'

        mask = Gate(cell=self.cell, cell_elems=self.cell.elementals)
        return SRef(mask)


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

