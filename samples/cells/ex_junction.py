import spira.all as spira
from spira.yevon.geometry import shapes
from spira.yevon.geometry.coord import Coord
from spira.yevon.rdd import get_rule_deck
from spira.yevon import process as pc


RDD = get_rule_deck()


class Jj(spira.Cell):

    def create_elementals(self, elems):

        shape_hexagon = shapes.ConvexShape(radius=7*1e6)
        ply = spira.Polygon(alias='J5', shape=shape_hexagon, gds_layer=spira.Layer(number=11))
        ply.center = (0,0)
        elems += ply

        return elems


class ResVia(spira.Cell):

    def create_elementals(self, elems):

        shape_rectangle = shapes.RectangleShape(p1=(-7.5*1e6, -13.2*1e6), p2=(7.5*1e6, -8.2*1e6))
        ply = spira.Polygon(shape=shape_rectangle, gds_layer=spira.Layer(number=11))
        ply.center = (0,0)
        elems += ply

        shape_rectangle = shapes.RectangleShape(p1=(-4*1e6, -12*1e6), p2=(4.1*1e6, -10*1e6))
        ply = spira.Polygon(shape=shape_rectangle, gds_layer=spira.Layer(number=10))
        ply.center = (0,0)
        elems += ply

        return elems


class Top(spira.Cell):

    def get_transforms(self):
        t1 = spira.Translation((0*1e6, 0*1e6))
        t2 = spira.Translation((0*1e6, -8*1e6))
        return [t1, t2]

    def create_elementals(self, elems):
        t1, t2 = self.get_transforms()

        s_jj = spira.SRef(Jj(), transformation=t1)
        s_res = spira.SRef(ResVia(), transformation=t2)

        elems += pc.Rectangle(p1=(-10*1e6, -15*1e6), p2=(10*1e6, 10*1e6), ps_layer=RDD.PLAYER.COU)

        elems += s_jj
        elems += s_res

        return elems


class Bot(spira.Cell):

    def get_transforms(self):
        t1 = spira.Translation((0*1e6, 0*1e6))
        t2 = spira.Translation((0*1e6, -30*1e6))
        return [t1, t2]

    def create_elementals(self, elems):
        t1, t2 = self.get_transforms()

        s_res = spira.SRef(ResVia(), transformation=t2)

        elems += pc.Rectangle(p1=(-10*1e6, -55*1e6), p2=(10*1e6, -25*1e6), ps_layer=RDD.PLAYER.COU)

        elems += s_res

        return elems


class Junction(spira.Cell):
    """ Hypres Josephson junction. """

    def get_transforms(self):
        t1 = spira.Translation((0*1e6, 0*1e6))
        # t2 = spira.Translation((0*1e6, -5*1e6))
        t2 = spira.Translation((0*1e6, 0*1e6))
        return [t1, t2]

    def create_elementals(self, elems):
        t1, t2 = self.get_transforms()

        s_top = spira.SRef(alias='S1', reference=Top(), transformation=t1)
        s_bot = spira.SRef(alias='S2', reference=Bot(), transformation=t2)

        elems += pc.Rectangle(p1=(-13*1e6, -60*1e6), p2=(13*1e6, 12*1e6), ps_layer=RDD.PLAYER.BAS)

        elems += s_top
        elems += s_bot

        return elems


if __name__ == '__main__':

    junction = Junction()
    # junction = junction.expand_transform()
    junction.output()

    # D = Top()
    # D.output()


