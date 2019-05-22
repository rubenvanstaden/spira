import spira.all as spira
from spira.yevon.geometry import shapes
from spira.yevon.geometry.coord import Coord
from spira.yevon.rdd import get_rule_deck


RDD = get_rule_deck()


class ResistorCell(spira.Cell):

    def create_elementals(self, elems):
        elems += spira.Rectangle(alias='RES', p1=(-5*1e6, -10*1e6), p2=(5*1e6, 10*1e6), ps_layer=RDD.PLAYER.RES)
        return elems

    def create_ports(self, ports):

        ply = self.elementals['RES']

        ply.ports['RES_e3'].locked = False

        ports += ply.ports['RES_e3']

        return ports


class PolygonCell(spira.Cell):

    def create_elementals(self, elems):

        c1 = ResistorCell()
        s1 = spira.SRef(c1)
        elems += s1

        elems += spira.Rectangle(alias='M1', p1=(-10*1e6, -15*1e6), p2=(10*1e6, 15*1e6), ps_layer=RDD.PLAYER.COU)

        return elems


class Junction(spira.Cell):

    def create_elementals(self, elems):

        c1 = PolygonCell()

        s1 = spira.SRef(c1, midpoint=(0,0))
        elems += s1

        T = spira.Translation((0*1e6, -40*1e6)) + spira.Rotation(180)
        s2 = spira.SRef(c1, midpoint=(0,0), transformation=T)
        elems += s2
        
        # port1 = s1.ports['RES_e3']
        # port2 = s2.ports['RES_e3']

        # print(port1)
        # print(port2)

        # R = spira.Route(
        #     port1=s1.ports['RES_e3'],
        #     port2=s2.ports['RES_e3'],
        #     ps_layer=RDD.PLAYER.RES
        # )
        # elems += spira.SRef(R)

        return elems

        # expand_elems = elems.expand_transform()
        # print(expand_elems)
        # return expand_elems


from spira.yevon.netlist.containers import __CellContainer__
class JunctionStretch(__CellContainer__):

    def create_elementals(self, elems):
        elems = self.cell.elementals
        return elems

    def create_ports(self, ports):
        # elems = self.cell.elementals
        return ports


def stretch_port_to_port(p1, p2):
    pass


if __name__ == '__main__':

    cell = spira.Cell(name='TopLevel')

    D = Junction()
    S = spira.SRef(reference=D)
    # cell += S

    E = S.flat_expand_transform_copy()
    # print(E.ref.elementals)
    # print(E.ref.elementals['RES_M=(0,0)-R=0.0-RF=False-MN=1'])
    print(E.ports)
    print(E.ports[7])
    print(E.ports[16])
    p0 = E.ports[5]
    p1 = E.ports[7]
    p2 = E.ports[16]
    # diff_coord = p2.midpoint - p1.midpoint
    d0 = p0.midpoint.distance(p1.midpoint)
    d1 = p0.midpoint.distance(p2.midpoint)
    print(d0, d1)
    sf = d1/d0
    print(sf)
    print("\n South Ports")
    print(E.ports.north_ports)
    T = spira.Stretch(stretch_factor=(1,sf), stretch_center=p0.midpoint)
    T.apply(E.ref.elementals['RES_M=(0,0)-R=0.0-RF=False-MN=1'])
    cell += E

    # # C = JunctionStretch(cell=S.flat_expand_transform_copy())
    
    # T = spira.Stretch(stretch_factor=(2,1))
    # S1 = S.stretch(T)
    # cell += S1

    cell.output()
