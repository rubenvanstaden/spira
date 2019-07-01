import spira.all as spira
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


p1 = spira.Port(midpoint=(0,0), width=4, length=1)

D = spira.Cell(name='PortTests')
D.ports += p1
D.gdsii_output()

