import spira.all as spira
from spira.core import param
from spira.yevon.geometry.route.routing import Route
from spira.yevon.geometry.route.route_shaper import *


class Test_Manhattan_180(spira.Cell):
    """ Routes with ports facing eachother in a 180 degree. """

    def test_q1_180(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(40*1e6,20*1e6), orientation=180, width=2*1e6)
        rm = Route(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(5*1e6,5*1e6))

    def test_q2_180(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(-40*1e6,20*1e6), orientation=180, width=2*1e6)
        rm = Route(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(-5*1e6,5*1e6))

    def test_q3_180(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=180, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(-40*1e6,-20*1e6), orientation=0, width=2*1e6)
        rm = Route(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(-5*1e6,-5*1e6))

    def test_q4_180(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=180, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(40*1e6,-20*1e6), orientation=0, width=2*1e6)
        rm = Route(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(5*1e6,-5*1e6))

    def create_elementals(self, elems):

        elems += self.test_q1_180()
        elems += self.test_q2_180()
        # elems += self.test_q3_180()
        elems += self.test_q4_180()

        return elems


class Test_Manhattan_90(spira.Cell):
    """ Routes with ports facing eachother in a 90 degree. """

    def test_q1_90(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(40*1e6,20*1e6), orientation=90, width=2*1e6)
        rm = Route(port1=p1, port2=p2, radius=8*1e6)
        # return spira.SRef(rm, midpoint=(200*1e6,0*1e6))
        return spira.SRef(rm, midpoint=(5*1e6,5*1e6))

    def test_q2_90(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(-40*1e6,20*1e6), orientation=-90, width=2*1e6)
        rm = Route(port1=p1, port2=p2, radius=8*1e6)
        # return spira.SRef(rm, midpoint=(200*1e6,200*1e6))
        return spira.SRef(rm, midpoint=(-5*1e6,5*1e6))

    def test_q3_90(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=180, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(-40*1e6,-20*1e6), orientation=-90, width=2*1e6)
        rm = Route(port1=p1, port2=p2, radius=8*1e6)
        # return spira.SRef(rm, midpoint=(200*1e6,400*1e6))
        return spira.SRef(rm, midpoint=(-5*1e6,-5*1e6))

    def test_q4_90(self):
        """ P1 has an orientation of 180. """
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=180, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(40*1e6,-20*1e6), orientation=90, width=2*1e6)
        rm = Route(port1=p1, port2=p2, radius=8*1e6)
        # return spira.SRef(rm, midpoint=(200*1e6,800*1e6))
        return spira.SRef(rm, midpoint=(5*1e6,-5*1e6))

    # ------------------------------------------------------------------------------------

    def test_q1_90_2(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=-90, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(40*1e6,20*1e6), orientation=180, width=2*1e6)
        rm = Route(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(115*1e6,5*1e6))

    def test_q2_90_2(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=90, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(-40*1e6,20*1e6), orientation=180, width=2*1e6)
        rm = Route(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(105*1e6,5*1e6))

    def test_q3_90_2(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=90, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(-40*1e6,-20*1e6), orientation=0, width=2*1e6)
        rm = Route(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(105*1e6,-5*1e6))

    def test_q4_90_2(self):
        """ P1 has an orientation of 180. """
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=-90, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(40*1e6,-20*1e6), orientation=0, width=2*1e6)
        rm = Route(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(115*1e6,-5*1e6))

    def create_elementals(self, elems):

        # Angle negative
        elems += self.test_q1_90()
        elems += self.test_q2_90()
        elems += self.test_q3_90()
        elems += self.test_q4_90()

        # Angle positive
        elems += self.test_q1_90_2()
        elems += self.test_q2_90_2()
        elems += self.test_q3_90_2()
        elems += self.test_q4_90_2()

        return elems


class Test_Manhattan_Horizontal(spira.Cell):
    """  """

    def test_p1p2_180_horizontal(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(40*1e6,0), orientation=0, width=2*1e6)
        rm = Route(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(5*1e6,5*1e6))

    def test_p2p1_180_horizontal(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(-40*1e6,0), orientation=0, width=2*1e6)
        rm = Route(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(-5*1e6,5*1e6))

    def test_p1p2_180_bot(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=180, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(40*1e6,0), orientation=180, width=2*1e6)
        rm = Route(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(5*1e6,-5*1e6))

    def test_p2p1_180_bot(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=180, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(-40*1e6,0), orientation=180, width=2*1e6)
        rm = Route(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(-5*1e6,-5*1e6))

    def create_elementals(self, elems):

        # elems += self.test_p1p2_180_horizontal()
        elems += self.test_p2p1_180_horizontal()
        # elems += self.test_p1p2_180_bot()
        # elems += self.test_p2p1_180_bot()

        return elems


class Test_Manhattan_Vertical(spira.Cell):
    """  """

    def test_p1p2_180_vertical(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=90, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(0,-40*1e6), orientation=90, width=2*1e6)
        rm = Route(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(-5*1e6,-5*1e6))

    def test_p2p1_180_vertical(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=90, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(0,40*1e6), orientation=90, width=2*1e6)
        rm = Route(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(-5*1e6,5*1e6))

    def test_p1p2_180_vertical_bot(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=-90, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(0,-40*1e6), orientation=-90, width=2*1e6)
        rm = Route(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(5*1e6,-5*1e6))

    def test_p2p1_180_vertical_bot(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=-90, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(0,40*1e6), orientation=-90, width=2*1e6)
        rm = Route(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(5*1e6,5*1e6))

    def create_elementals(self, elems):

        elems += self.test_p1p2_180_vertical()
        elems += self.test_p2p1_180_vertical()
        elems += self.test_p1p2_180_vertical_bot()
        elems += self.test_p2p1_180_vertical_bot()

        return elems


class Test_Manhattan_180_SimilarAngles(spira.Cell):
    """  """

    # FIXME!
    # angle = param.IntegerField(default=0)
    angle = param.IntegerField(default=180)

    def test_q1_parallel(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=self.angle, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(50*1e6,50*1e6), orientation=180, width=2*1e6)
        rm = Route(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(5*1e6, -5*1e6))

    def test_q2_parallel(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=self.angle, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(-50*1e6,50*1e6), orientation=180, width=2*1e6)
        rm = Route(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(-5*1e6, -5*1e6))

    def test_q3_parallel(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=self.angle, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(-50*1e6,-50*1e6), orientation=180, width=2*1e6)
        rm = Route(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(-5*1e6, 150*1e6))

    def test_q4_parallel(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=self.angle, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(50*1e6,-50*1e6), orientation=180, width=2*1e6)
        rm = Route(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(5*1e6, 150*1e6))

    def create_elementals(self, elems):

        elems += self.test_q1_parallel()
        elems += self.test_q2_parallel()
        elems += self.test_q3_parallel()
        elems += self.test_q4_parallel()

        return elems


class TestManhattan(spira.Cell):

    # FIXME!
    def test_q1_180_90(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=-90, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(40*1e6,20*1e6), orientation=90, width=2*1e6)
        rm = Route(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(0,400*1e6))

    def create_elementals(self, elems):

        # elems += spira.SRef(Test_Manhattan_90(), midpoint=(0,0))
        elems += spira.SRef(Test_Manhattan_180(), midpoint=(250*1e6, 0))
        # elems += spira.SRef(Test_Manhattan_Horizontal(), midpoint=(0,-250*1e6))
        # elems += spira.SRef(Test_Manhattan_Vertical(), midpoint=(250*1e6, -250*1e6))
        # elems += spira.SRef(Test_Manhattan_180_SimilarAngles(), midpoint=(500*1e6, -250*1e6))

        return elems


class TestGeneral(spira.Cell):

    D = spira.Cell(name='RouteSimplerTests')

    def create_elementals(self, elems):
        points = [(0,0), (0,-5*1e6), (10*1e6,-5*1e6), (10*1e6,0), (15*1e6,0)]

        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=-90, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(30*1e6,0), orientation=90, width=2*1e6)

        r1 = RouteSimple(port1=p1, port2=p2, path_type='straight', width_type='straight')
        r2 = RoutePointShape(path=points, width=1*1e6)
        r3 = RouteArcShape(start_angle=0, theta=90, angle_resolution=5)
        r4 = RouteSquareShape()

        elems += spira.SRef(structure=RouteGeneral(route_shape=r1), midpoint=(0*1e6, 0*1e6))
        elems += spira.SRef(structure=RouteGeneral(route_shape=r2), midpoint=(10*1e6, 0*1e6))
        elems += spira.SRef(structure=RouteGeneral(route_shape=r3), midpoint=(20*1e6, 0*1e6))
        elems += spira.SRef(structure=RouteGeneral(route_shape=r4), midpoint=(30*1e6, 0*1e6))

        return elems


if __name__ == '__main__':

    cell = spira.Cell(name='Route Tests')

    cell += spira.SRef(structure=TestManhattan())
    # cell += spira.SRef(structure=TestGeneral(), midpoint=(0, -100*1e6))

    cell.output(cell='Route Tests_1')

