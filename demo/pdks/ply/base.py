import spira
from spira import param
from spira.rdd import get_rule_deck


RDD = get_rule_deck()


class Base(spira.Cell):

    player = param.PhysicalLayerField()
    polygon = param.DataField(fdef_name='create_polygon')

    def create_polygon(self):
        return None

    def create_elementals(self, elems):
        elems += self.polygon
        return elems

    def create_ports(self, ports):
        if self.player.purpose in (RDD.PURPOSE.PRIM.VIA, RDD.PURPOSE.PRIM.JUNCTION):
            ports += spira.Port(name='P1', midpoint=self.center)
            ports += spira.Port(name='P2', midpoint=self.center)
        return ports

