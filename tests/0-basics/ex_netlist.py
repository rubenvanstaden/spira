import numpy as np
import spira.all as spira
from spira.yevon.visualization import color

from spira.technologies.mit import devices as dev
from spira.technologies.mit.rdd.database import RDD


# class ProcessPolygons(spira.PCell):
class ProcessPolygons(spira.Cell):

    def create_elementals(self, elems):

        points = [[0, 0], [2*1e6, 2*1e6],
                  [2*1e6, 6*1e6], [-6*1e6, 6*1e6],
                  [-6*1e6, -6*1e6], [-4*1e6, -4*1e6],
                  [-4*1e6, 4*1e6], [0, 4*1e6]]
        p1 = spira.Polygon(alias='M6', shape=points, ps_layer=RDD.PLAYER.M6)
        elems += p1

        # p2 = spira.Rectangle(p1=(-10*1e6, 2*1e6), p2=(-5*1e6, 4*1e6), ps_layer=RDD.PLAYER.M6)
        # elems += p2

        return elems

    def create_ports(self, ports):

        ply = self.elementals['M6']

        ply.ports['M6_e0'].locked = False
        ply.ports['M6_e4'].locked = False

        ports += ply.ports['M6_e0']
        ports += ply.ports['M6_e4']

        return ports

    def create_nets(self, nets):

        elems = self.elementals
        ports = self.ports

        nets += spira.Net(elementals=elems, ports=ports, ps_layer=RDD.PLAYER.M6)

        return nets


if __name__ == '__main__':

    # D = ProcessPolygons()
    # B = D.bbox_info()
    # D += spira.Polygon(shape=B.bounding_box)
    # D.output()

    D = ProcessPolygons()
    # D = ProcessPolygons(disable_edge_ports=True)
    g = D.nets[0].g
    D.plotly_netlist(G=g, graphname='metal', labeltext='id')
    D.output()
