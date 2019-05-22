import spira.all as spira
import gdspy
import numpy as np
import networkx as nx
from copy import deepcopy
from spira.yevon.rdd import get_rule_deck
from spira.yevon.gdsii.cell import Cell

from spira.yevon.rdd.layer import PhysicalLayerField
from spira.yevon.layer import LayerField
from spira.core.parameters.variables import *
from spira.core.parameters.descriptor import DataField
from spira.yevon.gdsii.elem_list import ElementalListField
from spira.yevon import constants
from spira.yevon.geometry.shapes.shape import ShapeField


__all__ = ['ProcessLayer']


RDD = get_rule_deck()


class __ProcessLayer__(Cell):

    doc = StringField()
    layer = DataField(fdef_name='create_layer')
    shape = ShapeField()

    def create_layer(self):
        return None

    def commit_to_gdspy(self, cell=None):
        for e in self.elementals:
            e.commit_to_gdspy(cell=cell)
        for p in self.ports:
            p.commit_to_gdspy(cell=cell)
        return cell


class __PortConstructor__(__ProcessLayer__):

    edge_ports = ElementalListField()
    metal_port = DataField(fdef_name='create_metal_port')
    contact_ports = DataField(fdef_name='create_contact_ports')

    def create_metal_port(self):
        layer = spira.Layer(
            name=self.name,
            number=self.ps_layer.layer.number,
            datatype=RDD.PURPOSE.METAL.datatype
        )
        return spira.Port(
            name='P_metal',
            midpoint=self.polygon.center,
            gds_layer=layer
        )

    def create_contact_ports(self):
        l1 = spira.Layer(
            name=self.name,
            number=self.layer1.number,
            datatype=RDD.PURPOSE.PRIM.VIA.datatype
        )
        p1 = spira.Port(
            name='P_contact_1',
            # midpoint=self.polygon.center,
            midpoint=self.elementals[0].center,
            gds_layer=l1
        )
        l2 = spira.Layer(
            name=self.name,
            number=self.layer2.number,
            datatype=RDD.PURPOSE.PRIM.VIA.datatype
        )
        p2 = spira.Port(
            name='P_contact_2',
            # midpoint=self.polygon.center,
            midpoint=self.elementals[0].center,
            gds_layer=l2
        )
        return [p1, p2]

    def create_edge_ports(self, edges):

        # PTS = []
        # for pts in self.points:
        #     PTS.append(np.array(pts))
        # xpts = list(PTS[0][:, 0])
        # ypts = list(PTS[0][:, 1])

        # PTS = np.array(self.points)
        # xpts = list(PTS[:, 0])
        # ypts = list(PTS[:, 1])

        xpts = list(self.shape.x_coords)
        ypts = list(self.shape.y_coords)

        n = len(xpts)
        xpts.append(xpts[0])
        ypts.append(ypts[0]) 

        clockwise = 0
        for i in range(0, n):
            clockwise += ((xpts[i+1] - xpts[i]) * (ypts[i+1] + ypts[i]))

        for i in range(0, n):
            name = '{}_e{}'.format(self.ps_layer.layer.name, i)
            x = np.sign(clockwise) * (xpts[i+1] - xpts[i])
            y = np.sign(clockwise) * (ypts[i] - ypts[i+1])
            orientation = (np.arctan2(x, y) * constants.RAD2DEG)
            midpoint = [(xpts[i+1] + xpts[i])/2, (ypts[i+1] + ypts[i])/2]
            width = np.abs(np.sqrt((xpts[i+1] - xpts[i])**2 + (ypts[i+1]-ypts[i])**2))
            edges += spira.EdgeTerminal(
                name=name,
                gds_layer=self.layer,
                midpoint=midpoint,
                orientation=orientation,
                width=width,
                length=0.5*1e6,
                edgelayer=spira.Layer(number=70),
                arrowlayer=spira.Layer(number=78),
            )

        return edges


class ProcessLayer(__PortConstructor__):

    layer1 = LayerField()
    layer2 = LayerField()
    ps_layer = PhysicalLayerField()
    level = IntegerField(default=0)
    error = IntegerField(default=0)
    enable_edges = BoolField(default=True)
    
    # def __repr__(self):
    #     return ("[SPiRA: ProcessLayer(\'{}\')] {} ports)").format(
    #         self.ps_layer.layer.number,
    #         self.ports.__len__()
    #     )

    def __repr__(self):
        return ("[SPiRA: ProcessLayer(\'{}\')] {} center, {} ports)").format(
            self.ps_layer.layer.number,
            # self.center,
            self.elementals[0].shape.center_of_mass,
            self.ports.__len__()
        )

    def __str__(self):
        return self.__repr__()

    def create_layer(self):
        if self.error != 0:
            layer = spira.Layer(
                name=self.name,
                number=self.ps_layer.layer.number,
                datatype=self.error
            )
        elif self.level != 0:
            layer = spira.Layer(
                name=self.name,
                number=self.ps_layer.layer.number,
                datatype=self.level
            )
        else:
            layer = spira.Layer(
                name=self.name,
                number=self.ps_layer.layer.number,
                datatype=self.ps_layer.layer.datatype
            )
        return layer

    def create_ports(self, ports):
        if self.ps_layer.purpose == RDD.PURPOSE.PRIM.JUNCTION:
            ports += self.contact_ports
        elif self.ps_layer.purpose == RDD.PURPOSE.PRIM.VIA:
            ports += self.contact_ports
        elif self.ps_layer.purpose == RDD.PURPOSE.METAL:
            if self.level == 1:
                ports += self.metal_port
            if self.enable_edges:
                for edge in self.edge_ports:
                    ports += edge
        elif self.ps_layer.purpose == RDD.PURPOSE.PROTECTION:
            if self.enable_edges:
                for edge in self.edge_ports:
                    ports += edge
        return ports
        
    # def expand_transform(self):
    #     self.transform(self.transformation)
    #     # self.transformation = None
    #     return self

