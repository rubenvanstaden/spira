import spira.all as spira
from spira.yevon.geometry import shapes
from spira.yevon.geometry.coord import Coord
from spira.yevon.utils.debugging import *
from spira.yevon.geometry.route.routes import RouteStraight
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = ['Junction']


class ResistorCell(spira.Cell):

    def create_elements(self, elems):
        elems += spira.Rectangle(alias='RES', p1=(-5, -10), p2=(5, 10), layer=RDD.PLAYER.M2.METAL)
        return elems

    def create_ports(self, ports):
        ports += self.elements['RES'].ports['E3_M2']
        return ports


class PolygonCell(spira.Cell):

    res = spira.Parameter(fdef_name='create_res')
    
    def create_res(self):
        res = ResistorCell()
        s = spira.SRef(reference=res)
        return s

    def create_elements(self, elems):
        # elems += spira.SRef(reference=ResistorCell())
        elems += self.res
        elems += spira.Rectangle(alias='M3', p1=(-10, -15), p2=(10, 15), layer=RDD.PLAYER.M3.METAL)
        return elems

    def create_ports(self, ports):
        ports += self.res.ports['E0_M2'].copy(name='P0_M2')
        ports += self.res.ports['E2_M2'].copy(name='P1_M2')
        return ports


class Junction(spira.Device):

    def get_transforms(self):
        t1 = spira.Translation((0,0))
        t2 = spira.Translation((0, -40)) + spira.Rotation(180)
        return (t1, t2)

    def create_elements(self, elems):
        t1, t2 = self.get_transforms()

        D = PolygonCell()
        s1 = spira.SRef(reference=D, transformation=t1)
        s2 = spira.SRef(reference=D, transformation=t2)

        # print(s1.ports)
        # print(s2.ports)

        # elems += RouteStraight(
        #     p1=s1.ports['M2_P1'],
        #     p2=s2.ports['M2_P1'],
        #     layer=RDD.PLAYER.M2.METAL)

        elems += [s1, s2]

        return elems

    # def create_ports(self, ports):
    #     t1, t2 = self.get_transforms()
    #     # ports += self.elementals[0].ports['M2_e2'].copy(name='M2_P0').unlock
    #     # ports += self.elementals[1].ports['M2_e0'].copy(name='M2_P1').unlock
    #     return ports


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
