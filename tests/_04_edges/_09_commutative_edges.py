import spira.all as spira
from spira.yevon.vmodel.connections import ElectricalConnections

from spira.technologies.mit.process import RDD


el = spira.ElementalList()

# Main Polygon
# el += spira.Rectangle(p1=(0, 0), p2=(4, 10), layer=RDD.PLAYER.M5.METAL)

# Main Cell
c1 = spira.Cell(name='Ply1')
c1 += spira.Rectangle(p1=(0, 0), p2=(4, 10), layer=RDD.PLAYER.M5.METAL)
el += spira.SRef(reference=c1)

# # T0
# el += spira.Rectangle(p1=(3, 4), p2=(8, 6), layer=RDD.PLAYER.M5.METAL)

# # T6
# el += spira.Rectangle(p1=(8, 4), p2=(-4, 6), layer=RDD.PLAYER.M5.METAL)

# # T2
# el += spira.Rectangle(p1=(-4, 4), p2=(1, 6), layer=RDD.PLAYER.M5.METAL)
# el += spira.Rectangle(p1=(3, 4), p2=(8, 6), layer=RDD.PLAYER.M5.METAL)

# # T1 FIXME!
# el += spira.Rectangle(p1=(-4, 8), p2=(8, 12), layer=RDD.PLAYER.M5.METAL)

# # T3 FIXME!
# el += spira.Rectangle(p1=(0, 10), p2=(4, 14), layer=RDD.PLAYER.M5.METAL)

# # T4 FIXME!
# el += spira.Rectangle(p1=(1, 9), p2=(3, 14), layer=RDD.PLAYER.M5.METAL)

# # T5 FIXME!
# el += spira.Rectangle(p1=(-1, 9), p2=(5, 14), layer=RDD.PLAYER.M5.METAL)

from spira.yevon.filters.boolean_filter import MetalConnectFilter

device = spira.Cell(name='Device', elementals=el)
# device.gdsii_output()

F = MetalConnectFilter()
D = F(device)
D.gdsii_output()

# D = spira.Circuit(name='TestElectricalConnections', elementals=D.elementals)
# D.netlist_output()





