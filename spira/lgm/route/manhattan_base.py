import spira
import numpy as np
from spira import param, shapes
from spira.lgm.route.manhattan import __Manhattan__
from spira.lgm.route.manhattan90 import RouteManhattan90
from spira.lgm.route.manhattan180 import RouteManhattan180


class RouteManhattan(__Manhattan__):

    cell = param.CellField()

    metals = param.DataField(fdef_name='create_flatten_metals')
    merged_layers = param.DataField(fdef_name='create_merged_layers')

    def create_flatten_metals(self):
        flat_elems = self.cell.flat_copy()
        # metal_elems = flat_elems.get_polygons(layer=self.player.layer)
        return flat_elems

    def create_merged_layers(self):
        points = []
        elems = spira.ElementList()
        for p in self.metals:
            assert isinstance(p, spira.Polygons)
            for pp in p.polygons:
                points.append(pp)
        if points:
            shape = shapes.Shape(points=points)
            shape.apply_merge
            for pts in shape.points:
                elems += spira.Polygons(shape=[pts], gdslayer=self.gdslayer)
        return elems

    def create_elementals(self, elems):

        # p1 = [self.port1.midpoint[0], self.port1.midpoint[1]]
        # p2 = [self.port2.midpoint[0], self.port2.midpoint[1]]

        # if p2[1] == p1[1] or p2[0] == p1[0]:
        #     raise ValueError('Error - ports must be at different x AND y values.')
        
        angle_diff = self.port1.orientation - self.port2.orientation
        angle = np.round(np.abs(np.mod(angle_diff, 360)), 3)
        if (angle == 180) or (angle == 0):
            R1 = RouteManhattan180(
                port1=self.port1, 
                port2=self.port2, 
                radius=self.radius, 
                length=self.length,
                gdslayer=self.gdslayer
            )
        else:
            R1 = RouteManhattan90(
                port1=self.port1, 
                port2=self.port2, 
                radius=self.radius, 
                length=self.length,
                gdslayer=self.gdslayer
            )

        for p in R1.ports:
            self.ports += p

        self.cell = R1

        # # for e in R1.elementals:
        # # for e in R1.flat_copy():
        # for e in R1.flatten():
        #     elems += e

        for e in self.merged_layers:
            elems += e

        return elems


class TestManhattan(spira.Cell):

    def test_q1_90(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(40*1e6,20*1e6), orientation=90, width=2*1e6)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(50*1e6,50*1e6))

    def test_q1_180(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(40*1e6,20*1e6), orientation=180, width=2*1e6)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(0,50*1e6))

    # FIXME!
    def test_q1_180_90(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=-90, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(40*1e6,20*1e6), orientation=90, width=2*1e6)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(0,50*1e6))

    def test_q2_90(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(-40*1e6,20*1e6), orientation=-90, width=2*1e6)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(-50*1e6,50*1e6))

    def test_q2_180(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(-40*1e6,20*1e6), orientation=180, width=2*1e6)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(-100*1e6,50*1e6))

    def test_q3_90(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=180, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(-40*1e6,-20*1e6), orientation=-90, width=2*1e6)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(-50*1e6,-50*1e6))

    def test_q3_180(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=180, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(-40*1e6,-20*1e6), orientation=0, width=2*1e6)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(-100*1e6,-50*1e6))

    def test_q4_90(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=180, width=2)
        p2 = spira.Term(name='P2', midpoint=(40,-20), orientation=90, width=2)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8)
        return spira.SRef(rm, midpoint=(50,-50))

    def test_q4_180(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=180, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(40*1e6,-20*1e6), orientation=0, width=2*1e6)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(100*1e6,-50*1e6))

    # ------------------------------- Vertical -----------------------------------

    def test_p1p2_180_horizontal(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(40*1e6,0), orientation=0, width=2*1e6)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(150*1e6,0))

    def test_p2p1_180_horizontal(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(-40*1e6,0), orientation=0, width=2*1e6)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(150*1e6,0))

    def test_p1p2_180_bot(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=180, width=2)
        p2 = spira.Term(name='P2', midpoint=(40,0), orientation=180, width=2)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8)
        return spira.SRef(rm, midpoint=(150,0))

    def test_p2p1_180_bot(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=180, width=2)
        p2 = spira.Term(name='P2', midpoint=(-40,0), orientation=180, width=2)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8)
        return spira.SRef(rm, midpoint=(150,0))

    def test_p1p2_180_vertical(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=90, width=2)
        p2 = spira.Term(name='P2', midpoint=(0,-40), orientation=90, width=2)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8)
        return spira.SRef(rm, midpoint=(150,0))

    def test_p2p1_180_vertical(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=90, width=2)
        p2 = spira.Term(name='P2', midpoint=(0,40), orientation=90, width=2)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8)
        return spira.SRef(rm, midpoint=(150,0))

    def test_p1p2_180_vertical_bot(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=-90, width=2)
        p2 = spira.Term(name='P2', midpoint=(0,-40), orientation=-90, width=2)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8)
        return spira.SRef(rm, midpoint=(150,0))

    def test_p2p1_180_vertical_bot(self):
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=-90, width=2)
        p2 = spira.Term(name='P2', midpoint=(0,40), orientation=-90, width=2)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8)
        return spira.SRef(rm, midpoint=(150,0))

    # ------------------------------- 180 same Qs ------------------------------

    def test_q1_parallel(self):
        # p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2)
        # p2 = spira.Term(name='P2', midpoint=(50,50), orientation=0, width=2)
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=180, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(50*1e6,50*1e6), orientation=180, width=2*1e6)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(0,0))

    def test_q2_parallel(self):
        # p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2)
        # p2 = spira.Term(name='P2', midpoint=(-50,50), orientation=0, width=2)
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=180, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(-50*1e6,50*1e6), orientation=180, width=2*1e6)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(150*1e6,0))

    def test_q3_parallel(self):
        # p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2)
        # p2 = spira.Term(name='P2', midpoint=(-50,-50), orientation=0, width=2)
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=180, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(-50*1e6,-50*1e6), orientation=180, width=2*1e6)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(150*1e6,150*1e6))

    def test_q4_parallel(self):
        # p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2)
        # p2 = spira.Term(name='P2', midpoint=(50,-50), orientation=0, width=2)
        p1 = spira.Term(name='P1', midpoint=(0,0), orientation=180, width=2*1e6)
        p2 = spira.Term(name='P2', midpoint=(50*1e6,-50*1e6), orientation=180, width=2*1e6)
        rm = RouteManhattan(port1=p1, port2=p2, radius=8*1e6)
        return spira.SRef(rm, midpoint=(-150*1e6,0))

    def create_elementals(self, elems):

        # elems += self.test_q1_90()
        # elems += self.test_q1_180()
        # elems += self.test_q1_180_90()

        # elems += self.test_q2_90()
        elems += self.test_q2_180()

        # elems += self.test_q3_90()
        # elems += self.test_q3_180()

        # elems += self.test_q4_90()
        # elems += self.test_q4_180()

        # elems += self.test_p1p2_180_horizontal()
        # elems += self.test_p2p1_180_horizontal()
        # elems += self.test_p1p2_180_bot()
        # elems += self.test_p2p1_180_bot()

        # elems += self.test_p1p2_180_vertical()
        # elems += self.test_p2p1_180_vertical()
        # elems += self.test_p1p2_180_vertical_bot()
        # elems += self.test_p2p1_180_vertical_bot()

        # elems += self.test_q1_parallel()
        # elems += self.test_q2_parallel()
        # elems += self.test_q3_parallel()
        # elems += self.test_q4_parallel()

        return elems


if __name__ == '__main__':
    test_cell = TestManhattan()
    test_cell.output()

