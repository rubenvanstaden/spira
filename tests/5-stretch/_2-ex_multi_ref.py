import spira.all as spira
from spira.yevon.geometry import shapes
from spira.yevon.geometry.coord import Coord
from spira.yevon.rdd import get_rule_deck


RDD = get_rule_deck()


class A(spira.Cell):
    """ Cell with boxes to stretch a SRef containing one polygon. """
    def create_elementals(self, elems):
        shape_hexagon = shapes.ConvexShape(radius=7*1e6)
        elems += spira.Polygon(alias='J5', shape=shape_hexagon, layer=spira.Layer(1))
        return elems


class B(spira.Cell):
    """ Cell with boxes to stretch a SRef containing two polygons. """
    def create_elementals(self, elems):
        shape_hexagon = shapes.ConvexShape(radius=7*1e6)
        elems += spira.Polygon(alias='J5', shape=shape_hexagon, layer=RDD.PLAYER.M1.METAL)
        shape_rect = shapes.RectangleShape(p1=(-2*1e6, -2*1e6), p2=(2*1e6, 2*1e6))
        elems += spira.Polygon(alias='J5', shape=shape_rect, layer=RDD.PLAYER.M2.METAL)
        return elems


class C(spira.Cell):
    """ Cell with boxes to stretch a SRef containing two polygons. """
    def create_elementals(self, elems):
        shape_rect = shapes.RectangleShape(p1=(-2*1e6, -2*1e6), p2=(2*1e6, 2*1e6))
        elems += spira.Polygon(alias='P1', shape=shape_rect, layer=spira.Layer(number=2))
        shape_circle = shapes.CircleShape(box_size=(5*1e6, 5*1e6))
        elems += spira.Polygon(alias='P2', shape=shape_circle, layer=spira.Layer(number=3))
        return elems


class D(spira.Cell):
    """ Cell with one elem in the toplevel, and another as a reference. """
    def create_elementals(self, elems):
        c0 = spira.Cell(name='C0')
        c0 += spira.Rectangle(alias='I5', p1=(-2*1e6, -2*1e6), p2=(2*1e6, 2*1e6), layer=RDD.PLAYER.M2.METAL)
        elems += spira.Convex(alias='J5', radius=7*1e6, layer=RDD.PLAYER.M1.METAL)
        elems += spira.SRef(c0)
        return elems


class E(spira.Cell):
    """ Cell with one elem in the toplevel, and another as a reference. """
    def create_elementals(self, elems):
        elems += spira.Convex(alias='J5', radius=7*1e6, layer=RDD.PLAYER.M0.GND)
        
        c1 = spira.Cell(name='C1')
        c1 += spira.Circle(alias='P2', box_size=(3*1e6, 3*1e6), layer=RDD.PLAYER.C2.VIA)

        c0 = spira.Cell(name='C0')
        c0 += spira.Rectangle(alias='I5', p1=(-2*1e6, -2*1e6), p2=(2*1e6, 2*1e6), layer=RDD.PLAYER.M2.METAL)
        c0 += spira.SRef(c1)

        elems += spira.SRef(c0)
        return elems


if __name__ == '__main__':

    cell = spira.Cell(name='TopLevel')

    # # ----- Stretching a reference. -----
    # D = A()
    # cell += spira.SRef(D).stretch(factor=(2,1))
    # # ------------------------------------

    # # ----- Stretching a reference. -----
    # D1 = B()
    # cell += spira.SRef(D1).stretch(factor=(1,2))
    # # ------------------------------------
    
    # # ----- Stretching a reference. -----
    # D1 = C()
    # cell += spira.SRef(D1).stretch(factor=(2,1))
    # # ------------------------------------
    
    # # ----- Stretching a reference. -----
    # D1 = D()
    # cell += spira.SRef(D1).stretch(factor=(2,1))
    # # ------------------------------------
    
    # ----- Stretching a reference. -----
    D1 = E()
    cell += spira.SRef(D1).stretch(factor=(2,1))
    # ------------------------------------

    cell.output()


