import spira.all as spira

from spira.yevon.geometry import shapes
from spira.yevon.geometry.coord import Coord
from spira.yevon.rdd import get_rule_deck


RDD = get_rule_deck()


class A(spira.Cell):
    """ Cell with boxes to stretch a SRef containing one polygon. """

    def create_elementals(self, elems):
        elems += spira.Convex(alias='J5', radius=7*1e6, ps_layer=RDD.PLAYER.RC)
        return elems


class B(spira.Cell):
    """ Cell with boxes to stretch a SRef containing two polygons. """

    def create_elementals(self, elems):
        elems += spira.Convex(alias='Pb0', radius=7*1e6, ps_layer=RDD.PLAYER.RC)
        elems += spira.Rectangle(alias='Pb1', p1=(-2*1e6, -2*1e6), p2=(2*1e6, 2*1e6), ps_layer=RDD.PLAYER.COU)
        return elems


class C(spira.Cell):
    """ Cell with boxes to stretch a SRef containing two polygons. """

    def create_elementals(self, elems):
        # shape_hexagon = shapes.ConvexShape(radius=7*1e6)
        # elems += spira.Polygon(alias='P0', shape=shape_hexagon, gds_layer=spira.Layer(number=11))
        # shape_rect = shapes.RectangleShape(p1=(-2*1e6, -2*1e6), p2=(2*1e6, 2*1e6))
        # elems += spira.Polygon(alias='P1', shape=shape_rect, gds_layer=spira.Layer(number=12))
        # shape_circle = shapes.CircleShape(box_size=(5*1e6, 5*1e6))
        # elems += spira.Polygon(alias='P2', shape=shape_circle, gds_layer=spira.Layer(number=13))
        elems += spira.Convex(alias='P0', radius=7*1e6, ps_layer=RDD.PLAYER.BAS)
        elems += spira.Rectangle(alias='P1', p1=(-2*1e6, -2*1e6), p2=(2*1e6, 2*1e6), ps_layer=RDD.PLAYER.COU)
        elems += spira.Circle(alias='P2', box_size=(5*1e6, 5*1e6), ps_layer=RDD.PLAYER.RC)
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

        S = spira.SRef(a1, midpoint=(0, 0))
        T = spira.Stretch(stretch_factor=(2,1))
        # S1 = T(S)
        S1 = S.stretch(T)
        elems += S1

        elems += spira.SRef(a2, midpoint=(30*1e6, 0))

        return elems


if __name__ == '__main__':

    cell = spira.Cell(name='TopLevel')

    # # ----- Stretching a reference. -----
    # D1 = Device_A()
    # S = spira.SRef(D1)
    # # cell += S
    # T = spira.Stretch(stretch_factor=(2,1))
    # S1 = S.stretch(T)
    # cell += S1
    # # ------------------------------------

    # # ----- Stretching a reference. -----
    # D1 = Device_B()
    # S = spira.SRef(D1)
    # # cell += S
    # T = spira.Stretch(stretch_factor=(2,1))
    # S1 = S.stretch(T)
    # cell += S1
    # # ------------------------------------

    # ----- Stretching a reference. -----
    D1 = Device_C()
    S = spira.SRef(D1)
    # cell += S
    T = spira.Stretch(stretch_factor=(1,2))
    S1 = S.stretch(T)
    cell += S1
    # ------------------------------------

    cell.output()


