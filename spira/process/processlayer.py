import spira
import gdspy
import numpy as np
import networkx as nx
from copy import deepcopy
from spira import param
from spira.rdd import get_rule_deck
from spira.lne.mesh import Mesh
from spira.lne.geometry import Geometry


RDD = get_rule_deck()


class __ProcessLayer__(spira.Cell):

    doc = param.StringField()
    layer = param.DataField(fdef_name='create_layer')
    points = param.DataField(fdef_name='create_points')
    polygon = param.DataField(fdef_name='create_polygon')
    tf_polygon = param.DataField(fdef_name='create_tf_polygon')

    def create_layer(self):
        return None

    def create_polygon(self):
        ply = self.elementals[0]
        return ply

    @property
    def tf_polygon(self):
    # def create_tf_polygon(self):
        ply = deepcopy(self.elementals[0])
        if self.pc_transformation is not None:
            # print('!!!!!!!!!!!!!!!!!!!!')
            ply.transform(transform=self.pc_transformation.apply())
        return ply

    def create_points(self):
        return self.polygon.shape.points

    def commit_to_gdspy(self, cell=None):
        P = self.polygon.commit_to_gdspy(cell=cell)
        for p in self.ports:
            p.commit_to_gdspy(cell=cell)
        return P

    def flat_copy(self, level=-1, commit_to_gdspy=False):
        elems = spira.ElementList()
        elems += self.polygon.flat_copy()
        elems += self.ports.flat_copy()
        return elems


class __PortConstructor__(__ProcessLayer__):

    edge_ports = param.ElementalListField()
    metal_port = param.DataField(fdef_name='create_metal_port')
    contact_ports = param.DataField(fdef_name='create_contact_ports')

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

        # xpts = list(self.points[0][:, 0])
        # ypts = list(self.points[0][:, 1])

        n = len(xpts)
        xpts.append(xpts[0])
        ypts.append(ypts[0]) 

        clockwise = 0
        for i in range(0, n):
            clockwise += ((xpts[i+1] - xpts[i]) * (ypts[i+1] + ypts[i]))

        # print(self._ID)

        for i in range(0, n):
            # name = '{}_e{}_{}'.format(self.ps_layer.layer.name, i, self._ID)
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
                is_edge=True
            )
            
            # el = spira.Layer(
            #     number=self.layer.number,
            #     datatype=RDD.PURPOSE.EDGE.datatype
            #     # datatype=RDD.PURPOSE.EDGE
            # )
            
            # al = spira.Layer(
            #     number=self.layer.number,
            #     # datatype=RDD.PURPOSE.ARROW
            #     datatype=RDD.PURPOSE.ARROW.datatype
            # )

            # edges += spira.EdgeTerm(
            #     name=name,
            #     gds_layer=self.layer,
            #     midpoint=midpoint,
            #     orientation=orientation,
            #     width=width,
            #     edgelayer=el,
            #     arrowlayer=al,
            #     local_connect=self.polygon.node_id,
            #     is_edge=True
            # )

        return edges


class ProcessLayer(__PortConstructor__):

    layer1 = param.LayerField()
    layer2 = param.LayerField()
    ps_layer = param.PhysicalLayerField()
    level = param.IntegerField(default=0)
    error = param.IntegerField(default=0)
    enable_edges = param.BoolField(default=True)

    # --- Net ---
    lcar = param.FloatField(default=0.0)
    dimension = param.IntegerField(default=2)
    algorithm = param.IntegerField(default=6)
    primitives = param.ElementalListField()
    route_nodes = param.ElementalListField()
    bounding_boxes = param.ElementalListField()
    graph = param.DataField(fdef_name='create_netlist_graph')
    # -----------

    pc_transformation = param.TransformationField(allow_none=True, default=None)

    # def __deepcopy__(self, memo):
    #     return ProcessLayer(
    #         elementals=deepcopy(self.elementals),
    #         # polygon=deepcopy(self.polygon),
    #         layer=self.layer,
    #         ps_layer=self.ps_layer,
    #         node_id=deepcopy(self.node_id),
    #     )

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
        # self.plot_netlist(G=mesh.g, graphname=self.name, labeltext='id')

        return mesh.g
