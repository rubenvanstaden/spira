import spira.all as spira
from spira.yevon.geometry import shapes
from spira.yevon.geometry.coord import Coord
from spira.yevon import process as pc
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


class Jj(spira.Cell):

    def create_elements(self, elems):
        elems += spira.Convex(radius=7.0, layer=RDD.PLAYER.C2.VIA)
        return elems


class ResVia(spira.Cell):

    def create_elements(self, elems):
        elems += spira.Rectangle(p1=(-7.5, -13.2), p2=(7.5, -8.2), layer=RDD.PLAYER.R1.METAL)
        elems += spira.Rectangle(p1=(-4, -12), p2=(4.1, -10), layer=RDD.PLAYER.C1.VIA)
        return elems


class Top(spira.Cell):

    def get_transforms(self):
        t1 = spira.Translation((0, 0))
        t2 = spira.Translation((0, -8))
        return [t1, t2]

    def create_elements(self, elems):
        t1, t2 = self.get_transforms()
        elems += spira.SRef(alias='Sj1', reference=Jj(), transformation=t1)
        elems += spira.SRef(alias='Sr1', reference=ResVia(), midpoint=(0, -8))
        elems += spira.Rectangle(p1=(-10, -23), p2=(10, 10), layer=RDD.PLAYER.M2.METAL)
        return elems


class Bot(spira.Cell):

    def get_transforms(self):
        t1 = spira.Translation((0, 0))
        t2 = spira.Translation((0, -30))
        return [t1, t2]

    def create_elements(self, elems):
        t1, t2 = self.get_transforms()
        elems += spira.SRef(alias='Sr2', reference=ResVia(), midpoint=(0, -30))
        elems += spira.Rectangle(p1=(-10, -55), p2=(10, -35), layer=RDD.PLAYER.M2.METAL)
        return elems


class Junction(spira.Cell):
    """ Josephson junction. """

    def get_transforms(self):
        t1 = spira.Translation((0, 0))
        t2 = spira.Translation((0, -5))
        return [t1, t2]

    def create_elements(self, elems):
        t1, t2 = self.get_transforms()
        elems += spira.Rectangle(p1=(-13, -60), p2=(13, 12), layer=RDD.PLAYER.M1.METAL)
        elems += spira.SRef(alias='S1', reference=Top(), transformation=t1)
        elems += spira.SRef(alias='S2', reference=Bot(), midpoint=(0, -5))
        return elems


if __name__ == '__main__':

    D = Junction()

    C = spira.Cell(name='TestingCell')

    S = spira.SRef(alias='Jj', reference=D)

    print(S.reference.elements['S1'])
    
    # S.reference.elements['S1'].stretch_by_factor(factor=(2,1))

    # S.stretch_by_factor(factor=(2,1))
    # S.stretch_p2p(port_name='Jj:S1:Sr1:E3_R1', destination_name='Jj:S2:Sr2:E1_R1')
    # S.stretch_p2p(port_name='Jj:S1:Sr1:R1:E3', destination_name='Jj:S2:Sr2:R1:E1')
    # S.stretch_p2c(port_name='S1:Sr1:E3_R1', destination_name='S2:Sr2:E1_R1')
    
    # S.stretch_p2p(port_name='S1:Sr1:R1:E3', destination_name='S2:Sr2:R1:E1')

    C += S

    # D = C.expand_flat_copy()
    D = C

    # print(D.elements)

    # print('\n*************************************')
    # for e in D.elements.polygons:
    #     print(e.ports)
    #     # print(e.location_name)

    # D.gdsii_view()
    
    # D.gdsii_output(file_name='expaneded')
    # D.gdsii_output(file_name='original')
    D.gdsii_output(file_name='stretch')



