import spira.all as spira
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


p1 = spira.Rectangle(p1=(0,0), p2=(10,10), layer=RDD.PLAYER.M1.METAL)

D = spira.Cell(name='C1')
D += p1

D.gdsii_output(name='1-output')


