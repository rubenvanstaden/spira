import spira.all as spira
from spira.yevon.geometry import shapes
from spira.yevon.geometry.coord import Coord
from spira.yevon import process as pc
from spira.yevon.rdd import get_rule_deck
from samples.ex_junction import Junction


RDD = get_rule_deck()


class Jtl(spira.Cell):

    routes = spira.DataField(fdef_name='create_routes')

    def get_transforms(self):
        t1 = spira.Translation(Coord(0*1e6, 0*1e6))
        t2 = spira.Translation(Coord(150*1e6, 0*1e6))
        return [t1, t2]

    def create_routes(self):
        routes = spira.ElementList()
        routes += pc.Rectangle(p1=(9*1e6, -10*1e6), p2=(142*1e6, -2*1e6), ps_layer=RDD.PLAYER.COU)
        routes += pc.Rectangle(p1=(-40*1e6, -10*1e6), p2=(0*1e6, -2*1e6), ps_layer=RDD.PLAYER.COU)
        return routes

    def create_elementals(self, elems):
        t1, t2 = self.get_transforms()

        jj = Junction()

        s_top = spira.SRef(alias='S1', reference=jj, transformation=t1)
        s_bot = spira.SRef(alias='S2', reference=jj, transformation=t2)

        for r in self.routes:
            elems += r

        elems += s_top
        elems += s_bot

        return elems

    # def create_ports(self, ports):

    #     ports += spira.Terminal(midpoint=(-40*1e6, -6*1e6), width=8*1e6, orientation=0)
    #     # ports += spira.Terminal(midpoint=(), width=10*1e6, orientation=180)

    #     return ports


# -------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':

    jtl= Jtl()

    jtl.expand_transform()

    for k, v in jtl['Junction_S1'].alias_cells.items():
        print(k, v)

    ply = jtl['Junction_S1']['Jj_S0']['J5']

    ply.stretch(sx=1, sy=2)

    print('\n--- Elementals ---')
    for e in jtl.elementals:
        print(e)
    print('')

    c1 = spira.Cell(name='C1')

    cell = jtl.flat_polygons(subj=c1)
    # cell = jtl.flat_copy(level=1)

    print('\n--- Compressed Elementals ---')
    for e in cell.elementals:
        print(e)
    print('')

    for e1 in cell.elementals:
        for e2 in cell.elementals:
            if e1 != e2:
                for p1 in e1.ports:
                    p_ply = p1.edge
                    e_ply = e2.elementals[0]
                    if p_ply & e_ply:
                        # ply = p_ply & e_ply
                        # ply.gds_layer.datatype = 88
                        # p1.edge = ply
                        p1.edgelayer.datatype=88

    topcell = spira.Cell(name='TopCell')
    topcell += spira.SRef(jtl)
    topcell += spira.SRef(cell)

    topcell.output()


