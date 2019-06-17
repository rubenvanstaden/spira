import spira.all as spira
from spira.yevon.utils.elementals import ElectricalConnections

from spira.technologies.mit.process import RDD


el = spira.ElementalList()
el += spira.Rectangle(p1=(0, 0), p2=(4, 10), layer=RDD.PLAYER.M5.METAL)
# el += spira.Rectangle(p1=(-4, 8), p2=(8, 12), layer=RDD.PLAYER.M5.METAL)
el += spira.Rectangle(p1=(-4, 4), p2=(1, 6), layer=RDD.PLAYER.M5.METAL)
el += spira.Rectangle(p1=(3, 4), p2=(8, 6), layer=RDD.PLAYER.M5.METAL)

device = spira.Cell(name='Device', elementals=el)

# elems = derived_edges(el)

ec = ElectricalConnections(cell=device)
# ec.gdsii_output_electrical_connection()

D = spira.Circuit(name='TestElectricalConnections', elementals=ec.connected_elementals)
# D = spira.Circuit(name='TestElectricalConnections', elementals=el)
D.netlist_output()





