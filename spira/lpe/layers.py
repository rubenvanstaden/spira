
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
from spira.lrc.rules import *
from spira.kernel.cell import CellField

from spira.kernel.cell import Cell
from spira.kernel.layer import Layer
from spira.kernel.elemental.polygons import Polygons
from spira.kernel.elemental.label import Label
from spira.kernel.elemental.port import Port
from spira.kernel.elemental.sref import SRef
from spira.lne.graph import Graph
from spira.lne.mesh import Mesh
from spira.kernel.parameters.field.element_list import ElementList


RDD = get_rule_deck()


class __DeviceLayer__(Cell):
    doc = param.StringField()
    name = param.StringField()


class __ProcessLayer__(Cell):
    doc = param.StringField()
    name = param.StringField()


class PLayer(__ProcessLayer__):

    layer = param.LayerField()
    player = param.PolygonField()

    def create_elementals(self, elems):
        # self.player.move(origin=self.player.center, destination=(0,0))
        elems += self.player
        return elems


class BoxLayers(__DeviceLayer__):

    blayer = param.PolygonField()
    device_elems = param.ElementListField()
    box = param.DataField(fdef_name='create_box_layer')
    terms = param.DataField(fdef_name='create_labels')

    # def create_ports(self, ports):
    def create_labels(self):
        elems = ElementList()
        for p in self.device_elems.polygons:
            layer = p.gdslayer.number
            if layer in RDD.METALS.layers:
                l2 = Layer(name='BoundingBox', number=layer, datatype=5)
                # FIXME: Ports with the same name overrides eachother.
                elems += Port(name='P{}'.format(layer), midpoint=self.blayer.center, gdslayer=l2)
        return elems

    def create_box_layer(self):
        elems = ElementList()
        for p in self.device_elems.polygons:
            layer = p.gdslayer.number
            if layer in RDD.METALS.layers:
                l1 = Layer(name='BoundingBox', number=layer, datatype=5)
                elems += Polygons(polygons=self.blayer.polygons, gdslayer=l1)
        return elems

    def create_elementals(self, elems):

        elems += self.box
        elems += self.terms

        elems = elems.flatten()

        return elems


class GLayer(PLayer):
    """ Ground Plane layer. """

    blayer = param.PolygonField()
    device_elems = param.ElementListField()
    box = param.DataField(fdef_name='create_box_layer')
    terms = param.DataField(fdef_name='create_labels')

    # def create_ports(self, ports):
    def create_labels(self):
        elems = ElementList()
        for p in self.device_elems.polygons:
            layer = p.gdslayer.number
            if layer in RDD.GROUND.layers:
                l2 = Layer(name='BoundingBox', number=layer, datatype=5)
                elems += Port(name='P{}'.format(layer), midpoint=self.blayer.center, gdslayer=l2)
        return elems

    def create_box_layer(self):
        elems = ElementList()
        for p in self.device_elems.polygons:
            layer = p.gdslayer.number
            if layer in RDD.GROUND.layers:
                l1 = Layer(name='BoundingBox', number=layer, datatype=5)
                elems += Polygons(polygons=self.blayer.polygons, gdslayer=l1)
        return elems

    def create_elementals(self, elems):

        super().create_elementals(elems)

        # elems += self.box
        # elems += self.terms
        #
        # elems = elems.flatten()

        return elems


class MLayer(PLayer):

    metal_elems = param.ElementListField()
    metal_layer = param.DataField(fdef_name='create_merged_metal_layers')

    def create_ports(self, ports):
        pass

    # def create_merged_metal_layers(self):
    #     points = []
    #     for p in self.metal_elems:
    #         for pp in p.polygons:
    #             points.append(pp)
    #     if points:
    #         self.player = UnionPolygons(polygons=points, gdslayer=self.layer)
    #     return self.player

    def create_elementals(self, elems):

        # elems += self.metal_layer

        super().create_elementals(elems)

        return elems


class ELayer(PLayer):

    def create_elementals(self, elems):

        super().create_elementals(elems)

        return elems


class DLayer(PLayer):

    layer1 = param.LayerField()
    layer2 = param.LayerField()

    port1 = param.DataField(fdef_name='create_port1')
    port2 = param.DataField(fdef_name='create_port2')

    color = param.ColorField(default='#C0C0C0')

    def create_port1(self):
        port = Port(name='P1', midpoint=self.vlayer.center, gdslayer=self.layer1)
        return port
    
    def create_port2(self):
        port = Port(name='P2', midpoint=self.vlayer.center, gdslayer=self.layer2)
        return port

    def create_elementals(self, elems):

        super().create_elementals(elems)

        # elems += self.port1
        # elems += self.port2

        return elems
