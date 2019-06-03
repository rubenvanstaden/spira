import spira.all as spira

from tests._03_structures.jj import Junction
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


class Jtl(spira.Cell):

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

        return elems


# -------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':

    D = Jtl()
    D.output()
