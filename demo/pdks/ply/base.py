import spira
import numpy as np
from spira import param
from spira.rdd import get_rule_deck


RDD = get_rule_deck()


class __ProcessLayer__(spira.Cell):

    layer = param.DataField(fdef_name='create_layer')
    polygon = param.DataField(fdef_name='create_polygon')

    def create_layer(self):
        return None

    def create_polygon(self):
        return None

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
            name='P1',
            midpoint=self.polygon.center,
            gdslayer = self.layer1
        )
        p2 = spira.Port(
            name='P2',
            midpoint=self.polygon.center,
            gdslayer = self.layer2
        )
        return [p1, p2]

    def create_edge_ports(self, edges):
        xpts = list(self.points[0][:, 0])
        ypts = list(self.points[0][:, 1])

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

            orientation = (-1) * orientation

            edges += spira.Term(
                name=name,
                # name='{}_{}'.format(i, name),
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

    def create_elementals(self, elems):
        elems += self.polygon
        return elems

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

        if self.player.purpose in (RDD.PURPOSE.PRIM.VIA, RDD.PURPOSE.PRIM.JUNCTION):
            ports += self.contact_ports
        elif self.player.purpose == RDD.PURPOSE.METAL:
            if self.level == 1:
                ports += self.metal_port
            for edge in self.edge_ports:
                ports += edge

        return ports
