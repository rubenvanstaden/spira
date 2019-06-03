import spira.all as spira

from spira.yevon.geometry import shapes
from spira.yevon.geometry.coord import Coord
from spira.yevon.rdd import get_rule_deck


RDD = get_rule_deck()


class A(spira.Cell):
    """ Cell with boxes to stretch a SRef containing one polygon. """
    def create_elementals(self, elems):
        elems += spira.Convex(alias='J5', radius=7*1e6, layer=RDD.PLAYER.M1.METAL)
        return elems


class B(spira.Cell):
    """ Cell with boxes to stretch a SRef containing two polygons. """
    def create_elementals(self, elems):
        elems += spira.Convex(alias='Pb0', radius=7*1e6, layer=RDD.PLAYER.M1.METAL)
        elems += spira.Rectangle(alias='Pb1', p1=(-2*1e6, -2*1e6), p2=(2*1e6, 2*1e6), layer=RDD.PLAYER.M2.METAL)
        return elems


class C(spira.Cell):
    """ Cell with boxes to stretch a SRef containing two polygons. """
    def create_elementals(self, elems):
        # elems += spira.Convex(alias='P0', radius=7*1e6, layer=RDD.PLAYER.M1.METAL)
        # elems += spira.Rectangle(alias='P1', p1=(-2*1e6, -2*1e6), p2=(2*1e6, 2*1e6), layer=RDD.PLAYER.M2.METAL)
        elems += spira.Circle(alias='P2', box_size=(5*1e6, 5*1e6), layer=RDD.PLAYER.C1.VIA)
        return elems


class Device_A(spira.Cell):

    def create_elementals(self, elems):

        a1 = A()
        a2 = A()

        elems += spira.SRef(a1, midpoint=(0, 0))
        elems += spira.SRef(a2, midpoint=(30*1e6, 0))

        return elems


class Device_B(spira.Cell):

    def create_elementals(self, elems):

        a1 = B()
        a2 = B()

        elems += spira.SRef(a1, midpoint=(0, 0))
        elems += spira.SRef(a2, midpoint=(30*1e6, 0))

        return elems


class Device_C(spira.Cell):

    def create_elementals(self, elems):

        a1 = B()
        a2 = C()

        elems += spira.SRef(a1).stretch(factor=(4,1))
        elems += spira.SRef(a2)
        # elems += spira.SRef(a2, midpoint=(30*1e6, 0))

        return elems


if __name__ == '__main__':

    cell = spira.Cell(name='TopLevel')

    # # ----- Stretching a reference. -----
    # D1 = Device_A()
    # cell += spira.SRef(D1).stretch(factor=(2,1))
    # # ------------------------------------

    # # ----- Stretching a reference. -----
    # D1 = Device_B()
    # cell += spira.SRef(D1).stretch(factor=(3,1))
    # # ------------------------------------

    # ----- Stretching a reference. -----
    D1 = Device_C()
    # cell += spira.SRef(D1).stretch(factor=(1,1))
    cell += spira.SRef(D1)
    # ------------------------------------

    cell.output()


