import numpy as np
import spira.all as spira
from spira.yevon.rdd import get_rule_deck


RDD = get_rule_deck()


class ProcessPolygons(spira.PCell):
# class ProcessPolygons(spira.Cell):

    def create_elementals(self, elems):

        points = [[0, 0], [2*1e6, 2*1e6],
                  [2*1e6, 6*1e6], [-6*1e6, 6*1e6],
                  [-6*1e6, -6*1e6], [-4*1e6, -4*1e6],
                  [-4*1e6, 4*1e6], [0, 4*1e6]]
        p1 = spira.Polygon(shape=points, ps_layer=RDD.PLAYER.M1)
        elems += p1

        p2 = spira.Rectangle(p1=(-10*1e6, 2*1e6), p2=(-5*1e6, 4*1e6), ps_layer=RDD.PLAYER.M1)
        elems += p2

        return elems


if __name__ == '__main__':

    D = ProcessPolygons()
    B = D.bbox_info.bounding_box
    D += spira.Polygon(shape=B)
    print(D.elementals)
    D.output()