import spira.all as spira
from spira.yevon.geometry import shapes
from spira.yevon.geometry.coord import Coord
from spira.yevon.netlist.containers import __CellContainer__
from copy import deepcopy
from spira.yevon.rdd import get_rule_deck


RDD = get_rule_deck()


class A(spira.Cell):
    """ Cell with boxes to stretch a SRef containing two polygons. """

    def get_polygons(self):
        p1 = spira.Rectangle(p1=(0, 0), p2=(10*1e6, 2*1e6), layer=RDD.PLAYER.M1.METAL)
        p2 = spira.Rectangle(p1=(10*1e6, 0), p2=(20*1e6, 2*1e6), layer=RDD.PLAYER.M1.METAL)
        return [p1, p2]

    def create_elementals(self, elems):
        elems += self.get_polygons()
        return elems

    def create_ports(self, ports):
        p1, p2 = self.get_polygons()
        ports = p1.ports & p2
        return ports


class B(spira.Cell):
    """ Cell with boxes to stretch a SRef containing two polygons. """

    def get_polygons(self):
        p1 = spira.Rectangle(alias='M0', p1=(0,0), p2=(12*1e6, 2*1e6), layer=RDD.PLAYER.M1.METAL)
        c = spira.Cell(name='1')
        c += spira.Rectangle(alias='M1', p1=(0,0), p2=(10*1e6, 2*1e6), layer=RDD.PLAYER.M1.METAL)
        S = spira.SRef(c, midpoint=(10*1e6, 0))
        return [p1, S]

    def create_elementals(self, elems):
        elems += self.get_polygons()
        return elems

    # def create_ports(self, ports):
    #     p1, p2 = self.get_polygons()
    #     ports = p1.ports & p2
    #     return ports


class Connector(__CellContainer__):
    """ Contains the expanded cell for connection detection. """

    def create_elementals(self, elems):
        elems = self.cell.elementals
        # p_and = elems[0] & elems[1]
        p1 = deepcopy(elems[0])
        p2 = deepcopy(elems[1])
        p1.shape = p1.shape.transform(p1.transformation)
        p2.shape = p2.shape.transform(p2.transformation)
        p_and = p1 & p2
        for p in p_and:
            p.layer = spira.Layer(2)
            elems += p
        return elems

    def create_ports(self, ports):
        from spira.yevon.visualization.viewer import PortLayout
        elems = self.cell.elementals

        for p in elems[0].ports:
            print(p)

        L = PortLayout(port=elems[0].ports[2])

        s1 = elems[1].shape.transform_copy(elems[1].transformation)
        s2 = L.edge.shape.transform_copy(L.edge.transformation)
        # rp = s1 & s2
        rp = s1.intersection(s2)
        print(s2.points)
        print(rp)
        if rp:
            print(elems[0].ports[2])
            ports += elems[0].ports[2].unlock

        print(ports)

        # # ports = elems[2].ports & elems[2]
        return ports


if __name__ == '__main__':

    cell = spira.Cell(name='TopLevel')

    # D1 = A()
    # cell += spira.SRef(D1, midpoint=(0,0))

    D1 = B()
    S = spira.SRef(D1, midpoint=(0,0))

    D = S.flat_expand_transform_copy()

    connector = Connector(cell=D.ref)
    connector.output()

    # # cell += D
    # cell += S
    # cell.output()

