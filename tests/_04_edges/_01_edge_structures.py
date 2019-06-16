import numpy as np
import spira.all as spira
from spira.yevon import constants
from spira.yevon.structure.edges import generate_polygon_edges
from spira.technologies.mit.process import RDD


p1 = spira.Rectangle(p1=(0, 0), p2=(4*1e6, 10*1e6), layer=RDD.PLAYER.M5.METAL)
edges = generate_polygon_edges(shape=p1.shape, layer=p1.layer)

elems = spira.ElementalList()
elems += p1
for edge in edges:
    for e in edge.elementals:
        elems += e.transform(edge.transformation)

D = spira.Cell(name='Edge', elementals=elems)

D.gdsii_output()

