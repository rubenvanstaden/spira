import spira.all as spira
from spira.yevon.geometry import shapes
from spira.yevon.geometry.coord import Coord
from spira.yevon.utils.debugging import *
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = ['Junction']


class ResistorCell(spira.Cell):

    def create_elementals(self, elems):
        elems += spira.Rectangle(alias='RES', p1=(-5, -10), p2=(5, 10), layer=RDD.PLAYER.M2.METAL)
        return elems

    def create_ports(self, ports):
        ports += self.elementals['RES'].ports['M2_e3'].unlock
        return ports


class PolygonCell(spira.Cell):

    def create_elementals(self, elems):
        elems += spira.SRef(reference=ResistorCell())
        elems += spira.Rectangle(alias='M1', p1=(-10, -15), p2=(10, 15), layer=RDD.PLAYER.M3.METAL)
        return elems


class Junction(spira.Device):

    def create_elementals(self, elems):

        D = PolygonCell()

        elems += spira.SRef(reference=D, midpoint=(0,0))

        T = spira.Translation((0, -40)) + spira.Rotation(180)
        elems += spira.SRef(reference=D, midpoint=(0,0), transformation=T)

        # R = spira.Route(
        #     port1=s1.ports['RES_e3'],
        #     port2=s2.ports['RES_e3'],
        #     ps_layer=RDD.PLAYER.RES
        # )
        # elems += spira.SRef(R)

        return elems


if __name__ == '__main__':

    cell = spira.Cell(name='TopLevel')

    D = Junction()
    S = spira.SRef(reference=D)
    cell += S

    # E = S.flat_expand_transform_copy()
    # print(E.ports)
    # E.stretch_port(port=E.ports[3], destination=E.ports[11].midpoint)
    # cell += E

    cell.gdsii_output()