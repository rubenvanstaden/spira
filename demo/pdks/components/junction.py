import spira
from spira import param
from spira import shapes
from spira.rdd import get_rule_deck
from spira.rdd.technology import ProcessTree
from spira.lpe.structure import ComposeMLayers
from spira.lpe.structure import ComposeNLayer


RDD = get_rule_deck()


class PShape(spira.Cell):

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


class PBox(PShape):

    w = param.FloatField(default=1)
    h = param.FloatField(default=1)
    center = param.PointField()

    def validate_parameters(self):
        if self.w < self.player.data.WIDTH:
            return False
        if self.h < self.player.data.WIDTH:
            return False
        return True

    def create_polygon(self):
        shape = shapes.BoxShape(center=self.center, width=self.w, height=self.h)
        ply = spira.Polygons(shape=shape, gdslayer=self.player.layer)
        return ply


class Junction(spira.Cell):
    """ Josephon Junction component for the AIST process. """

    metals = param.DataField(fdef_name='create_metal_layers')
    contacts = param.DataField(fdef_name='create_contact_layers')

    def create_metal_layers(self):
        metals = spira.ElementList()
        metals += PBox(player=RDD.PLAYER.COU, center=(1.95, 5.76), w=1.9, h=6.7)
        metals += PBox(player=RDD.PLAYER.BAS, center=(1.95, 2.6), w=3.9, h=5.2)
        metals += PBox(player=RDD.PLAYER.BAS, center=(1.95, 7.7), w=1.9, h=2.8)
        metals += PBox(player=RDD.PLAYER.RES, center=(1.95, 7.2), w=1.5, h=1.5)
        metals += PBox(player=RDD.PLAYER.RES, center=(1.95, 5.76), w=1.5, h=2.0)
        metals += PBox(player=RDD.PLAYER.RES, center=(1.95, 3.55), w=3.4, h=2.8)
        return metals

    def create_contact_layers(self):
        elems = spira.ElementList()
        elems += PBox(player=RDD.PLAYER.GC, center=(1.95, 1.1), w=2.9, h=1.2)
        elems += PBox(player=RDD.PLAYER.BC, center=(1.95, 8.5), w=1.4, h=1.0)
        elems += PBox(player=RDD.PLAYER.RC, center=(1.95, 7.2), w=0.9, h=1.0)
        elems += PBox(player=RDD.PLAYER.RC, center=(1.95, 3.55), w=2.9, h=2.3)
        elems += PBox(player=RDD.PLAYER.JC, center=(1.95, 3.55), w=1.4, h=1.0)
        elems += PBox(player=RDD.PLAYER.JJ, center=(1.95, 3.55), w=1.9, h=1.3)
        return elems

    def create_elementals(self, elems):
        if len(elems) == 0:
            for e in self.metals:
                elems += e
            for e in self.contacts:
                elems += e

        for key in RDD.VIAS.keys:
            RDD.VIAS[key].PCELL.create_elementals(elems)

        return elems

    def create_ports(self, ports):
        t1 = spira.Term(name='Input', midpoint=(3.6, 3.5), orientation=180)
        t2 = spira.Term(name='Output', midpoint=(0.25, 3.5))
        ports += t1
        ports += t2
        return ports


if __name__ == '__main__':

    name = 'Junction_PCell'
    spira.LOG.header('Running example: {}'.format(name))

    jj = Junction()
    jj.output(name=name)

    spira.LOG.end_print('Junction example finished')








