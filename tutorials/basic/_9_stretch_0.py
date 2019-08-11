import spira.all as spira
from spira.yevon.geometry import shapes
from spira.yevon.geometry.coord import Coord
from spira.yevon import process as pc
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()

 
# ply = spira.Rectangle(p1=(0, 0), p2=(20, 5), layer=RDD.PLAYER.M2.METAL)


# T = spira.Stretch(stretch_factor=(1,4))
# # ply = ply.transform(T)
# # print(ply.transformation)


# cell = spira.Cell(name='Stretcth')
# cell += ply


# # cell.gdsii_view()
# cell.gdsii_output(file_name='no_stretch')

 
T = spira.Stretch(stretch_factor=(1,4))
ply = spira.Rectangle(p1=(0, 0), p2=(20, 5), layer=RDD.PLAYER.M2.METAL, transformation=T)

cell = spira.Cell(name='Stretcth', elements=[ply])

cell.gdsii_view()
# cell.gdsii_output(file_name='no_stretch')







