import spira.all as spira
from spira.yevon import constants
from spira.yevon.geometry.vector import *


class PortBasics(spira.Cell):

    def create_ports(self, ports):

        ports += spira.Terminal(midpoint=(2.5*1e6,  0*1e6), orientation=0, width=5*1e6)
        ports += spira.Terminal(midpoint=(0*1e6,    2.5*1e6), orientation=90, width=5*1e6)
        ports += spira.Terminal(midpoint=(-2.5*1e6, 0*1e6), orientation=180, width=5*1e6)
        ports += spira.Terminal(midpoint=(0*1e6,    -2.5*1e6), orientation=270, width=5*1e6)

        return ports


class PortVectorBasics(spira.Cell):

    def create_ports(self, ports):

        p1 = spira.Terminal(midpoint=(2.5*1e6,  0*1e6), orientation=0, width=5*1e6)
        p2 = spira.Terminal(midpoint=(0*1e6,    2.5*1e6), orientation=90, width=5*1e6)

        T = vector_match_transform(p2, p1)
        print(T)
        print(type(T))
        p2.transform(T)

        ports += p1
        ports += p2

        return ports


class PortConstants(spira.Cell):

    def create_ports(self, ports):

        p1 = spira.Terminal(midpoint=constants.NORTH*1e6, orientation=90, width=5*1e6)
        p2 = spira.Terminal(midpoint=constants.SOUTH*1e6, orientation=270, width=5*1e6)

        ports += p1
        ports += p2

        return ports


if __name__ == '__main__':

    # D = PortBasics()
    # D = PortVectorBasics()
    D = PortConstants()
    D.output()


