import spira
from spira.lgm.shapes.basic import *
from spira.lgm.shapes.advance import *


if __name__ == '__main__':

    circle_shape = CircleShape()
    hexagon_shape = ConvexPolygon()
    arrow_shape = ArrowShape()
    arrow_shape.apply_merge
    rect_shape = RectangleShape()
    box_shape = BoxShape()
    basic_tri_shape = BasicTriangle()
    tri_shape = TriangleShape()
    tri_shape.apply_merge

    cell = spira.Cell(name='Basic Shapes')

    # ----------------------------- Basic Shapes ----------------------------------

    circle = spira.Polygons(shape=circle_shape, gds_layer=spira.Layer(number=13))
    circle.center = (0,0)
    cell += circle

    hexagon = spira.Polygons(shape=hexagon_shape, gds_layer=spira.Layer(number=14))
    hexagon.center = (5*1e6,0)
    cell += hexagon

    arrow = spira.Polygons(shape=arrow_shape, gds_layer=spira.Layer(number=15))
    arrow.center = (10*1e6,0)
    cell += arrow

    rect = spira.Polygons(shape=rect_shape, gds_layer=spira.Layer(number=16))
    rect.center = (15*1e6,0)
    cell += rect

    box = spira.Polygons(shape=box_shape, gds_layer=spira.Layer(number=17))
    box.center = (20*1e6,0)
    cell += box

    basic = spira.Polygons(shape=basic_tri_shape, gds_layer=spira.Layer(number=18))
    basic.center = (25*1e6,0)
    cell += basic

    tri = spira.Polygons(shape=tri_shape, gds_layer=spira.Layer(number=19))
    tri.center = (30*1e6,0)
    cell += tri

    # ----------------------------- Advanced Shapes ----------------------------------
    
    ytron_shape = YtronShape()
    ytron = spira.Polygons(shape=ytron_shape, gds_layer=spira.Layer(number=20))
    ytron.center = (35*1e6,0)
    cell += ytron

    cell.output()

