import numpy as np
import spira.all as spira
from spira.yevon import process as pc
from spira.yevon.geometry import shapes
from spira.yevon.visualization import color
from spira.yevon.operations.elementals import *

from spira.technologies.mit import devices as dev
from spira.technologies.mit.rdd.database import RDD


class NativePolygons(spira.Cell):

    def create_elementals(self, elems):

        points = [[(0, 0), (2*1e6, 2*1e6), (2*1e6, 6*1e6), (-6*1e6, 6*1e6),
                   (-6*1e6, -6*1e6), (-4*1e6, -4*1e6), (-4*1e6, 4*1e6), (0, 4*1e6)]]
        p1 = spira.Polygon(shape=points, gds_layer=spira.Layer(number=60))

        elems += p1

        return elems


class ProcessPolygons(spira.PCell):

    def create_elementals(self, elems):

        points = [[(0, 0), (2*1e6, 2*1e6), (2*1e6, 6*1e6), (-6*1e6, 6*1e6),
                   (-6*1e6, -6*1e6), (-4*1e6, -4*1e6), (-4*1e6, 4*1e6), (0, 4*1e6)]]
        p1 = pc.Polygon(points=points, ps_layer=RDD.PLAYER.M6)

        p2 = pc.Rectangle(p1=(-10*1e6, 2*1e6), p2=(-5*1e6, 4*1e6), ps_layer=RDD.PLAYER.M6)

        elems += p1
        elems += p2

        return elems


if __name__ == '__main__':

    # D = NativePolygons()
    # c_elems = convert_polygons_to_processlayers(D.elementals)
    # C1 = spira.Cell(name='ConvertedPolygons', elementals=c_elems)
    # C1.output()
    # D.output()

    D = ProcessPolygons()
    print(D.routes)
    # # m_elems = merge_metal_processlayers(D.elementals)
    # connect_processlayer_edges(D.elementals)
    # C1 = spira.Cell(name='ProcessPolygons', elementals=D.elementals)
    # # C1 = spira.Cell(name='ProcessPolygons', elementals=m_elems)
    # C1.output()
    D.output()


