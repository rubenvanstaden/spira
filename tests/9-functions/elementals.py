import gdspy
import numpy as np
import spira.all as spira
from spira.yevon.utils import geometry as geom
from spira.yevon.geometry import shapes


RDD = spira.get_rule_deck()


class TestPolygons(spira.Cell):

    def create_elementals(self, elems):

        points = [
            (0, 0), (2*1e6, 2*1e6), 
            (2*1e6, 6*1e6), (-6*1e6, 6*1e6), 
            (-6*1e6, -6*1e6), (-4*1e6, -4*1e6), 
            (-4*1e6, 4*1e6), (0, 4*1e6)
        ]
        shape = shapes.Shape(points=points)
        pp = spira.Polygon(shape=shape, ps_layer=RDD.PLAYER.COU)

        plys = spira.ElementList()
        pl = geom.cut(ply=pp, position=[-3*1e6, 3*1e6], axis=0)

        for p in pl:
            s1 = shapes.Shape(points=p.points)
            ply = spira.Polygon(shape=s1, ps_layer=RDD.PLAYER.COU)
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

