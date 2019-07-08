import spira.all as spira
from spira.yevon.geometry import shapes
from spira.yevon.geometry.coord import Coord
from tests._05_transforms.expand_junction import Junction
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


class Jtl(spira.Cell):

    def get_transforms(self):
        t1 = spira.Translation(Coord(0, 0))
        t2 = spira.Translation(Coord(150, 0))
        return [t1, t2]

    def create_elements(self, elems):
        t1, t2 = self.get_transforms()

        jj = Junction()

        elems += spira.SRef(alias='ref_jj1', reference=jj, transformation=t1)
        elems += spira.SRef(alias='ref_jj2', reference=jj, transformation=t2)

        elems += spira.Rectangle(p1=(7, -13), p2=(143, 1), layer=spira.Layer(number=2))

        return elems


# --------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':

    jtl = Jtl()
    
    C = spira.Cell(name='TestingCell')

    S = spira.SRef(alias='Jj', reference=jtl)

    S.stretch_p2p(port_name='ref_jj1:S1:Sr1:E3_R1', destination_name='ref_jj1:S2:Sr2:E1_R1')

    C += S

    C.gdsii_output()
    # C.gdsii_expanded_output()


