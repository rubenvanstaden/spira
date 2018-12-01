import spira
import spira.kernel.parameters as param
from spira import SRef
from spira.rdd.mitll import RDD
from .templates import __TempateDevice__


class JunctionModel(__TempateDevice__):

    gdsdatatype = param.IntegerField(default=3)

    def create_elementals(self, elems):

        i4 = SRef(RDD.VIAS.I4.PCELL, origin=(0,0))
        i5 = SRef(RDD.VIAS.I5.PCELL, origin=(0,0))
        j5 = SRef(RDD.VIAS.J5.PCELL, origin=(0,0))
        c5 = SRef(RDD.VIAS.C5.PCELL, origin=(0,0))

        elems += i4
        elems += i5
        elems += j5
        elems += c5

        return elems



