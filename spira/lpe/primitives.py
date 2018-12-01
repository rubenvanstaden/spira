
# import spira
import gdspy
import networkx as nx

from copy import copy, deepcopy
from spira import settings

from spira.rdd import get_rule_deck
from spira.kernel.elemental.polygons import UnionPolygons
from spira.kernel import parameters as param
from spira.templates import vias
from spira.kernel import utils

from spira.kernel.cell import Cell
from spira.kernel.layer import Layer
from spira.kernel.elemental.polygons import Polygons
from spira.kernel.elemental.label import Label
from spira.kernel.elemental.port import Port
from spira.kernel.elemental.sref import SRef
# from spira.kernel.elemental.graph import Graph
from spira.lne.graph import Graph
# from spira.kernel.elemental.mesh import Mesh
from spira.lne.mesh import Mesh
from spira.lne.geometry import Geometry
from spira.kernel.parameters.field.element_list import ElementList

from spira.lpe.containers import __CellContainer__
from spira.lpe.layers import *


RDD = get_rule_deck()


class Primitive(__CellContainer__):

    cell_elems = param.ElementListField()

    def create_elementals(self, elems):

        for layer in (*RDD.METALS.layers, *RDD.GROUND.layers):

            flat_elems = self.cell_elems.flat_copy()
            metal_elems = flat_elems.get_polygons(layer=layer)

            ll = Layer(name='METAL', number=layer)

            if metal_elems:
                # NOTE: Does not loop over all elems,
                # because we are merging them.
                for i, ply in enumerate(metal_elems):
                    name = 'MLayer_{}_{}'.format(layer, i)
                    # ml = MLayer(name=name, layer=ll, metal_elems=metal_elems)
                    ml = MLayer(name=name, layer=ll, player=ply)
                    elems += SRef(ml)

        for layer in RDD.VIAS.layers:

            flat_elems = self.cell_elems.flat_copy()
            via_elems = flat_elems.get_polygons(layer=layer)

            ll = Layer(name='VIA', number=layer)

            if via_elems:
                for i, device in enumerate(via_elems):
                    name = 'DLayer_{}_{}'.format(layer, i)
                    device_layer = DLayer(name=name, layer=ll, player=device)
                    elems += SRef(device_layer)

        return elems


class Rules(Cell):

    def create_elementals(self, elems):

        # elems += Surround(layer1=RDD.J5, layer2=RDD.M6, min=0.3) # TODO: Remove, just a test
        # elems += Width(layer1=RDD.M5, min=0.7, max=20) # TODO: Not implemented!

        return elems

RDD.PRIM_RULES = Rules()


class AddVirtualGround(Primitive):

    plane_elems = param.ElementListField() # Elementals like skyplanes and groundplanes.
    ground_layer = param.DataField(fdef_name='create_merged_ground_layers')

    def create_merged_ground_layers(self):
        points = []
        for p in self.plane_elems.flat_copy():
            for pp in p.polygons:
                points.append(pp)
        if points:
            ll = Layer(number=RDD.GROUND.M4.LAYER, datatype=6)
            merged_ply = UnionPolygons(polygons=points, gdslayer=ll)
            return merged_ply
        return None

    def create_elementals(self, elems):

        super().create_elementals(elems)

        box = self.cell.bbox
        # box.move(origin=box.center, destination=(0,0))

        gnd_full = self.ground_layer

        gnd = gnd_full | box

        name = 'GLayer_{}'.format(gnd.gdslayer.number)
        gnd_layer = GLayer(name=name, layer=gnd.gdslayer, player=gnd)
        elems += SRef(gnd_layer)

        # TODO: Add a GROUND bbox to Device for primitive
        # and DRC detection, since GROUND is only in Mask Cell.

        # B = BoxLayers(blayer=box, device_elems=self.cell.elementals)
        # Bs = SRef(B)
        # Bs.move(origin=(0,0), destination=self.cell.bbox.center)
        # elems += Bs

        return elems


class PrimitiveRuleCheck(AddVirtualGround):

    def create_elementals(self, elems):

        super().create_elementals(elems)

        broken_rules = ElementList()

        for rule in RDD.PRIM_RULES.elementals:
            if rule.apply(elems):
                for S in elems:
                    if S.ref.layer.number == rule.layer1.number:
                        broken_rules += S

        print('\n----- DRC Violations -----')
        for elemental in broken_rules:
            print(elemental)
            elems += elemental
        print('')

        return elems


class Device(PrimitiveRuleCheck):

    device_elems = param.ElementListField()

    def create_elementals(self, elems):

        super().create_elementals(elems)

        box = self.cell.bbox
        box.move(origin=box.center, destination=(0,0))

        # TODO: Add a GROUND bbox to Device for primitive
        # and DRC detection, since GROUND is only in Mask Cell.

        B = BoxLayers(blayer=box, device_elems=self.cell.elementals)
        Bs = SRef(B)
        Bs.move(origin=(0,0), destination=self.cell.bbox.center)
        elems += Bs

        return elems


class Circuit(__CellContainer__):

    graphs = param.DataField(fdef_name='create_graphs')
    container = param.DataField(fdef_name='create_container')

    def create_geometry(self):
        pass

    def create_mesh(self):
        pass

    def create_graphs(self):

        elems = self.cell.elementals

        for D in elems.dependencies():
            if isinstance(D, Device):

                prim_elems = ElementList()
                for S in D.elementals.sref:
                    if isinstance(S.ref, DLayer):
                        prim_elems += S

                for layer in RDD.METALS.layers:
                    L = Cell(name='{}'.format(layer))

                    geom = Geometry(name='{}'.format(layer), layer=layer)

                    ply_elems = ElementList()
                    for S in D.elementals.sref:
                        if isinstance(S.ref, MLayer):
                            if S.ref.layer.number == layer:
                                for p in S.ref.elementals:
                                    ply_elems += p

                    if ply_elems:
                        geom.create_geom_elements(ply_elems)

                        mesh_data = geom.create_mesh

                        l1 = Layer(name='', number=layer)
                        params = {'name': D.name,
                                  'layer': l1,
                                  'point_data': [mesh_data[2]],
                                  'cell_data': [mesh_data[3]],
                                  'field_data': [mesh_data[4]]}

                        mesh = Mesh(polygons=ply_elems,
                                          primitives=prim_elems,
                                          points=mesh_data[0],
                                          cells=mesh_data[1],
                                          **params)

                        L += mesh
                        D += SRef(L)

        for D in elems.dependencies():
            if isinstance(D, Device):
                sg = {}
                subgraphs = D.elementals.subgraphs
                for name, g in subgraphs.items():
                    graph = Graph(subgraphs={name:g})
                    sg[name] = graph.g
                ng = Graph(subgraphs=sg)
                ng.write_graph(graphname=D.name)
                D += ng
                # D.plot_subgraphs()

    def create_container(self):
        dmap = {}
        for T in self.library.pcells:
            for D in self.cell.dependencies():

                plane_elems = ElementList()
                plane_elems += self.cell.elementals[(RDD.GROUND.M4.LAYER, 0)]

                C = Device(cell=D, cell_elems=D.elementals, plane_elems=plane_elems)

                for S in T.elementals.sref:
                    S.ref.create_elementals(C.elementals)

                C.name = '{}_pcell'.format(D.name)
                dmap.update({D.name: C})

                # print('\n----- Dependencies -----')
                # print(C)
                # for d in C.elementals.dependencies():
                #     print(d)

        # FIXME: Does not work recursively.
        for e in self.cell.elementals.sref:
            if e.ref.name in dmap.keys():
                e.ref = dmap[e.ref.name]
                e.ref.name = e.ref.name + '_n'

    def create_elementals(self, elems):
        """
        Connect to the current library and get the
        primitive metadata from the Rule Deck.
        The pcell device is updated after parsing the
        elementals in the via pcell class.
        """

        super().create_elementals(elems)

        self.container
        # self.cell_graphs

        return elems
