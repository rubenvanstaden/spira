import spira
import numpy as np
from spira import param
from spira.rdd import get_rule_deck


RDD = get_rule_deck()


class __ProcessLayer__(spira.Cell):

    doc = param.StringField()
    layer = param.DataField(fdef_name='create_layer')
    points = param.DataField(fdef_name='create_points')
    polygon = param.DataField(fdef_name='create_polygon')

    def create_layer(self):
        return None

    def create_polygon(self):
        return self.elementals[0]

    def create_points(self):
        return self.polygon.shape.points

    def commit_to_gdspy(self, cell):
        self.polygon.commit_to_gdspy(cell=cell)
        for p in self.ports:
            p.commit_to_gdspy(cell=cell)

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
        return spira.Port(
            name='P_metal',
            midpoint=self.polygon.center,
            gdslayer = self.player.layer
        )

    def create_contact_ports(self):
        p1 = spira.Port(
            name='P_contact_1',
            midpoint=self.polygon.center,
            gdslayer = self.layer1
        )
        p2 = spira.Port(
            name='P_contact_2',
            midpoint=self.polygon.center,
            gdslayer = self.layer2
        )
        return [p1, p2]

    def create_edge_ports(self, edges):
        # print(self.points)

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

        for i in range(0, n):
            name = 'e{}'.format(i)
            x = np.sign(clockwise) * (xpts[i+1] - xpts[i])
            y = np.sign(clockwise) * (ypts[i] - ypts[i+1])
            orientation = (np.arctan2(x, y) * 180/np.pi) - 90
            midpoint = [(xpts[i+1] + xpts[i])/2, (ypts[i+1] + ypts[i])/2]
            width = np.abs(np.sqrt((xpts[i+1] - xpts[i])**2 + (ypts[i+1]-ypts[i])**2))
            edges += spira.EdgeTerm(
                name=name,
                gdslayer=self.layer,
                midpoint=midpoint,
                orientation=orientation,
                width=width,
                edgelayer=spira.Layer(number=65),
                arrowlayer=spira.Layer(number=78),
                local_connect=self.polygon.node_id,
                is_edge=True
            )

        return edges


class ProcessLayer(__PortConstructor__):

    layer1 = param.LayerField()
    layer2 = param.LayerField()
    player = param.PhysicalLayerField()
    level = param.IntegerField(default=10)
    error = param.IntegerField(default=0)
    enable_edges = param.BoolField(default=True)
    
    def __repr__(self):
        return ("[SPiRA: ProcessLayer(\'{}\')] {} center, {} ports)").format(
            self.player.layer.number,
            self.center,
            self.ports.__len__()
        )

    def __str__(self):
        return self.__repr__()

    def create_layer(self):
        if self.error != 0:
            layer = spira.Layer(
                name=self.name,
                number=self.player.layer.number,
                datatype=self.error
            )
        elif self.level != 0:
            layer = spira.Layer(
                name=self.name,
                number=self.player.layer.number,
                datatype=self.level
            )
        else:
            layer = spira.Layer(
                name=self.name,
                number=self.player.layer.number,
                datatype=self.player.layer.datatype
            )
        return layer

    def create_ports(self, ports):
        if self.player.purpose == RDD.PURPOSE.PRIM.JUNCTION:
            ports += self.contact_ports
        elif self.player.purpose == RDD.PURPOSE.PRIM.VIA:
            ports += self.contact_ports
        elif self.player.purpose == RDD.PURPOSE.METAL:
            if self.level == 1:
                ports += self.metal_port
            if self.enable_edges:
                for edge in self.edge_ports:
                    ports += edge
        return ports
