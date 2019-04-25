import spira.all as spira
from spira.yevon.geometry import shapes


class A(spira.Cell):

    def create_elementals(self, elems):

        shape = shapes.RectangleShape(p1=(0,0), p2=(10*1e6, 50*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=11))
        elems += ply

        return elems

    def create_ports(self, ports):

        ports += spira.Terminal(name='P2', midpoint=(5*1e6, 50*1e6), orientation=0, width=10*1e6)

        return ports


class Canvas(spira.Cell):

    def create_elementals(self, elems):

        return elems

    def create_ports(self, ports):

        ports += spira.Terminal(name='P1', midpoint=(20*1e6, 0*1e6), orientation=90, width=10*1e6)

        return ports


if __name__ == '__main__':

    canvas = Canvas()

    a = A()

    sa = spira.SRef(a)

    sa.connect(port=sa.ports['P2'], destination=canvas.ports['P1'])

    canvas += sa

    canvas.output()

