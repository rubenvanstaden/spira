import spira
import gdspy
import networkx as nx

from copy import copy, deepcopy
from spira import settings

from spira.kernel.elemental.polygons import UnionPolygons
from spira.kernel import parameters as param
from spira.kernel import utils
from spira.kernel.cell import CellField
from spira.lpe.containers import __CellContainer__
from spira.lpe.layers import *
from spira.lpe.layer_cells import MetalCell
from spira.lpe.layer_cells import Rules
from spira.lpe.layer_cells import MetalRuleCheck
from spira.lgm.booleans import merge


RDD = spira.get_rule_deck()


# class MetalRuleCheck(MetalCell):

#     metal_elems = param.ElementListField()

#     def create_elementals(self, elems):

#         super().create_elementals(elems)

#         incorrect_elems = ElementList()
#         correct_elems = ElementList()

#         for rule in RDD.RULES.elementals:
#             if not rule.apply(elems):
#                 for S in elems:
#                     if S.ref.layer.number == rule.layer1.number:
#                         correct_elems += S
#             else:
#                 for M in elems:
#                     if M.ref.layer.number == rule.layer1.number:
#                         ply = deepcopy(M.ref.elementals[0])
#                         E = ELayer(points=ply.polygons,
#                                    number=M.ref.layer.number,
#                                    error_type=rule.error)
#                         M.ref += SRef(E)
#                         # incorrect_elems += M

#         # print('\n----- DRC Violations -----')
#         # for elemental in incorrect_elems:
#         #     print(elemental)
#         #     elems += elemental
#         # print('')

#         # for elemental in correct_elems:
#         #     elems += elemental

#         return elems


class PlacePrimitives(__CellContainer__):

    device_elems = param.ElementListField()

    def create_elementals(self, elems):

        super().create_elementals(elems)

        # TODO: Do DRC and ERC checking here.
        sref_elems = self.device_elems[0].ref.get_srefs()
        for S in sref_elems:
            if isinstance(S.ref, DLayer):
                elems += S

        # for S in self.device_elems:
        #     for S_prim in S.ref.elementals:
        #         if isinstance(S_prim.ref, DLayer):
        #             elems += S_prim

        return elems


class MaskCell(__CellContainer__):

    def create_mask_graph(self, elems):
        for layer in RDD.METALS.layers:
            L = spira.Cell(name='{}'.format(layer))

            prim_elems = spira.ElementList()
            for S in elems.sref:
                if isinstance(S.ref, DLayer):
                    prim_elems += S

            geom = spira.Geometry(name='{}'.format(layer),
                                  lcar=10,
                                  algorithm=1,
                                  layer=layer)

            assert isinstance(elems[0].ref, MetalRuleCheck)

            ply_elems = spira.ElementList()
            for S in elems[0].ref.elementals:
                if S.ref.clayer == layer:
                    ply_elems = S.ref.elementals

            if ply_elems:
                geom.create_geom_elements(ply_elems)

                mesh_data = geom.create_mesh

                l1 = spira.Layer(name='', number=layer)
                params = {'name': '{}'.format(layer),
                          'layer': l1,
                          'point_data': [mesh_data[2]],
                          'cell_data': [mesh_data[3]],
                          'field_data': [mesh_data[4]]}

                mesh = spira.Mesh(polygons=ply_elems,
                                  primitives=prim_elems,
                                  points=mesh_data[0],
                                  cells=mesh_data[1],
                                  **params)

                L += mesh
                elems += spira.SRef(L)

        sg = {}
        subgraphs = elems.subgraphs
        for name, g in subgraphs.items():
            graph = spira.Graph(subgraphs={name:g})
            sg[name] = graph.g
        ng = spira.Graph(subgraphs=sg)
        ng.write_graph(graphname='Mask')
        elems += ng
        # D.plot_subgraphs()

    def create_elementals(self, elems):

        super().create_elementals(elems)

        # metals = MetalCell(cell_elems=self.cell.elementals)
        # elems += spira.SRef(metals)

        M = MetalRuleCheck(cell_elems=self.cell.elementals)
        elems += spira.SRef(M)

        mask_cell = PlacePrimitives(cell=M, device_elems=self.cell.elementals)
        elems += spira.SRef(mask_cell)

        # metals = MetalCell(cell_elems=self.cell.elementals)
        # elems += spira.SRef(metals)

        # M = MetalRuleCheck(metal_elems=metals.elementals)
        # elems += spira.SRef(M)

        # mask_cell = PlacePrimitives(cell=M, device_elems=self.cell.elementals)
        # elems += spira.SRef(mask_cell)

        # self.create_mask_graph(mask_cell.elementals)

        return elems
