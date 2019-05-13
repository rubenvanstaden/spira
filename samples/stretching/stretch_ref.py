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
        elems += spira.Polygon(alias='J5', shape=shape_hexagon, gds_layer=spira.Layer(number=11))

        shape_rect = shapes.RectangleShape(p1=(-2*1e6, -2*1e6), p2=(2*1e6, 2*1e6))
        elems += spira.Polygon(alias='J5', shape=shape_rect, gds_layer=spira.Layer(number=12))

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


class D(spira.Cell):
    """ Cell with one elem in the toplevel, and another as a reference. """

    def create_elementals(self, elems):

        shape_hexagon = shapes.ConvexShape(radius=7*1e6)
        elems += spira.Polygon(alias='J5', shape=shape_hexagon, gds_layer=spira.Layer(number=11))

        shape_rect = shapes.RectangleShape(p1=(-2*1e6, -2*1e6), p2=(2*1e6, 2*1e6))
        p0 = spira.Polygon(alias='J5', shape=shape_rect, gds_layer=spira.Layer(number=12))
        c0 = spira.Cell(name='C0')
        c0 += p0
        elems += spira.SRef(c0)

        return elems


class E(spira.Cell):
    """ Cell with one elem in the toplevel, and another as a reference. """

    def create_elementals(self, elems):

        shape_hexagon = shapes.ConvexShape(radius=7*1e6)
        elems += spira.Polygon(alias='J5', shape=shape_hexagon, gds_layer=spira.Layer(number=11))

        shape_rect = shapes.RectangleShape(p1=(-2*1e6, -2*1e6), p2=(2*1e6, 2*1e6))
        p0 = spira.Polygon(alias='J5', shape=shape_rect, gds_layer=spira.Layer(number=12))
        c0 = spira.Cell(name='C0')
        c0 += p0

        shape_circle = shapes.CircleShape(box_size=(3*1e6, 3*1e6))
        p1 = spira.Polygon(alias='P2', shape=shape_circle, gds_layer=spira.Layer(number=13))
        c1 = spira.Cell(name='C1')
        c1 += p1
        
        c0 += spira.SRef(c1)

        elems += spira.SRef(c0)

        return elems


if __name__ == '__main__':

    cell = spira.Cell(name='TopLevel')

    # D1 = Squares(name='SquareCell_1')
    # S2 = spira.SRef(D1)
    # cell += S2

    # # ----- Stretching a reference. -----
    # D = A()
    # S = spira.SRef(D)
    # T = spira.Stretch(stretch_factor=(2,1))
    # S1 = T(S)
    # cell += S1
    # # ------------------------------------
    
    # # ----- Stretching a reference. -----
    # D1 = B()
    # S = spira.SRef(D1)
    # T = spira.Stretch(stretch_factor=(2,1))
    # S1 = T(S)
    # cell += S1
    # # ------------------------------------
    
    # # ----- Stretching a reference. -----
    # D1 = C()
    # S = spira.SRef(D1)
    # T = spira.Stretch(stretch_factor=(2,1))
    # S1 = T(S)
    # cell += S1
    # # ------------------------------------

    # # ----- Stretching a reference. -----
    # D1 = D()
    # S = spira.SRef(D1)
    # T = spira.Stretch(stretch_factor=(2,1))
    # S1 = T(S)
    # cell += S1
    # # ------------------------------------

    # ----- Stretching a reference. -----
    D1 = E()
    S = spira.SRef(D1)
    # cell += S
    T = spira.Stretch(stretch_factor=(2,1))
    S1 = T(S)
    cell += S1
    # ------------------------------------
    cell.output()


