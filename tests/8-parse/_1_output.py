import spira.all as spira
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


# p1 = spira.Rectangle(p1=(0,0), p2=(10,10), layer=RDD.PLAYER.M1.METAL)

# D = spira.Cell(name='C1')
# D += p1

# D.gdsii_output(name='output')



# p1 = spira.Rectangle(p1=(0,0), p2=(10,10), layer=RDD.PLAYER.M1.METAL)
# c1 = spira.Cell(name='C1')
# c1 += p1

# D = spira.Cell(name='C1')
# D += spira.SRef(c1)

# D.gdsii_output(name='output')



p1 = spira.Rectangle(p1=(0,0), p2=(10,10), layer=RDD.PLAYER.M1.METAL)
c1 = spira.Cell(name='C1')
c1 += p1

c2 = spira.Cell(name='C2')
c2 += spira.SRef(c1)

D = spira.Cell(name='Device')
D += spira.SRef(c2)

D.gdsii_output(name='output')



