import spira.all as spira
from spira.yevon.geometry import shapes
from spira.yevon.geometry.coord import Coord
from spira.yevon.rdd import get_rule_deck
from spira.yevon import process as pc


RDD = get_rule_deck()


class A(spira.Cell):
    """ Cell with boxes to stretch a SRef containing one polygon. """

    def create_elementals(self, elems):

        shape_hexagon = shapes.ConvexShape(radius=7*1e6)
        elems += spira.Polygon(alias='J5', shape=shape_hexagon, gds_layer=spira.Layer(number=11))

        return elems


class B(spira.Cell):
    """ Cell with boxes to stretch a SRef containing two polygons. """

    def create_elementals(self, elems):

        shape_hexagon = shapes.ConvexShape(radius=7*1e6)
        elems += spira.Polygon(alias='Pb0', shape=shape_hexagon, gds_layer=spira.Layer(number=11))

        shape_rect = shapes.RectangleShape(p1=(-2*1e6, -2*1e6), p2=(2*1e6, 2*1e6))
        elems += spira.Polygon(alias='Pb1', shape=shape_rect, gds_layer=spira.Layer(number=12))

        return elems


class C(spira.Cell):
    """ Cell with boxes to stretch a SRef containing two polygons. """

    def create_elementals(self, elems):

        shape_hexagon = shapes.ConvexShape(radius=7*1e6)
        elems += spira.Polygon(alias='P0', shape=shape_hexagon, gds_layer=spira.Layer(number=11))

        shape_rect = shapes.RectangleShape(p1=(-2*1e6, -2*1e6), p2=(2*1e6, 2*1e6))
        elems += spira.Polygon(alias='P1', shape=shape_rect, gds_layer=spira.Layer(number=12))
        
        shape_circle = shapes.CircleShape(box_size=(5*1e6, 5*1e6))
        elems += spira.Polygon(alias='P2', shape=shape_circle, gds_layer=spira.Layer(number=13))

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
        S1 = T(S)
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
    # S1 = T(S)
    # cell += S1
    # ------------------------------------

    # # ----- Stretching a reference. -----
    # D1 = Device_B()
    # S = spira.SRef(D1)
    # # cell += S
    # T = spira.Stretch(stretch_factor=(2,1))
    # S1 = T(S)
    # print(S1)
    # print(S1.ref)
    # print(S1.ref.elementals)
    # cell += S1
    # # ------------------------------------

    # ----- Stretching a reference. -----
    D1 = Device_C()
    S = spira.SRef(D1)
    # print(S)
    # print(S.ref)
    # print(S.ref.elementals)
    cell += S
    # T = spira.Stretch(stretch_factor=(2,1))
    # S1 = T(S)
    # print(S1)
    # print(S1.ref)
    # print(S1.ref.elementals)
    # cell += S1
    # ------------------------------------

    cell.output()


