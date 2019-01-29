import spira
from spira import param
from spira.rdd import get_rule_deck


RDD = get_rule_deck()


class __ProcessLayer__(spira.Cell):
    pass


class ProcessLayer(__ProcessLayer__):

    layer1 = param.LayerField()
    layer2 = param.LayerField()
    player = param.PhysicalLayerField()

    level = param.IntegerField(default=0)
    error = param.IntegerField(default=0)

    layer = param.DataField(fdef_name='create_layer')
    polygon = param.DataField(fdef_name='create_polygon')
    metal_port = param.DataField(fdef_name='create_metal_port')
    contact_ports = param.DataField(fdef_name='create_contact_ports')

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

    def create_ports(self, ports):
        if self.player.purpose in (RDD.PURPOSE.PRIM.VIA, RDD.PURPOSE.PRIM.JUNCTION):
            ports += self.contact_ports
        elif self.player.purpose == RDD.PURPOSE.METAL:
            if self.level == 1:
                ports += self.metal_port
        return ports

    def commit_to_gdspy(self, cell):
        self.polygon.commit_to_gdspy(cell=cell)
        for p in self.ports:
            p.commit_to_gdspy(cell=cell)

    def flat_copy(self, level=-1, commit_to_gdspy=False):
        elems = spira.ElementList()
        elems += self.polygon.flat_copy()
        elems += self.ports.flat_copy()
        return elems