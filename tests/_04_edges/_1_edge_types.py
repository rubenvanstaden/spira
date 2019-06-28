import numpy as np
import spira.all as spira
from spira.yevon import constants
from spira.yevon.geometry.edges.edges import *
from spira.technologies.mit.process import RDD


p1 = spira.Rectangle(p1=(0, 0), p2=(4, 10), layer=RDD.PLAYER.M5.METAL)

elems = spira.ElementalList()
elems += p1
for edge in p1.edges:
    for e in edge.elementals:
        elems += e.transform(edge.transformation)

D = spira.Cell(name='Edge', elementals=elems)

D.gdsii_output()

