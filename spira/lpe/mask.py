import spira
import gdspy
import networkx as nx

from copy import copy, deepcopy
from spira import settings

from spira.kernel.elemental.polygons import UnionPolygons
from spira.kernel import parameters as param
from spira.templates import vias
from spira.kernel import utils
from spira.lrc.rules import *
from spira.kernel.cell import CellField
from spira.lpe.containers import __CellContainer__
from spira.lpe.layers import *


RDD = spira.get_rule_deck()


class MLayer(spira.Cell):

    layer = param.LayerField()
    metal_elems = param.ElementListField()
    merged_layer = param.DataField(fdef_name='create_merged_layer')

    def create_ports(self, ports):
        pass

    def create_merged_layer(self):
        points = []
        for p in self.metal_elems:
            for pp in p.polygons:
                points.append(pp)
        if points:
            # l1 = spira.Layer(name='MergedLayer', number=self.clayer)
            merge_ply = UnionPolygons(polygons=points, gdslayer=self.layer)
            return merge_ply
        return None

    def create_elementals(self, elems):

        elems += self.merged_layer

        return elems


class MetalCell(spira.Cell):

    cell_elems = param.ElementListField()

    def create_elementals(self, elems):

        for layer in (*RDD.METALS.layers, *RDD.GROUND.layers, RDD.MOAT.number):

            flat_elems = self.cell_elems.flat_copy()
            metal_elems = flat_elems.get_polygons(layer=layer)

            if metal_elems:
                name = 'MLayer_{}'.format(layer)
                ll = spira.Layer(name='MergedLayer', number=layer)
                ml = MLayer(name=name, layer=ll, metal_elems=metal_elems)
                elems += spira.SRef(ml)

        return elems


class Rules(spira.Cell):

    def create_elementals(self, elems):

        # elems += Density(layer1=RDD.M4, layer2=RDD.MOAT, min=35)
        elems += Surround(layer1=RDD.M6, layer2=RDD.M4, min=0.3) # TODO: Remove, just a test
        # elems += Width(layer1=RDD.M5, min=0.7, max=20) # TODO: Not implemented!
        # elems += Width(layer1=RDD.R5, min=0.7, max=20) # TODO: Not implemented!

        return elems

RDD.RULES = Rules()


class MetalRuleCheck(spira.Cell):

    metal_elems = param.ElementListField()

    def create_elementals(self, elems):

        for rule in RDD.RULES.elementals:
            if rule.apply(self.metal_elems):
                for S in self.metal_elems:
                    if S.ref.layer.number == rule.layer1.number:
                        elems += S
            else:
                for M in self.metal_elems:
                    if M.ref.layer.number == rule.layer1.number:
                        name = 'ELayer_{}'.format(RDD.ERRORS.SPACING)
                        ll = Layer(name='ERROR', 
                                   number=M.ref.metal_elems[0].gdslayer.number, 
                                   datatype=RDD.ERRORS.SPACING)
                        epolygon = deepcopy(M.ref.metal_elems[0])
                        epolygon.gdslayer = ll
                        E = ELayer(name=name, layer=ll, player=epolygon)
                        M.ref += SRef(E)

                        elems += M

        return elems


class PlacePrimitives(__CellContainer__):

    device_elems = param.ElementListField()

    def create_elementals(self, elems):

        super().create_elementals(elems)

        # TODO: Do DRC and ERC checking here.
        sref_elems = self.device_elems[0].ref.get_srefs()
        for S in sref_elems:
            if isinstance(S.ref, BoxLayers):
                elems += S

        # for S in self.device_elems:
        #     for S_prim in S.ref.elementals:
        #         if isinstance(S_prim.ref, BoxLayers):
        #             elems += S_prim

        return elems


class MaskCell(__CellContainer__):

    def create_mask_graph(self, elems):
        for layer in RDD.METALS.layers:
            L = spira.Cell(name='{}'.format(layer))

            prim_elems = spira.ElementList()
            for S in elems.sref:
                if isinstance(S.ref, BoxLayers):
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

        metals = MetalCell(cell_elems=self.cell.elementals)
        elems += spira.SRef(metals)

        M = MetalRuleCheck(metal_elems=metals.elementals)
        elems += spira.SRef(M)

        mask_cell = PlacePrimitives(cell=M, device_elems=self.cell.elementals)
        elems += spira.SRef(mask_cell)

        # self.create_mask_graph(mask_cell.elementals)

        return elems
