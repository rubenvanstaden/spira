import spira.all as spira
from spira.yevon import filters
from spira.yevon import constants
from spira.all import RDD


ply1 = spira.Rectangle(p1=(0,0), p2=(10,2), layer=RDD.PLAYER.M1.METAL)
D = spira.Cell(name='TopLevel', elements=[ply1])

# D += ply1.edges

for edge in ply1.edges:
    EF = filters.EdgeToPolygonFilter()
    D += EF(edge)

# for e in ply1.edges:
    # D += spira.EdgeAdapter(original_edge=e, edge_type=constants.EDGE_TYPE_OUTSIDE)

# EF = filters.EdgeFilter(edge_type=constants.EDGE_TYPE_OUTSIDE)
# D = EF(D)

D.gdsii_output(file_name='Edges')



