import spira.all as spira
from spira.yevon.geometry.route.routing import Route
from spira.yevon.geometry.route.route_shaper import *


from spira.technologies.mit import devices as dev
from spira.technologies.mit.rdd.database import RDD


class TestGeneral(spira.Cell):

    D = spira.Cell(name='RouteSimplerTests')

    def create_elementals(self, elems):
        points = [(0,0), (0,-5*1e6), (10*1e6,-5*1e6), (10*1e6,0), (15*1e6,0)]

        p1 = spira.Terminal(name='P1', midpoint=(0,0), orientation=-90, width=2*1e6)
        p2 = spira.Terminal(name='P2', midpoint=(15*1e6,0), orientation=90, width=2*1e6)

        r1 = RouteSimple(port1=p1, port2=p2, path_type='straight', width_type='straight')
        r2 = RoutePointShape(path=points, width=1*1e6)
        r3 = RouteArcShape(start_angle=0, theta=90, angle_resolution=5)
        r4 = RouteSquareShape()

        elems += spira.SRef(
            # reference=RouteGeneral(route_shape=r1, gds_layer=spira.Layer(number=1)),
            reference=RouteGeneral(route_shape=r1, connect_layer=RDD.PLAYER.M0), 
            midpoint=(0*1e6, 0*1e6)
        )
        elems += spira.SRef(
            # reference=RouteGeneral(route_shape=r2, gds_layer=spira.Layer(number=2)),
            reference=RouteGeneral(route_shape=r2, connect_layer=RDD.PLAYER.M1),
            midpoint=(25*1e6, 0*1e6)
        )
        elems += spira.SRef(
            # reference=RouteGeneral(route_shape=r3, gds_layer=spira.Layer(number=3)), 
            reference=RouteGeneral(route_shape=r3, connect_layer=RDD.PLAYER.M2),
            midpoint=(50*1e6, 0*1e6)
        )
        elems += spira.SRef(
            # reference=RouteGeneral(route_shape=r4, gds_layer=spira.Layer(number=4)), 
            reference=RouteGeneral(route_shape=r4, connect_layer=RDD.PLAYER.M3),
            midpoint=(75*1e6, 0*1e6)
        )

        return elems


if __name__ == '__main__':

    cell = spira.Cell(name='Route Tests')
    cell += spira.SRef(reference=TestGeneral(), midpoint=(0, -100*1e6))
    cell.output()
    # cell.output(cell='Route Tests_1')

