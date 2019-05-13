import spira.all as spira
from spira.yevon.geometry import shapes
from spira.yevon.geometry.coord import Coord
from spira.yevon.rdd import get_rule_deck
from spira.yevon import process as pc
from spira.netex.containers import __CellContainer__


RDD = get_rule_deck()


class A(spira.Cell):
    """ Cell with boxes to stretch a SRef containing two polygons. """

    def get_polygons(self):
        p1 = pc.Rectangle(p1=(0, 0), p2=(10*1e6, 2*1e6), ps_layer=RDD.PLAYER.COU)
        p2 = pc.Rectangle(p1=(10*1e6, 0), p2=(20*1e6, 2*1e6), ps_layer=RDD.PLAYER.COU)
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
        p1 = pc.Rectangle(alias='M0', p1=(0, 0), p2=(10*1e6, 2*1e6), ps_layer=RDD.PLAYER.COU)
        p2 = pc.Rectangle(alias='M1', p1=(0*1e6, 0), p2=(10*1e6, 2*1e6), ps_layer=RDD.PLAYER.COU)
        c = spira.Cell(name='1')
        c += p2
        S = spira.SRef(c, midpoint=(5*1e6, 0))
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
        return elems

    def create_ports(self, ports):
        elems = self.cell.elementals
        ports = elems[0].ports & elems[1]
        return ports


if __name__ == '__main__':

    cell = spira.Cell(name='TopLevel')

    # D1 = A()
    # cell += spira.SRef(D1, midpoint=(0,0))

    D1 = B()
    S = spira.SRef(D1, midpoint=(0,0))

    D = S.flat_expand()

    connector = Connector(cell=D)
    # connector.output()

    cell += spira.SRef(connector)
    cell += S
    cell.output()

