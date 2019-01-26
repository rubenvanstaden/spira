import spira
from spira import param
from spira.rdd import get_rule_deck


RDD = get_rule_deck()


class Base(spira.Cell):

    layer1 = param.LayerField()
    layer2 = param.LayerField()
    player = param.PhysicalLayerField()

    level = param.IntegerField(default=0)
    error = param.IntegerField(default=0)

    layer = param.DataField(fdef_name='create_layer')
    polygon = param.DataField(fdef_name='create_polygon')
    metal_port = param.DataField(fdef_name='create_metal_port')
    contact_ports = param.DataField(fdef_name='create_contact_ports')
    display_contact_ports = param.DataField(fdef_name='create_display_contact_ports')

    def create_layer(self):
        return None

    def create_polygon(self):
        return None

    def create_elementals(self, elems):
        elems += self.polygon
        return elems

    def create_metal_port(self):
        return spira.Port(
            name='P_metal',
            # name=self.polygon.id,
            midpoint=self.polygon.center,
            gdslayer = self.layer1
        )

    def create_display_contact_ports(self):
        display = '\n'
        for p in self.contact_ports:
            display.join(p)
        return display

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

    def create_ports(self, ports):
        if self.player.purpose in (RDD.PURPOSE.PRIM.VIA, RDD.PURPOSE.PRIM.JUNCTION):
            ports += self.contact_ports
        elif self.player.purpose == RDD.PURPOSE.METAL:
            if self.level == 1:
                ports += self.metal_port
        return ports

