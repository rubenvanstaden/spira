import spira.all as spira
from spira.yevon.geometry import shapes
from spira.yevon.rdd import get_rule_deck


RDD = get_rule_deck()


cell = spira.Cell(name='C1')

c1 = spira.Cell(name='C2')

shape = shapes.RectangleShape(p1=(0,0), p2=(2*1e6,2*1e6))
c1 += spira.Polygon(shape=shape, layer=RDD.PLAYER.M1.METAL)

cell += spira.SRef(c1)

cell.output()

