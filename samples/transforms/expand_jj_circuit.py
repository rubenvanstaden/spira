import spira.all as spira
from spira.yevon.geometry import shapes
from spira.yevon.geometry.coord import Coord
from expand_junction import Junction
from spira.netex.containers import __CellContainer__
from spira.yevon import process as pc
from spira.yevon.rdd import get_rule_deck


RDD = get_rule_deck()


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
                    e1 = elems[i]
                    e2 = elems[j]
                    if e1.ps_layer == e2.ps_layer:
                        pl = elems[i].ports & elems[j]
                        for p in pl:
                            ports += p
        return ports


class Jtl(spira.Cell):

    def get_transforms(self):
        t1 = spira.Translation(Coord(0*1e6, 0*1e6))
        t2 = spira.Translation(Coord(150*1e6, 0*1e6))
        return [t1, t2]

    def get_routes(self):
        shape_rectangle = shapes.RectangleShape(p1=(10*1e6, -5.6*1e6), p2=(40*1e6, 7.6*1e6))
        r1 = pc.Polygon(points=shape_rectangle.points, ps_layer=RDD.PLAYER.COU)
        shape_rectangle = shapes.RectangleShape(p1=(-10*1e6, -5.6*1e6), p2=(-40*1e6, 7.6*1e6))
        r2 = pc.Polygon(points=shape_rectangle.points, ps_layer=RDD.PLAYER.COU)
        # ply = spira.Polygon(alias='M4', shape=shape_rectangle, gds_layer=spira.Layer(number=5))
        return r1, r2

    def create_elementals(self, elems):
        t1, t2 = self.get_transforms()

        jj = Junction()

        # s_top = spira.SRef(alias='S1', reference=jj, transformation=t1)
        s_top = spira.SRef(alias='S1', reference=jj)

        r1, r2 = self.get_routes()

        elems += r1
        elems += r2
        elems += s_top

        return elems


# --------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':

    cell = spira.Cell(name='TopLevel')

    D = Jtl()

    S = spira.SRef(D, midpoint=(0,0))

    X = S.flat_expand()
    # X.output()

    connector = Connector(cell=X)
    connector.ports
    # connector.output()

    # # cell += spira.SRef(connector)
    cell += S

    cell.output()


