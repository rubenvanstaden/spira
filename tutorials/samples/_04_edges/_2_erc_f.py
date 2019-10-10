import numpy as np
import spira.all as spira

from spira.yevon.vmodel.virtual import virtual_connect
from spira.technologies.mit.process import RDD


el = spira.ElementList()

p1 = spira.Rectangle(p1=(0, 0), p2=(4, 10), layer=RDD.PLAYER.M5.METAL)
p2 = spira.Rectangle(p1=(0, 0), p2=(4, 12), layer=RDD.PLAYER.M5.METAL)
# FIXME: Throught a weird polygon error.
# p2 = spira.Rectangle(p1=(0, 0), p2=(4, 10), layer=RDD.PLAYER.M5.METAL)
p2.shape.move(pos=(7,0))

# --------------- NOTE: overlapping cases.
# p3 = spira.Rectangle(p1=(3, 4), p2=(8, 6), layer=RDD.PLAYER.M5.METAL)

# el += spira.Rectangle(p1=(8, 4), p2=(-4, 6), layer=RDD.PLAYER.M5.METAL)

# p3 = spira.Rectangle(p1=(-4, 4), p2=(1, 6), layer=RDD.PLAYER.M5.METAL)
# p4 = spira.Rectangle(p1=(3, 4), p2=(8, 6), layer=RDD.PLAYER.M5.METAL)

# p3 = spira.Rectangle(p1=(-4, 8), p2=(8, 12), layer=RDD.PLAYER.M5.METAL)

# p3 = spira.Rectangle(p1=(1, 9), p2=(3, 14), layer=RDD.PLAYER.M5.METAL)

# p3 = spira.Rectangle(p1=(-1, 9), p2=(5, 14), layer=RDD.PLAYER.M5.METAL)

# --------------- NOTE: Edge cases.
# p3 = spira.Rectangle(p1=(0, 10), p2=(4, 14), layer=RDD.PLAYER.M5.METAL)

# p3 = spira.Rectangle(p1=(-4, 4), p2=(0, 6), layer=RDD.PLAYER.M5.METAL)

# p3 = spira.Rectangle(p1=(4, 4), p2=(7, 6), layer=RDD.PLAYER.M5.METAL)

# p3 = spira.Rectangle(p1=(3, 10), p2=(7, 11), layer=RDD.PLAYER.M5.METAL)

# --------------- NOTE: Both cases.
# p3 = spira.Rectangle(p1=(3, 10), p2=(8, 11), layer=RDD.PLAYER.M5.METAL)
# p3 = spira.Rectangle(p1=(3, 9), p2=(8, 11), layer=RDD.PLAYER.M5.METAL)
p3 = spira.Rectangle(p1=(2, 7), p2=(7, 11), layer=RDD.PLAYER.M5.METAL)

# # # --------------- NOTE: Angle cases.
# # p3 = spira.Rectangle(p1=(1, 8), p2=(7, 11), layer=RDD.PLAYER.M5.METAL)
# p3 = spira.Rectangle(p1=(2.5, 8), p2=(7, 11), layer=RDD.PLAYER.M5.METAL)
# p3.rotate(5)
# p1.rotate(-10)

# ------------------------------------------------------------------------

el += p1
el += p2
el += p3
# el += p4

D = spira.Cell(name='Device', elements=el)

v_model = virtual_connect(device=D)
v_model.view_virtual_connect(show_layers=True, write=True)

# F = MetalConnectFilter()
# D = F(device)

# D = spira.Circuit(name='TestElectricalConnections', elements=D.elements)
# # D.gdsii_output()
# D.netlist_output()

# D = RDD.FILTERS.MASK(D)

D.netlist_view()





