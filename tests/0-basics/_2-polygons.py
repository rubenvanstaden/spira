import spira.all as spira
from spira.yevon.rdd import get_rule_deck


RDD = get_rule_deck()


points = [[0, 0], [2*1e6, 2*1e6],
          [2*1e6, 6*1e6], [-6*1e6, 6*1e6],
          [-6*1e6, -6*1e6], [-4*1e6, -4*1e6],
          [-4*1e6, 4*1e6], [0, 4*1e6]]
p1 = spira.Polygon(shape=points, layer=spira.Layer(number=1))
# p1 = spira.Polygon(shape=points, layer=RDD.PLAYER.M1.HOLE)

D = spira.Cell(name='PolygonTest')
D += p1
D.output()

