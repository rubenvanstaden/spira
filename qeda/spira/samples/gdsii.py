import spira
from core import param
from spira import shapes, pc
from copy import deepcopy


# points = [(0, 0), (2, 2), (2, 6), (-6, 6), (-6, -6), (-4, -4), (-4, 4), (0, 4)]
shape = shapes.RectangleShape(p1=(0,0), p2=(2*1e6,2*1e6))
shape1 = shapes.RectangleShape(p1=(-2*1e6,-2*1e6), p2=(4*1e6,4*1e6))

ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=88))
ply.move(midpoint=(1*1e6, 1*1e6), destination=(0*1e6, 0*1e6))
ply2 = spira.Polygon(shape=deepcopy(shape), gds_layer=spira.Layer(number=88))
ply2.move(midpoint=(1*1e6, 1*1e6), destination=(10*1e6, 0*1e6))

port = spira.Term(name='P1', midpoint=(1*1e6, 0*1e6), orientation=-90, pid=ply.node_id)
port1 = spira.Term(name='P2', midpoint=(10*1e6, 0*1e6), orientation=90, pid=ply2.node_id)

c0 = spira.Cell(name='ply')
c0 += ply
c0 += port
s0 = spira.SRef(c0)

c1 = spira.Cell(name='T1')
ply3 = spira.Polygon(shape=shape1, gds_layer=spira.Layer(number=100))
ply3.move(midpoint=(1*1e6, 1*1e6), destination=(0*1e6, 0*1e6))
c1 += ply3
c1 += s0

c3 = spira.SRef(c1)

c4 = spira.SRef(c1, rotation=180)
c4.reflect()
c4.move(midpoint=c4.midpoint, destination=(10*1e6, 0*1e6))


# ---------------- Top-Level Cell --------------------
cell = spira.Cell(name='TL')
# cell += spira.SRef(c1)
# cell += spira.SRef(c3)
cell += c3
cell += c4


# --------------- Apply Stretching -------------------
# for p in cell.get_ports():
#     print(p.pid)

# Tl = []
# for e in cell.elementals.sref:
#     Tl.append(e.get_transformation)
#     for e1 in e.ref.elementals.sref:
#         Tl.append(e1.get_transformation)
#         for e2 in e1.ref.elementals:
#             print(e2)
# print('')


# Tl = []
# Tl.append(c4.get_transformation)
# elems = spira.ElementList()
# ports = spira.PortList()
# for e1 in c4.ref.elementals.sref:
#     Tl.append(e1.get_transformation)
#     for e2 in e1.ref.elementals:
#         elems += e2
#     for e2 in e1.ref.ports:
#         ports += e2


# print('Transformation')
# print(Tl)
# Tl = list(reversed(Tl))

# cell_2 = spira.Cell(name='T')

# for e in elems:
#     for t in Tl:
#         e = e.transform_copy(t)
#     cell_2 += e

# for e in ports:
#     for t in Tl:
#         e = e.transform_copy(t)
#     cell_2 += e


Tl = c4.get_transformation
elems = spira.ElementList()
ports = spira.PortList()
for e1 in c4.ref.elementals.sref:
    Tl += e1.get_transformation
    for e2 in e1.ref.elementals:
        e2.transformation = Tl
        elems += e2
    # for e2 in e1.ref.ports.transform(Tl):
    for e2 in e1.ref.ports:
        ports += e2

cell_2 = spira.Cell(name='T')
for e in elems:
    cell_2 += e
for e in ports:
    cell_2 += e
cell_2.output()




c4 = update_transforms(cell=c4)


# cell.output()



