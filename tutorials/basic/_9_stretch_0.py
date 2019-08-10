import spira.all as spira
from spira.yevon.geometry import shapes
from spira.yevon.geometry.coord import Coord
from spira.yevon import process as pc
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()

 
ply = spira.Rectangle(p1=(0, 0), p2=(10, 5), layer=RDD.PLAYER.M2.METAL)


T = spira.Stretch(stretch_factor=(1,2))
# points = T.apply_to_array(ply.points)
# print(points)
ply = ply.transform(T)
print(ply.transformation)


cell = spira.Cell(name='Stretcth')
cell += ply


cell.gdsii_view()




