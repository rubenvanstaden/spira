import spira.all as spira
from spira.yevon.rdd import get_rule_deck


RDD = get_rule_deck()


p1 = spira.Port(midpoint=(0,0), width=4*1e6, length=1*1e6)

D = spira.Cell(name='PortTests')
D.ports += p1
D.output()

