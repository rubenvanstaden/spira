import spira.all as spira
from spira.yevon.geometry import shapes
from spira.yevon.geometry.coord import Coord
from expand_transform import Junction
from spira.yevon.rdd import get_rule_deck


RDD = get_rule_deck()


class Jtl(spira.Cell):

    def get_transforms(self):
        t1 = spira.Translation(Coord(0, 0))
        t2 = spira.Translation(Coord(150, 0))
        return [t1, t2]

    def get_routes(self):
        shape_rectangle = shapes.RectangleShape(p1=(-13, -60), p2=(13, 12))
        ply = spira.Polygon(alias='M4', shape=shape_rectangle, gds_layer=spira.Layer(number=5))
        return ply

    def create_elementals(self, elems):
        t1, t2 = self.get_transforms()

        jj = Junction()

        s_top = spira.SRef(alias='S1', reference=jj, transformation=t1)
        s_bot = spira.SRef(alias='S2', reference=jj, transformation=t2)

        elems += s_top
        elems += s_bot

        return elems


# --------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':

    jtl= Jtl()

    jtl.expand_transform()

    # for k, v in jtl['Junction_S1'].alias_cells.items():
    #     print(k, v)

    ply = jtl['Junction_S1']['Jj_S0']['J5']
    print(ply)

    # ply.stretch(factor=(1,2))
    T = spira.Stretch(stretch_factor=(2,1))
    ply.transform(T)

    print(ply)
    jtl.output()


