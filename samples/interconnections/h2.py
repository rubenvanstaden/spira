import spira.all as spira
from spira.yevon.geometry import shapes
from spira.yevon.geometry.coord import Coord
from spira.yevon import process as pc
from spira.netex.containers import __CellContainer__
from spira.yevon.rdd import get_rule_deck


RDD = get_rule_deck()


class Poly(spira.Cell):

    def get_polygons(self):
        p1 = pc.Rectangle(p1=(0, 0), p2=(10*1e6, 2*1e6), ps_layer=RDD.PLAYER.COU)
        p2 = pc.Rectangle(p1=(0, 0), p2=(10*1e6, 4*1e6), ps_layer=RDD.PLAYER.COU)
        p3 = pc.Rectangle(p1=(0, 0), p2=(10*1e6, 6*1e6), ps_layer=RDD.PLAYER.COU)
        return p1, p2, p3


class H1(Poly):

    def create_elementals(self, elems):
        p1, p2, p3 = self.get_polygons()
        elems += p1
        return elems        


class H2(Poly):

    def create_elementals(self, elems):

        p1, p2, p3 = self.get_polygons()
        elems += p2

        c = H1()
        S = spira.SRef(c, midpoint=(10*1e6, 0))
        elems += S

        return elems


class H3(Poly):

    def create_elementals(self, elems):

        p1, p2, p3 = self.get_polygons()
        elems += p3

        c = H2()
        S = spira.SRef(c, midpoint=(10*1e6, 0))
        elems += S

        return elems


class Connector(__CellContainer__):
    """ Contains the expanded cell for connection detection. """

    def create_elementals(self, elems):
        elems = self.cell.elementals
        return elems

    def create_ports(self, ports):
        elems = self.cell.elementals
        # ports = elems[0].ports & elems[1]
        # ports = elems[0].ports
        for i in range(len(elems)):
            for j in range(len(elems)):
                if i != j:
                    pl = elems[i].ports & elems[j]
                    for p in pl:
                        ports += p
        return ports


if __name__ == '__main__':

    cell = spira.Cell(name='TopLevel')

    # D = H1()
    # D = H2()
    D = H3()
    S = spira.SRef(D, midpoint=(0,0))

    connector = Connector(cell=S.flat_expand())
    connector.ports
    # connector.output()

    # cell += spira.SRef(connector)
    cell += S
    cell.output()


