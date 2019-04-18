import spira.all as spira
from spira.yevon.geometry import shapes


class ProcessLayer(spira.Cell):

    def create_elementals(self, elems):

        shape = shapes.RectangleShape(p1=(0,0), p2=(50*1e6, 5*1e6))
        ply = spira.Polygon(shape=shape, gds_layer=spira.Layer(number=1))
        elems += ply

        return elems

    def create_ports(self, ports):

        ports += spira.Term(midpoint=(0, 2.5*1e6), width=5*1e6)

        return ports


if __name__ == '__main__':

    pc = ProcessLayer()

    print(pc.ports)

    pc.output()
    

