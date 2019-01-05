import gdspy
import networkx as nx

from copy import copy, deepcopy
from spira import settings

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
        from spira.gdsii.utils import scale_coord_down as scd
        for e in c.elementals:
            if isinstance(e, SRef):
                if e.ref in c2dmap:
                    e.ref = c2dmap[e.ref]

    def create_devices(self):
        deps = self.cell.dependencies()
        c2dmap = {}
        # for DeviceTCell in self.library.pcells:
        # print(RDD.DEVICES.JJ.PCELL)
        # for DeviceTCell in RDD.DEVICES.JJ.PCELL:
        #     print(type(DeviceTCell))
        #     for C in deps:

        #         plane_elems = ElementList()
        #         plane_elems += self.cell.get_purpose_layers(purpose_symbol='GROUND')
        #         # plane_elems += self.cell.elementals[(RDD.GDSII.GPLAYER, 0)]

        #         D = Device(cell=C, cell_elems=C.elementals, plane_elems=plane_elems)

        #         for PrimTCell in DeviceTCell.elementals.sref:
        #             PrimTCell.ref.create_elementals(D.elementals)
        #         c2dmap.update({C: D})

        for key in RDD.DEVICES.keys:
            DeviceTCell = RDD.DEVICES[key].PCELL
            for C in deps:

                plane_elems = ElementList()
                # from spira.gdsii import utils
                # players = RDD.PLAYER.get_physical_layers(purposes='GROUND')
                # plane_elems += utils.get_purpose_layers(self.cell, players)
                # # plane_elems += self.cell.elementals[(RDD.GDSII.GPLAYER, 0)]

                D = Device(cell=C, cell_elems=C.elementals, plane_elems=plane_elems)

                for PrimTCell in DeviceTCell.elementals.sref:
                    PrimTCell.ref.create_elementals(D.elementals)
                c2dmap.update({C: D})

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









