import spira
from spira import param
from spira.lgm.route.manhattan_base import RouteManhattan


class Test_Manhattan_180(spira.Cell):
    """ Routes with ports facing eachother in a 180 degree. """

    def test_q1_180(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(40*1e6,20*1e6), orientation=180, width=2*1e6)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(0,0*1e6))

    def test_q2_180(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(-40*1e6,20*1e6), orientation=180, width=2*1e6)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(0*1e6,200*1e6))

    def test_q3_180(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=180, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(-40*1e6,-20*1e6), orientation=0, width=2*1e6)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(0*1e6,400*1e6))

    def test_q4_180(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=180, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(40*1e6,-20*1e6), orientation=0, width=2*1e6)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(0*1e6,600*1e6))

    def create_elementals(self, elems):

        elems += self.test_q1_180()
        elems += self.test_q2_180()
        elems += self.test_q3_180()
        elems += self.test_q4_180()

        return elems


class Test_Manhattan_90(spira.Cell):
    """ Routes with ports facing eachother in a 90 degree. """

    def test_q1_90(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(40*1e6,20*1e6), orientation=90, width=2*1e6)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(200*1e6,0*1e6))

    def test_q2_90(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(-40*1e6,20*1e6), orientation=-90, width=2*1e6)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(200*1e6,200*1e6))

    def test_q3_90(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=180, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(-40*1e6,-20*1e6), orientation=-90, width=2*1e6)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(200*1e6,400*1e6))

    def test_q4_90(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=180, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(40*1e6,-20*1e6), orientation=90, width=2*1e6)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(200*1e6,600*1e6))

    def create_elementals(self, elems):

        elems += self.test_q1_90()
        elems += self.test_q2_90()
        elems += self.test_q3_90()
        elems += self.test_q4_90()

        return elems


class Test_Manhattan_Horizontal(spira.Cell):
    """  """

    def create_elementals(self, elems):


        return elems


class Test_Manhattan_Vertical(spira.Cell):
    """  """

    def create_elementals(self, elems):


        return elems


class TestManhattan(spira.Cell):

    # def test_q1_180(self):
    #     p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2*1e6)
    #     p2 = spira.Term(name='P2', midpoint=(40*1e6,20*1e6), orientation=180, width=2*1e6)
    #     rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
    #     return spira.SRef(rm, midpoint=(0,0*1e6))

    # def test_q2_180(self):
    #     p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2*1e6)
    #     p2 = spira.Term(name='P2', midpoint=(-40*1e6,20*1e6), orientation=180, width=2*1e6)
    #     rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
    #     return spira.SRef(rm, midpoint=(0*1e6,200*1e6))

    # def test_q3_180(self):
    #     p1 = spira.Term(name='P1', midpoint=(0,0), orientation=180, width=2*1e6)
    #     p2 = spira.Term(name='P2', midpoint=(-40*1e6,-20*1e6), orientation=0, width=2*1e6)
    #     rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
    #     return spira.SRef(rm, midpoint=(0*1e6,400*1e6))

    # def test_q4_180(self):
    #     p1 = spira.Term(name='P1', midpoint=(0,0), orientation=180, width=2*1e6)
    #     p2 = spira.Term(name='P2', midpoint=(40*1e6,-20*1e6), orientation=0, width=2*1e6)
    #     rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
    #     return spira.SRef(rm, midpoint=(0*1e6,600*1e6))

    # ------------------------------------------------------------------------------------

    # def test_q1_90(self):
    #     p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2*1e6)
    #     p2 = spira.Term(name='P2', midpoint=(40*1e6,20*1e6), orientation=90, width=2*1e6)
    #     rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
    #     return spira.SRef(rm, midpoint=(200*1e6,0*1e6))

    # def test_q2_90(self):
    #     p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2*1e6)
    #     p2 = spira.Term(name='P2', midpoint=(-40*1e6,20*1e6), orientation=-90, width=2*1e6)
    #     rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
    #     return spira.SRef(rm, midpoint=(200*1e6,200*1e6))

    # def test_q3_90(self):
    #     p1 = spira.Term(name='P1', midpoint=(0,0), orientation=180, width=2*1e6)
    #     p2 = spira.Term(name='P2', midpoint=(-40*1e6,-20*1e6), orientation=-90, width=2*1e6)
    #     rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
    #     return spira.SRef(rm, midpoint=(200*1e6,400*1e6))

    # def test_q4_90(self):
    #     p1 = spira.Term(name='P1', midpoint=(0,0), orientation=180, width=2*1e6)
    #     p2 = spira.Term(name='P2', midpoint=(40*1e6,-20*1e6), orientation=90, width=2*1e6)
    #     rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
    #     return spira.SRef(rm, midpoint=(200*1e6,600*1e6))

    # ------------------------------- Horizontal -----------------------------------

    # FIXME!
    def test_q1_180_90(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=-90, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(40*1e6,20*1e6), orientation=90, width=2*1e6)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(0,400*1e6))

    # ------------------------------- Horizontal -----------------------------------

    def test_p1p2_180_horizontal(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(40*1e6,0), orientation=0, width=2*1e6)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(400*1e6,0*1e6))

    def test_p2p1_180_horizontal(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(-40*1e6,0), orientation=0, width=2*1e6)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(400*1e6,200*1e6))

    def test_p1p2_180_bot(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=180, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(40*1e6,0), orientation=180, width=2*1e6)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(400*1e6,400*1e6))

    def test_p2p1_180_bot(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=180, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(-40*1e6,0), orientation=180, width=2*1e6)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(400*1e6,600*1e6))

    # ------------------------------- Vertical -----------------------------------

    def test_p1p2_180_vertical(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=90, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(0,-40*1e6), orientation=90, width=2*1e6)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(600*1e6,0))

    def test_p2p1_180_vertical(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=90, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(0,40*1e6), orientation=90, width=2*1e6)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(600*1e6,200*1e6))

    def test_p1p2_180_vertical_bot(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=-90, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(0,-40*1e6), orientation=-90, width=2*1e6)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(600*1e6,400*1e6))

    def test_p2p1_180_vertical_bot(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=-90, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(0,40*1e6), orientation=-90, width=2*1e6)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(600*1e6,600*1e6))

    # ------------------------------- 180 same Qs ------------------------------

    def test_q1_parallel(self):
        # p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2)
        # p2 = spira.Term(name='P2', midpoint=(50,50), orientation=0, width=2)
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=180, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(50*1e6,50*1e6), orientation=180, width=2*1e6)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(800*1e6, 0))

    def test_q2_parallel(self):
        # p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2)
        # p2 = spira.Term(name='P2', midpoint=(-50,50), orientation=0, width=2)
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=180, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(-50*1e6,50*1e6), orientation=180, width=2*1e6)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(800*1e6, 200*1e6))

    def test_q3_parallel(self):
        # p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2)
        # p2 = spira.Term(name='P2', midpoint=(-50,-50), orientation=0, width=2)
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=180, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(-50*1e6,-50*1e6), orientation=180, width=2*1e6)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(800*1e6, 400*1e6))

    def test_q4_parallel(self):
        # p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2)
        # p2 = spira.Term(name='P2', midpoint=(50,-50), orientation=0, width=2)
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=180, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(50*1e6,-50*1e6), orientation=180, width=2*1e6)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(800*1e6, 450*1e6))

    def create_elementals(self, elems):

        # elems += spira.SRef(Test_Manhattan_90())
        # elems += spira.SRef(Test_Manhattan_180())


        # elems += self.test_q1_180()
        # elems += self.test_q2_180()
        # elems += self.test_q3_180()
        # elems += self.test_q4_180()

        # elems += self.test_q1_90()
        # elems += self.test_q2_90()
        # elems += self.test_q3_90()
        # elems += self.test_q4_90()

        # elems += self.test_q1_parallel()
        # elems += self.test_q2_parallel()
        # elems += self.test_q3_parallel()
        # elems += self.test_q4_parallel()

        # elems += self.test_q1_180_90()

        elems += self.test_p1p2_180_horizontal()
        elems += self.test_p2p1_180_horizontal()
        # elems += self.test_p1p2_180_bot()
        # elems += self.test_p2p1_180_bot()

        # elems += self.test_p1p2_180_vertical()
        # elems += self.test_p2p1_180_vertical()
        # # elems += self.test_p1p2_180_vertical_bot()
        # # elems += self.test_p2p1_180_vertical_bot()

        return elems


if __name__ == '__main__':
    test_cell = TestManhattan()
    test_cell.output()

