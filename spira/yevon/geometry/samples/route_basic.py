import spira.all as spira
from spira.yevon.geometry.route.routing import Route
from spira.yevon.geometry.route.route_shaper import *


from spira.technologies.mit import devices as dev
from spira.technologies.mit.rdd.database import RDD


class TestGeneral(spira.Cell):

    D = spira.Cell(name='RouteSimplerTests')

    def create_elementals(self, elems):
        points = [(0,0), (0,-5*1e6), (10*1e6,-5*1e6), (10*1e6,0), (15*1e6,0)]

        # p1 = spira.Terminal(name='P1', midpoint=(0,0), orientation=-90, width=2*1e6)
        # p2 = spira.Terminal(name='P2', midpoint=(15*1e6,0), orientation=90, width=2*1e6)

        # p1 = spira.Terminal(name='P1', midpoint=(0,0), orientation=-90, width=2*1e6)
        # p2 = spira.Terminal(name='P2', midpoint=(15*1e6, 15*1e6), orientation=90, width=2*1e6)

        p1 = spira.Terminal(name='P1', midpoint=(0,0), orientation=90, width=2*1e6)
        p2 = spira.Terminal(name='P2', midpoint=(15*1e6,0), orientation=-90, width=2*1e6)

        r1 = RouteSimple(port1=p1, port2=p2, path_type='straight', width_type='straight')
        r2 = RoutePointShape(path=points, width=1*1e6)
        r4 = RouteSquareShape()

        r3 = RouteArcShape(start_angle=0, theta=90, angle_resolution=5)
        R_arc = RouteArcShape(start_angle=0, theta=-90, angle_resolution=5)

        S = spira.SRef(
            reference=RouteGeneral(route_shape=r1, connect_layer=RDD.PLAYER.M0),
            midpoint=(0*1e6, 0*1e6)
        )
        T = spira.Rotation(rotation=p1.orientation, center=p1.midpoint)
        S.transform(T)
        # # S.move(midpoint=(0,0), destination=p1.midpoint)
        elems += S

        # elems += spira.SRef(
        #     # reference=RouteGeneral(route_shape=r2, gds_layer=spira.Layer(number=2)),
        #     reference=RouteGeneral(route_shape=r2, connect_layer=RDD.PLAYER.M1),
        #     midpoint=(25*1e6, 0*1e6)
        # )
        # elems += spira.SRef(
        #     # reference=RouteGeneral(route_shape=r4, gds_layer=spira.Layer(number=4)), 
        #     reference=RouteGeneral(route_shape=r4, connect_layer=RDD.PLAYER.M3),
        #     midpoint=(75*1e6, 0*1e6)
        # )

        # --- ArcShape ---
        elems += spira.SRef(
            # reference=RouteGeneral(route_shape=r3, gds_layer=spira.Layer(number=3)),
            reference=RouteGeneral(route_shape=r3, connect_layer=RDD.PLAYER.M2),
            midpoint=(50*1e6, 0*1e6)
        )
        elems += spira.SRef(
            reference=RouteGeneral(route_shape=R_arc, connect_layer=RDD.PLAYER.M2),
            midpoint=(50*1e6, 10*1e6)
        )

        return elems


class TestSimple(spira.Cell):

    D = spira.Cell(name='RouteSimplerTests')

    def create_elementals(self, elems):

        p1 = spira.Terminal(name='P1', midpoint=(0,0), orientation=-45, width=2*1e6)
        p2 = spira.Terminal(name='P2', midpoint=(15*1e6,0), orientation=135, width=2*1e6)

        # p1 = spira.Terminal(name='P1', midpoint=(0,0), orientation=-90, width=2*1e6)
        # p2 = spira.Terminal(name='P2', midpoint=(15*1e6, 15*1e6), orientation=90, width=2*1e6)

        # p1 = spira.Terminal(name='P1', midpoint=(0,0), orientation=0, width=2*1e6)
        # p2 = spira.Terminal(name='P2', midpoint=(15*1e6,0), orientation=180, width=2*1e6)

        r1 = RouteSimple(port1=p1, port2=p2, path_type='straight', width_type='straight')

        R = RouteGeneral(route_shape=r1, connect_layer=RDD.PLAYER.M0)
        S = spira.SRef(R)
        # S.connect(port=p1, destination=self.ports['P1'])
        S.connect(port=S.ports['P1'], destination=p1)
        # T = spira.Rotation(rotation=p1.orientation, center=p1.midpoint)
        # S.transform(T)
        # # S.move(midpoint=(0,0), destination=p1.midpoint)
        elems += S

        return elems

    def create_ports(self, ports):

        ports += spira.Terminal(name='P1', midpoint=(20*1e6, 20*1e6), orientation=30)

        return ports


if __name__ == '__main__':

    # cell = spira.Cell(name='Route Tests')
    # cell += spira.SRef(reference=TestGeneral(), midpoint=(0, -100*1e6))
    # cell.output()
    # # cell.output(cell='Route Tests_1')

    D = TestSimple()
    D.output()

