import numpy as np
import spira.all as spira
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


class ProcessPolygons(spira.PCell):

    def create_elementals(self, elems):
        points = [[0, 0], [2, 2], [2, 6], [-6, 6], [-6, -6], [-4, -4], [-4, 4], [0, 4]]
        elems += spira.Polygon(shape=points, layer=RDD.PLAYER.M2.METAL)
        elems += spira.Rectangle(p1=(-10, 2), p2=(-5, 4), layer=RDD.PLAYER.M2.METAL)
        return elems


if __name__ == '__main__':

    D = ProcessPolygons()
    # B = D.bbox_info.bounding_box()
    # D += spira.Polygon(shape=B, layer=spira.Layer(3))
    D.gdsii_output()