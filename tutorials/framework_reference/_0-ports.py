import spira.all as spira
from spira.yevon.geometry import shapes
from spira.yevon import constants
from spira.yevon.geometry.vector import *


class PortBasics(spira.Cell):

    def create_elementals(self, elems):
        shape = shapes.RectangleShape(p1=(-2.5, -2.5), p2=(2.5, 2.5))
        elems += spira.Polygon(shape=shape, layer=spira.Layer(number=1), enable_edges=False)
        return elems

    def create_ports(self, ports):
        ports += spira.Port(midpoint=(2.5, 0), orientation=0, width=5)
        return ports


class PortVectorBasics(spira.Cell):

    def create_ports(self, ports):

        p1 = spira.Port(midpoint=(2.5,  0), orientation=0, width=5)
        p2 = spira.Port(midpoint=(0,    2.5), orientation=90, width=5)

        T = vector_match_transform(p2, p1)
        print(T)
        print(type(T))
        p2.transform(T)

        ports += p1
        ports += p2

        return ports


class PortConstants(spira.Cell):

    def create_ports(self, ports):
        ports += spira.Port(midpoint=constants.NORTH*10.0, orientation=90, width=5)
        ports += spira.Port(midpoint=constants.SOUTH*10.0, orientation=270, width=5)
        return ports


if __name__ == '__main__':

    # D = PortBasics()
    D = PortVectorBasics()
    # D = PortConstants()
    D.gdsii_output()


