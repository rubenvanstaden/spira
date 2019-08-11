import numpy as np

from spira.technologies.mit.process import RDD

import spira.all as spira


class NetBranchTest(spira.Circuit):
    """  """

    @spira.cache()
    def get_ports(self):
        p1 = spira.Port(name='M6:P1', midpoint=(0,0), orientation=0)
        p2 = spira.Port(name='M6:P2', midpoint=(5,15), orientation=270)
        p3 = spira.Port(name='M6:P3', midpoint=(10,0), orientation=180)
        return [p1, p2, p3]

    def create_elements(self, elems):
        elems += spira.Rectangle(p1=(0, -0.5), p2=(10, 0.5), layer=RDD.PLAYER.M5.METAL)
        elems += spira.Rectangle(p1=(4.5, 0), p2=(5.5, 15), layer=RDD.PLAYER.M5.METAL)
        return elems

    def create_ports(self, ports):
        ports += self.get_ports()
        return ports


if __name__ == '__main__':

    D = NetBranchTest()

    D = RDD.FILTERS.MASK(D)

    # D.gdsii_view()
    D.netlist_view()


