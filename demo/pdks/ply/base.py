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

    def create_layer(self):
        return None

    def create_polygon(self):
        return None

    def create_elementals(self, elems):
        elems += self.polygon
        return elems

    def create_ports(self, ports):
        if self.player.purpose in (RDD.PURPOSE.PRIM.VIA, RDD.PURPOSE.PRIM.JUNCTION):
            ports += spira.Port(
                name='P1', 
                midpoint=self.polygon.center,
                gdslayer = self.layer1
            )
            ports += spira.Port(
                name='P2', 
                midpoint=self.polygon.center,
                gdslayer = self.layer2
            )
        return ports

