import numpy as np
import spira.all as spira
from spira.yevon.visualization import color

from spira.technologies.mit import devices as dev
from spira.technologies.mit.rdd.database import RDD


class ProcessPolygons(spira.PCell):
# class ProcessPolygons(spira.Cell):

    def create_elementals(self, elems):

        points = [[0, 0], [2*1e6, 2*1e6], 
                  [2*1e6, 6*1e6], [-6*1e6, 6*1e6],
                  [-6*1e6, -6*1e6], [-4*1e6, -4*1e6], 
                  [-4*1e6, 4*1e6], [0, 4*1e6]]
        p1 = spira.Polygon(shape=points, ps_layer=RDD.PLAYER.M6)
        elems += p1

        p2 = spira.Rectangle(p1=(-10*1e6, 2*1e6), p2=(-5*1e6, 4*1e6), ps_layer=RDD.PLAYER.M6)
        elems += p2

        return elems


if __name__ == '__main__':

    D = ProcessPolygons()
    B = D.bbox_info()
    D += spira.Polygon(shape=B.bounding_box)
    print(D.elementals)
    D.output()