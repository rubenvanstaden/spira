import spira.all as spira
import numpy as np
from spira.yevon.vmodel.connections import ElectricalConnections

from spira.technologies.mit.process import RDD


el = spira.ElementalList()

# Main Polygon
p1 = spira.Rectangle(p1=(0, 0), p2=(4, 10), layer=RDD.PLAYER.M5.METAL)
p2 = spira.Rectangle(p1=(0, 0), p2=(4, 12), layer=RDD.PLAYER.M5.METAL)
# FIXME: Throught a weird polygon error.
# p2 = spira.Rectangle(p1=(0, 0), p2=(4, 10), layer=RDD.PLAYER.M5.METAL)
p2.shape.move(pos=(7,0))
el += p1
el += p2

# # Main Cell
# c1 = spira.Cell(name='Ply1')
# c1 += spira.Rectangle(p1=(0, 0), p2=(4, 10), layer=RDD.PLAYER.M5.METAL)
# el += spira.SRef(reference=c1)

# # T0
# el += spira.Rectangle(p1=(3, 4), p2=(8, 6), layer=RDD.PLAYER.M5.METAL)

# # T6
# el += spira.Rectangle(p1=(8, 4), p2=(-4, 6), layer=RDD.PLAYER.M5.METAL)

# el += spira.Rectangle(p1=(-4, 4), p2=(1, 6), layer=RDD.PLAYER.M5.METAL)
# el += spira.Rectangle(p1=(3, 4), p2=(8, 6), layer=RDD.PLAYER.M5.METAL)

# el += spira.Rectangle(p1=(-4, 8), p2=(8, 12), layer=RDD.PLAYER.M5.METAL)

# el += spira.Rectangle(p1=(1, 9), p2=(3, 14), layer=RDD.PLAYER.M5.METAL)

# el += spira.Rectangle(p1=(-1, 9), p2=(5, 14), layer=RDD.PLAYER.M5.METAL)

el += spira.Rectangle(p1=(0, 10), p2=(4, 14), layer=RDD.PLAYER.M5.METAL)

from spira.yevon.vmodel.virtual import virtual_connect
from spira.yevon.geometry.shapes.modifiers import ShapeConnected
from spira.yevon.filters.boolean_filter import MetalConnectFilter
from spira.yevon.geometry.shapes.shape import Shape
from copy import deepcopy

device = spira.Cell(name='Device', elementals=el)

D = device

v_model = virtual_connect(device=D)
# v_model.gdsii_output_virtual_connect()


# points = np.array)([])
for i, e1 in enumerate(D.elementals):
    points = []
    for e2 in D.elementals:
        e1 = deepcopy(e1)
        e2 = deepcopy(e2)
        if e1 != e2:
            overlap_shape = e1.shape.intersections(e2.shape)
            points.extend(overlap_shape.points.tolist())
    print('[--] Overlapping shape points:')
    print(points)

# for i, p in enumerate(D.elementals):

    # e1.shape = ShapeConnected(original_shape=e1.shape, overlapping_shape=Shape(points), edges=v_model.connected_edges)
    D.elementals[i].shape = ShapeConnected(original_shape=e1.shape, overlapping_shape=Shape(points), edges=v_model.connected_edges)
    print('---------')
    print(e1.shape.points)

    # if i == 2:
    #     e1.shape = ShapeConnected(original_shape=e1.shape, overlapping_shape=Shape(points), edges=v_model.connected_edges)
    #     print('---------')
    #     print(e1.shape.points)

# device.gdsii_output()

# F = MetalConnectFilter()
# D = F(device)


print('\n[--] Elementals:')
for i, p in enumerate(D.elementals):
    print(p)
    print(type(p.shape))
    print(p.shape.points)
    print('')

D.gdsii_output()

D = spira.Circuit(name='TestElectricalConnections', elementals=D.elementals)
D.netlist_output()





