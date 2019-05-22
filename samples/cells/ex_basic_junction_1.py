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

        elems += spira.Rectangle(p1=(-10*1e6, -15*1e6), p2=(10*1e6, 15*1e6), ps_layer=RDD.PLAYER.COU)

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


if __name__ == '__main__':

    cell = spira.Cell(name='TopLevel')

    D = Junction()
    S = spira.SRef(reference=D)

    # C = JunctionStretch(cell=S.flat_expand_transform_copy())
    
    T = spira.Stretch(stretch_factor=(2,1))
    S1 = T(S)
    cell += S1

    cell.output()
