import spira.all as spira

from tests._03_structures.jj import Junction
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


class VirtualBias(spira.Cell):

    def create_elementals(self, elems):

        elems += spira.Rectangle(p1=(60*1e6, 45*1e6), p2=(80*1e6, 80*1e6), layer=RDD.PLAYER.M2.METAL)

        c1 = spira.Cell(name='ply1')
        c1 += spira.Rectangle(p1=(60*1e6, 80*1e6), p2=(80*1e6, 100*1e6), layer=RDD.PLAYER.M2.METAL)
        c1 += spira.Rectangle(p1=(70*1e6, 60*1e6), p2=(100*1e6, 70*1e6), layer=RDD.PLAYER.M2.METAL)
        elems += spira.SRef(c1)
        
        return elems


class JtlBiasPorts(spira.Cell):

    routes = spira.DataField(fdef_name='create_routes')

    def get_transforms(self):
        t1 = spira.Translation(translation=(0*1e6, 0*1e6))
        t2 = spira.Translation(translation=(150*1e6, 0*1e6))
        return [t1, t2]

    def create_routes(self):
        routes = spira.ElementalList()
        routes += spira.Rectangle(p1=(4*1e6, -4*1e6), p2=(146*1e6, 4*1e6), layer=RDD.PLAYER.M2.METAL)
        routes += spira.Rectangle(p1=(-3*1e6, -4*1e6), p2=(-30*1e6, 4*1e6), layer=RDD.PLAYER.M2.METAL)
        routes += spira.Rectangle(p1=(153*1e6, -4*1e6), p2=(180*1e6, 4*1e6), layer=RDD.PLAYER.M2.METAL)
        routes += spira.Rectangle(p1=(60*1e6, 0*1e6), p2=(80*1e6, 50*1e6), layer=RDD.PLAYER.M2.METAL)
        return routes

    def create_elementals(self, elems):
        t1, t2 = self.get_transforms()

        jj = Junction()

        s_top = spira.SRef(alias='S1', reference=jj, transformation=t1)
        s_bot = spira.SRef(alias='S2', reference=jj, transformation=t2)

        for r in self.routes:
            elems += r

        elems += s_top
        elems += s_bot

        elems += spira.SRef(reference=VirtualBias())

        return elems

    def create_ports(self, ports):
        ports += spira.Port(process=RDD.PROCESS.M2, midpoint=(-28*1e6, 0), orientation=180, width=8*1e6)
        ports += spira.Port(process=RDD.PROCESS.M2, midpoint=(180*1e6, 0), orientation=0, width=8*1e6)
        ports += spira.Port(process=RDD.PROCESS.M2, midpoint=(100*1e6, 65*1e6), orientation=0, width=20*1e6)
        ports += spira.Port(process=RDD.PROCESS.M2, midpoint=(70*1e6, 100*1e6), orientation=90, width=20*1e6)
        return ports


# -------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':

    D = JtlBias()
    D.output()



