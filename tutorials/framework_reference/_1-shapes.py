import spira.all as spira
from spira.yevon.geometry.shapes.basic import *
from spira.yevon.geometry.shapes.advance import *


if __name__ == '__main__':

    circle_shape = CircleShape()
    hexagon_shape = ConvexShape()
    arrow_shape = ArrowShape()
    rect_shape = RectangleShape()
    box_shape = BoxShape()
    basic_tri_shape = BasicTriangle()
    tri_shape = TriangleShape()

    cell = spira.Cell(name='Basic Shapes')

    # circle = spira.Polygon(shape=circle_shape, layer=spira.Layer(number=13))
    # circle.center = (0,0)
    # cell += circle

    # hexagon = spira.Polygon(shape=hexagon_shape, layer=spira.Layer(number=14))
    # hexagon.center = (5,0)
    # cell += hexagon

    # rect = spira.Polygon(shape=rect_shape, layer=spira.Layer(number=16))
    # rect.center = (15,0)
    # cell += rect

    # box = spira.Polygon(shape=box_shape, layer=spira.Layer(number=17))
    # box.center = (20,0)
    # cell += box

    # FIXME
    # basic = spira.Polygon(shape=basic_tri_shape, layer=spira.Layer(number=18))
    # basic.center = (25,0)
    # cell += basic

    # FIXME
    # tri = spira.Polygon(shape=tri_shape, layer=spira.Layer(number=19))
    # tri.center = (30,0)
    # cell += tri

    # FIXME
    # arrow = spira.Polygon(shape=arrow_shape, layer=spira.Layer(number=15))
    # arrow.center = (10,0)
    # cell += arrow

    # NOTE: Advanced shapes
    ytron_shape = YtronShape()
    ytron = spira.Polygon(shape=ytron_shape, layer=spira.Layer(number=20))
    ytron.center = (35,0)
    cell += ytron

    cell.gdsii_output()

