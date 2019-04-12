import spira
import gdspy
import numpy as np
import networkx as nx
from copy import deepcopy
from spira.core import param
from spira.netex.mesh import Mesh
from spira.netex.geometry import Geometry
from spira.yevon.rdd import get_rule_deck
from spira.yevon.gdsii.cell import Cell

from spira.yevon.rdd.layer import PhysicalLayerField
from spira.yevon.layer import LayerField
from spira.core.param.variables import *
from spira.core.descriptor import DataField
from spira.core.elem_list import ElementalListField


__all__ = ['ProcessLayer']


RDD = get_rule_deck()


class __ProcessLayer__(Cell):

    doc = StringField()
    layer = DataField(fdef_name='create_layer')
    points = DataField(fdef_name='create_points')
    polygon = DataField(fdef_name='create_polygon')

    def create_layer(self):
        return None

    def create_polygon(self):
        ply = self.elementals[0]
        # if self.transformation is not None:
        #     # print(type(self.transformation))
        #     if hasattr(self.transformation, '__subtransforms__'):
        #         for T in self.transformation.__subtransforms__:
        #             ply = ply.transform_copy(T)
        #     else:
        #         # print(self.transformation)
        #         ply = ply.transform_copy(self.transformation)
        return ply

    def create_points(self):
        return self.polygon.shape.points

    def commit_to_gdspy(self, cell=None):
        P = self.polygon.commit_to_gdspy(cell=cell)
        for p in self.ports:
            p.commit_to_gdspy(cell=cell)
        return P

    # def transform(self, transformation=None):
    #     if transformation is None:
    #         t = self.transformation
    #     else:
    #         t = transformation

    #     if t is not None:
    #         if hasattr(t, '__subtransform__'):
    #             for T in t.__subtransforms__:
    #                 if T.reflection is True:
    #                     self.reflect()
    #                 if T.rotation is not None:
    #                     self.rotate(angle=T.rotation)
    #                 if len(T.midpoint) != 0:
    #                     self.translate(dx=T.midpoint[0], dy=T.midpoint[1])
    #         else:
    #             T = t
    #             if T.reflection is True:
    #                 self.reflect()
    #             if T.rotation is not None:
    #                 self.rotate(angle=T.rotation)
    #             if len(T.midpoint) != 0:
    #                 self.translate(dx=T.midpoint[0], dy=T.midpoint[1])

    #     self.transformation = transformation

    #     # print('\n\n\nwfenwekjfnwejknfjwkefnwkefj')
    #     # print(self.elementals)
    #     self.points = self.elementals[0].points
        
    #     # from spira.yevon.geometry.shapes.basic import BoxShape
    #     # elems = spira.ElementList()
    #     # ply = spira.Polygon(shape=self.points, gds_layer=self.layer)
    #     # elems += ply.transform_copy(self.transformation)
    #     # # ply.center = self.center
    #     # self.elementals = elems

    #     return self
        
    # def flat_copy(self, level=-1):
    #     elems = spira.ElementList()
    #     ports = spira.ElementList()
    #     elems += self.polygon.flat_copy()
    #     ports += self.ports.flat_copy()
    #     C = self.modified_copy(elementals=elems, ports=ports)
    #     return C

    # def flat_copy(self, level=-1, commit_to_gdspy=False):
    #     elems = spira.ElementList()
    #     elems += self.polygon.flat_copy()
    #     elems += self.ports.flat_copy()
    #     return elems


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
            midpoint=self.polygon.center,
            gds_layer=l1
        )
        l2 = spira.Layer(
            name=self.name,
            number=self.layer2.number,
            datatype=RDD.PURPOSE.PRIM.VIA.datatype
        )
        p2 = spira.Port(
            name='P_contact_2',
            midpoint=self.polygon.center,
            gds_layer=l2
        )
        return [p1, p2]

    def create_edge_ports(self, edges):

        PTS = []
        for pts in self.points:
            PTS.append(np.array(pts))
        xpts = list(PTS[0][:, 0])
        ypts = list(PTS[0][:, 1])

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
            orientation = (np.arctan2(x, y) * 180/np.pi) - 90
            midpoint = [(xpts[i+1] + xpts[i])/2, (ypts[i+1] + ypts[i])/2]
            width = np.abs(np.sqrt((xpts[i+1] - xpts[i])**2 + (ypts[i+1]-ypts[i])**2))
            edges += spira.EdgeTerm(
                name=name,
                gds_layer=self.layer,
                midpoint=midpoint,
                orientation=orientation,
                width=width,
                edgelayer=spira.Layer(number=65),
                arrowlayer=spira.Layer(number=78),
                local_connect=self.polygon.node_id,
                is_edge=True,
                # pid=self.node_id
            )

        return edges


class ProcessLayer(__PortConstructor__):

    layer1 = LayerField()
    layer2 = LayerField()
    ps_layer = PhysicalLayerField()
    level = IntegerField(default=0)
    error = IntegerField(default=0)
    enable_edges = BoolField(default=True)

    # --- Net ---
    lcar = FloatField(default=0.0)
    dimension = IntegerField(default=2)
    algorithm = IntegerField(default=6)
    primitives = ElementalListField()
    route_nodes = ElementalListField()
    bounding_boxes = ElementalListField()
    graph = DataField(fdef_name='create_netlist_graph')
    # -----------

    def __repr__(self):
        return ("[SPiRA: ProcessLayer(\'{}\')] {} center, {} ports)").format(
            self.ps_layer.layer.number,
            self.center,
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

    def create_netlist_graph(self):

        geom = Geometry(
            name=self.name,
            layer=self.ps_layer.layer,
            lcar=self.lcar,
            # polygons=[self.polygon],
            polygons=[self],
            algorithm=self.algorithm,
            dimension=self.dimension
        )

        mesh = Mesh(
            name='{}'.format(self.layer),
            level=self.level,
            layer=self.ps_layer.layer,
            # polygons=[self.polygon],
            polygons=[self],
            primitives=self.primitives,
            route_nodes=self.route_nodes,
            bounding_boxes=self.bounding_boxes,
            data=geom.create_mesh
        )

        # print(list(nx.connected_components(mesh.g)))
        # self.plotly_netlist(G=mesh.g, graphname=self.name, labeltext='id')

        return mesh.g
