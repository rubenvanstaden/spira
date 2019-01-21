# import spira
import gdspy
import networkx as nx

from copy import copy, deepcopy
from spira import settings

from spira.rdd import get_rule_deck
from spira import param
from spira.gdsii import utils

from spira.gdsii.cell import Cell
from spira.gdsii.layer import Layer
from spira.gdsii.elemental.polygons import Polygons
from spira.gdsii.elemental.label import Label
from spira.gdsii.elemental.port import Port
from spira.gdsii.elemental.port import Port
from spira.gdsii.elemental.sref import SRef
from spira.lne.graph import Graph
from spira.lne.mesh import Mesh
from spira.core.lists import ElementList


RDD = get_rule_deck()


class CMLayers(Cell):

    layer = param.LayerField()

    def create_elementals(self, elems):
        return elems

    def set_net(self):
        pass

    def get_net(self):
        pass


class CNLayers(Cell):

    layer = param.LayerField()

    def create_elementals(self, elems):
        return elems


class CGLayers(Cell):

    layer = param.LayerField()

    def create_elementals(self, elems):
        return elems


class __DeviceLayer__(Cell):
    doc = param.StringField()
    name = param.StringField()


class __ProcessLayer__(Cell):
    doc = param.StringField()
    points = param.ElementListField()
    # points = param.PointArrayField()
    number = param.IntegerField()
    error_type = param.IntegerField()
    level = param.IntegerField()

    layer = param.DataField(fdef_name='create_layer')
    polygon = param.DataField(fdef_name='create_polygon_layer')
    player = param.PhysicalLayerField()

    def create_polygon_layer(self):
        return Polygons(shape=self.points, gdslayer=self.layer)

    def create_layer(self):
        if self.error_type != 0:
            return Layer(name=self.name, number=self.number, datatype=self.error_type)
        else:
            return Layer(name=self.name, number=self.number, datatype=self.level)

    def create_elementals(self, elems):
        elems += self.polygon
        return elems


class __ConnectLayer__(__ProcessLayer__):

    midpoint = param.MidPointField()

    layer1 = param.LayerField()
    layer2 = param.LayerField()

    port1 = param.DataField(fdef_name='create_port1')
    port2 = param.DataField(fdef_name='create_port2')
    player = param.PhysicalLayerField()

    def create_port1(self):
        port = Port(name='P1', midpoint=self.midpoint, gdslayer=self.layer1)
        return port

    def create_port2(self):
        port = Port(name='P2', midpoint=self.midpoint, gdslayer=self.layer2)
        return port

    def create_ports(self, ports):
        ports += self.port1
        ports += self.port2
        return ports

    def create_elementals(self, elems):
        super().create_elementals(elems)
        return elems


# class DLayer(__DeviceLayer__):

#     blayer = param.PolygonField()
#     device_elems = param.ElementListField()
#     box = param.DataField(fdef_name='create_box_layer')
#     terms = param.DataField(fdef_name='create_labels')

#     color = param.ColorField(default='#e54e7f')

#     def create_labels(self):
#         elems = ElementList()
#         for p in self.device_elems.polygons:
#             layer = p.gdslayer.number
#             players = RDD.PLAYER.get_physical_layers(purposes='METAL')
#             if layer in players:
#                 l2 = Layer(name='BoundingBox', number=layer, datatype=8)
#                 # FIXME: Ports with the same name overrides eachother.
#                 elems += Port(name='P{}'.format(layer), midpoint=self.blayer.center, gdslayer=l2)
#         return elems

#     def create_box_layer(self):
#         elems = ElementList()
#         setter = {}

#         for p in self.device_elems.polygons:
#             layer = p.gdslayer.number
#             setter[layer] = 'not_set'

#         for p in self.device_elems.polygons:
#             layer = p.gdslayer.number
#             players = RDD.PLAYER.get_physical_layers(purposes=['METAL'])
#             if layer in players and setter[layer] == 'not_set':
#                 l1 = Layer(name='BoundingBox', number=layer, datatype=8)
#                 elems += Polygons(shape=self.blayer.polygons, gdslayer=l1)
#                 setter[layer] = 'already_set'
#         return elems

#     def create_elementals(self, elems):

#         elems += self.box
#         elems += self.terms

#         elems = elems.flatten()

#         return elems


class DLayer(__DeviceLayer__):

    points = param.PointArrayField()
    device_elems = param.ElementListField()
    box = param.DataField(fdef_name='create_box_layer')
    terms = param.DataField(fdef_name='create_labels')

    color = param.ColorField(default='#e54e7f')

    def create_labels(self):
        elems = ElementList()
        for p in self.device_elems.polygons:
            layer = p.gdslayer.number
            players = RDD.PLAYER.get_physical_layers(purposes='METAL')
            if layer in players:
                l2 = Layer(name='BoundingBox', number=layer, datatype=8)
                # FIXME: Ports with the same name overrides eachother.
                # elems += Port(name='P{}'.format(layer), midpoint=self.blayer.center, gdslayer=l2)
        return elems

    def create_box_layer(self):
        elems = ElementList()
        setter = {}

        for p in self.device_elems.polygons:
            layer = p.gdslayer.number
            setter[layer] = 'not_set'

        for p in self.device_elems.polygons:
            for pl in RDD.PLAYER.get_physical_layers(purposes=['METAL', 'GND']):
                if pl.layer == p.gdslayer:
                    if setter[pl.layer.number] == 'not_set':
                        l1 = Layer(name='BoundingBox', number=pl.layer.number, datatype=0)
                        # l1 = Layer(name='BoundingBox', number=pl.layer.number, datatype=8)
                        elems += Polygons(shape=self.points, gdslayer=l1)
                        setter[pl.layer.number] = 'already_set'
        return elems

    def create_elementals(self, elems):
        for e in self.box:
            elems += e
        # elems += self.terms
        # elems = elems.flatten()
        return elems
    
    def create_ports(self, ports):



        return ports


class GLayer(__ProcessLayer__):
    """ Ground Plane layer. """

    blayer = param.PolygonField()
    device_elems = param.ElementListField()
    box = param.DataField(fdef_name='create_box_layer')
    terms = param.DataField(fdef_name='create_labels')

    def create_labels(self):
        elems = ElementList()
        for p in self.device_elems.polygons:
            layer = p.gdslayer.number
            # if layer in RDD.GROUND.layers:
            if layer == RDD.GDSII.GPLAYER:
                l2 = Layer(name='BoundingBox', number=layer, datatype=5)
                elems += Port(name='P{}'.format(layer), midpoint=self.blayer.center, gdslayer=l2)
        return elems

    def create_box_layer(self):
        elems = ElementList()
        for p in self.device_elems.polygons:
            layer = p.gdslayer.number
            # if layer in RDD.GROUND.layers:
            if layer == RDD.GDSII.GPLAYER:
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


class MLayer(__ProcessLayer__):

    def create_elementals(self, elems):

        super().create_elementals(elems)

        return elems


class ELayer(__ProcessLayer__):

    def create_elementals(self, elems):

        super().create_elementals(elems)

        return elems


class NLayer(__ConnectLayer__):

    color = param.ColorField(default='#C0C0C0')

    def create_elementals(self, elems):

        super().create_elementals(elems)

        return elems


class TLayer(__ConnectLayer__):

    color = param.ColorField(default='#B4F8C8')

    def create_elementals(self, elems):

        super().create_elementals(elems)

        return elems
