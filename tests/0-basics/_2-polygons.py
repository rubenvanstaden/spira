import spira.all as spira
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


points = [[0, 0], [2, 2], [2, 6], [-6, 6], [-6, -6], [-4, -4], [-4, 4], [0, 4]]
# p1 = spira.Polygon(shape=points, layer=spira.Layer(number=1))
p1 = spira.Polygon(shape=points, layer=RDD.PLAYER.M1.METAL)

D = spira.Cell(name='PolygonTest')
D += p1
D.gdsii_output()

