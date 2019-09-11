import spira.all as spira
from spira.yevon.geometry import shapes
from spira.yevon.geometry.coord import Coord
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
        elems += spira.SRef(alias='Sr1', reference=ResVia(), transformation=t2)
        elems += spira.Rectangle(p1=(-10, -23), p2=(10, 10), layer=RDD.PLAYER.M2.METAL)
        return elems


class Bot(spira.Cell):

    def get_transforms(self):
        t1 = spira.Translation((0, 0))
        t2 = spira.Translation((0, -30))
        return [t1, t2]

    def create_elements(self, elems):
        t1, t2 = self.get_transforms()
        elems += spira.SRef(alias='Sr2', reference=ResVia(), transformation=t2)
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


class Jtl(spira.Cell):

    def get_transforms(self):
        t1 = spira.Translation(Coord(0, 0))
        t2 = spira.Translation(Coord(150, 0))
        return [t1, t2]

    def create_elements(self, elems):
        t1, t2 = self.get_transforms()

        jj = Junction()

        elems += spira.SRef(alias='ref_jj1', reference=jj, transformation=t1)
        elems += spira.SRef(alias='ref_jj2', reference=jj, midpoint=(150, 0))
        # elems += spira.SRef(alias='ref_jj2', reference=jj, transformation=t2)

        # elems += spira.Rectangle(p1=(7, -13), p2=(143, 1), layer=spira.Layer(number=2))
        elems += spira.Rectangle(p1=(7, -13), p2=(143, 1), layer=RDD.PLAYER.M2.METAL)

        return elems


# --------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':

    jtl = Jtl()

    C = spira.Cell(name='TestingCell')

    S = spira.SRef(alias='Jj', reference=jtl)
    S.stretch_p2p(port_name='ref_jj1:S1:Sr1:R1:E3', destination_name='ref_jj1:S2:Sr2:R1:E1')
    
    C += S

    # D = C.expand_flat_copy()
    # D = C.expand_transform()
    D = C

    # D.gdsii_view()
    # C.gdsii_view()

    D.gdsii_output(file_name='stretch_2')


