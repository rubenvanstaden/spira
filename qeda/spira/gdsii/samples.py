import spira
import gdspy
import numpy as np
from core import param
from spira import shapes, pc
from spira import utils


RDD = spira.get_rule_deck()


class TestPolygons(spira.Cell):

    def create_elementals(self, elems):

        points = [[(0, 0), (2*1e6, 2*1e6), (2*1e6, 6*1e6), (-6*1e6, 6*1e6), (-6*1e6, -6*1e6), (-4*1e6, -4*1e6), (-4*1e6, 4*1e6), (0, 4*1e6)]]
        pp = pc.Polygon(points=points, ps_layer=RDD.PLAYER.COU)

        plys = spira.ElementList()
        pl = utils.cut(ply=pp, position=[-3*1e6, 3*1e6], axis=0)
        
        # p = pl[1]
        # ply = pc.Polygon(points=p.points, ps_layer=RDD.PLAYER.COU)
        # plys += ply
        # elems += p

        for p in pl:
            ply = pc.Polygon(points=p.points, ps_layer=RDD.PLAYER.COU)
            plys += ply
            elems += p

        x1 = int(np.floor(len(plys)/2))
        x2 = int(np.floor(len(plys)))

        for i in range(0, x1):
            p1 = plys[i]
            for j in range(x1, x2):
                p2 = plys[j]
                for e1 in p1.edge_ports:
                    for e2 in p2.edge_ports:
                        if e1.edge & e2.edge:
                            elems += e1.edge

        return elems


if __name__ == '__main__':

    tp = TestPolygons()

    tp.output()

