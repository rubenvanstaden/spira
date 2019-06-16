import spira.all as spira
from spira.yevon.utils.elementals import get_generated_elementals, get_derived_edges

from spira.technologies.mit.process import RDD


el = spira.ElementalList()
el += spira.Rectangle(p1=(0, 0), p2=(4, 10), layer=RDD.PLAYER.M5.METAL)
el += spira.Rectangle(p1=(8, 4), p2=(-4, 6), layer=RDD.PLAYER.M5.METAL)

dl = RDD.PLAYER.M5.OVERLAP_REGION

mapping = {
    dl : RDD.PLAYER.R5.METAL
}

elems = get_derived_edges(el, mapping)

D = spira.Cell(name='Commutative Edges', elementals=elems)

D.gdsii_output()



