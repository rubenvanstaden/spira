import spira
import numpy as np
from spira import param
from spira.lgm.route.arc_bend import ArcRoute, Arc
from spira.lgm.route.basic import RouteShape
from spira.lgm.route.basic import RouteBasic
from spira.gdsii.utils import scale_coord_up as scu


class RouteManhattan(spira.Cell):
    port1 = param.DataField()
    port2 = param.DataField()

    dx = param.DataField(fdef_name='create_x_distance')
    dy = param.DataField(fdef_name='create_y_distance')

    bend_type = param.StringField(default='circular')
    layer = param.IntegerField(default=12)
    radius = param.IntegerField(default=2)

    def create_x_distance(self):
        p1=[self.port1.midpoint[0], self.port1.midpoint[1]]
        p2=[self.port2.midpoint[0], self.port2.midpoint[1]]
        return abs(p2[0]-p1[0])/2

    def create_y_distance(self):
        p1=[self.port1.midpoint[0], self.port1.midpoint[1]]
        p2=[self.port2.midpoint[0], self.port2.midpoint[1]]
        return abs(p2[1]-p1[1])/2

    # def validate_parameters(self):
    #     if (self.radius > self.dx) or (self.radius > self.dy):
    #         return False
    #     return True

    def create_elementals(self, elems):

        # Total = spira.Cell(name='Device')
        # width = self.port1.width

        if self.port1.orientation==0:
            p2=[self.port2.midpoint[0], self.port2.midpoint[1]]
            p1=[self.port1.midpoint[0], self.port1.midpoint[1]]
        if self.port1.orientation==90:
            p2=[self.port2.midpoint[1], -self.port2.midpoint[0]]
            p1=[self.port1.midpoint[1], -self.port1.midpoint[0]]
        if self.port1.orientation==180:
            p2=[-self.port2.midpoint[0], -self.port2.midpoint[1]]
            p1=[-self.port1.midpoint[0], -self.port1.midpoint[1]]
        if self.port1.orientation==270:
            p2=[-self.port2.midpoint[1], self.port2.midpoint[0]]
            p1=[-self.port1.midpoint[1], self.port1.midpoint[0]]

        # if p2[1] == p1[1] or p2[0] == p1[0]:
        #     raise ValueError('Error - ports must be at different x AND y values.')

        if (np.round(np.abs(np.mod(self.port1.orientation - self.port2.orientation,360)),3) == 180) \
            or (np.round(np.abs(np.mod(self.port1.orientation - self.port2.orientation,360)),3) == 0):
            R1 = RouteManhattan180(
                port1=self.port1, 
                port2=self.port2,
                bend_type=self.bend_type,
                layer=self.layer,
                radius=self.radius
            )
            elems += spira.SRef(R1)
        return elems

    def create_ports(self, ports):
        ports += self.port1
        ports += self.port2
        return ports


class RouteManhattan180(spira.Cell):
    """ Route ports that has a 180 degree difference. """

    port1 = param.DataField()
    port2 = param.DataField()
    quadrant_one = param.DataField(fdef_name='create_quadrant_one')

    length = param.FloatField(default=2)
    layer = param.IntegerField(default=13)
    radius = param.IntegerField(default=1)
    bend_type = param.StringField(default='circular')

    def _generate_route(self, p1, p2):
        route = RouteShape(
            port1=p1, port2=p2,
            path_type='straight',
            width_type='straight',
            layer=self.layer
        )
        R1 = RouteBasic(route=route)
        r1 = spira.SRef(R1)
        r1.rotate(angle=p2.orientation-180, center=R1.port1.midpoint)
        r1.move(midpoint=(0,0), destination=p1.midpoint)
        return r1

    def create_quadrant_one(self):
        if self.bend_type == 'circular':
            ll = spira.Layer(number=self.layer)
            B1 = Arc(shape=ArcRoute(radius=self.radius, width=self.port1.width, gdslayer=ll, start_angle=90, theta=-90))
            B2 = Arc(shape=ArcRoute(radius=self.radius, width=self.port1.width, gdslayer=ll, start_angle=0, theta=90))
            radiusEff = self.radius

        b1 = spira.SRef(B1)
        b2 = spira.SRef(B2)

        b2.connect(port=b2.ports['P1'], destination=self.term_ports['T1'])
        h = self.length - radiusEff
        b2.move(midpoint=b2.ports['P1'].midpoint, destination=[0, h])

        b1.connect(port=b1.ports['P2'], destination=b2.ports['P2'])
        h = self.length - radiusEff
        b1.move(midpoint=b1.ports['P1'].midpoint, destination=[self.term_ports['T2'].midpoint[0], h])

        r1 = self._generate_route(b1.ports['P1'], self.term_ports['T2'])
        r2 = self._generate_route(b2.ports['P1'], self.term_ports['T1'])
        r3 = self._generate_route(b2.ports['P2'], b1.ports['P2'])

        return [b1, b2, r1, r2, r3]

    def create_elementals(self, elems):

        width = self.port1.width

        p1=[self.port1.midpoint[0], self.port1.midpoint[1]]
        p2=[self.port2.midpoint[0], self.port2.midpoint[1]]

        if self.port1.orientation == self.port2.orientation:
            if (p2[1] > p1[1]) & (p2[0] > p1[0]):
                if self.bend_type == 'circular':
                    ll = spira.Layer(number=self.layer)
                    B1 = Arc(shape=ArcRoute(radius=self.radius, width=width, gdslayer=ll, start_angle=90, theta=90))
                    B2 = Arc(shape=ArcRoute(radius=self.radius, width=width, gdslayer=ll, start_angle=0, theta=90))
                    radiusEff = self.radius

                b1 = spira.SRef(B1)
                b2 = spira.SRef(B2)

                Total += b1
                Total += b2

                b1.connect(port=b1.ports['P2'], destination=Total.term_ports['T1'])
                h = (p2[1]-p1[1])/2 - radiusEff
                b1.move(midpoint=b1.ports['P2'].midpoint, destination=[0, h])

                b2.connect(port=b2.ports['P1'], destination=b1.ports['P1'])
                h = (p2[0]-p1[0])
                b2.move(midpoint=b2.ports['P2'].midpoint, destination=[h, b2.ports['P2'].midpoint[1]])

                route = RouteShape(port1=b1.ports['P2'],
                                   port2=Total.term_ports['T1'],
                                   path_type='straight',
                                   width_type='straight',
                                   layer=self.layer)
                R1 = RouteBasic(route=route)
                r1 = spira.SRef(R1)
                r1.rotate(angle=route.port2.orientation,
                          center=R1.port1.midpoint)
                r1.move(midpoint=(0,0), destination=Total.term_ports['T1'].midpoint)
                Total += r1

                route = RouteShape(port1=b2.ports['P2'],
                                   port2=Total.term_ports['T2'],
                                   path_type='straight',
                                   width_type='straight',
                                   layer=self.layer)
                R2 = RouteBasic(route=route)
                r2 = spira.SRef(R2)
                r2.rotate(angle=route.port2.orientation,
                          center=R2.port1.midpoint)
                r2.move(midpoint=(0,0), destination=Total.term_ports['T2'].midpoint)
                Total += r2

                route = RouteShape(port1=b2.ports['P1'],
                                port2=b1.ports['P1'],
                                path_type='straight',
                                width_type='straight',
                                layer=self.layer)
                R3 = RouteBasic(route=route)
                r3 = spira.SRef(R3)
                # r3.rotate(angle=route.port1.orientation,
                #             center=R3.port1.midpoint)
                r3.move(midpoint=(0,0), destination=b1.ports['P1'].midpoint)
                Total += r3


                # Total.ports += r1.ports['P1']
                # Total.ports += b2.ports['P2']

                # Total.ports += r1.ports['P1']._copy()
                # Total.ports += b2.ports['P2']._copy()

                # R1=route_basic(port1=Total.ports['t1'],port2=b1.ports[1],layer=layer)
                # r1=Total.add_ref(R1)

                # R2=route_basic(port1=b1.ports[2],port2=b2.ports[1],layer=layer)
                # r2=Total.add_ref(R2)

                # Total.add_port(name=1,port=r1.ports[1])
                # Total.add_port(name=2,port=b2.ports[2])

            if (p2[1] > p1[1]) & (p2[0] < p1[0]):

                if self.bend_type == 'circular':
                    ll = spira.Layer(number=self.layer)
                    B1 = Arc(shape=ArcRoute(radius=self.radius, width=width, gdslayer=ll, start_angle=90, theta=90))
                    B2 = Arc(shape=ArcRoute(radius=self.radius, width=width, gdslayer=ll, start_angle=0, theta=90))
                    radiusEff = self.radius

                b1 = spira.SRef(B1)
                b2 = spira.SRef(B2)

                Total += b1
                Total += b2

                b2.connect(port=b2.ports['P1'], destination=Total.term_ports['T1'])
                h = (p2[1]-p1[1])/2 - radiusEff
                b2.move(midpoint=b2.ports['P1'].midpoint, destination=[0, h])

                b1.connect(port=b1.ports['P2'], destination=b2.ports['P2'])
                h = (p2[0]-p1[0])
                b1.move(midpoint=b1.ports['P1'].midpoint, destination=[h, b1.ports['P1'].midpoint[1]])

                route = RouteShape(port1=b1.ports['P1'],
                                   port2=Total.term_ports['T2'],
                                   path_type='straight',
                                   width_type='straight',
                                   layer=self.layer)
                R1 = RouteBasic(route=route)
                r1 = spira.SRef(R1)
                r1.rotate(angle=route.port2.orientation,
                          center=R1.port1.midpoint)
                r1.move(midpoint=(0,0), destination=Total.term_ports['T2'].midpoint)
                Total += r1

                route = RouteShape(port1=b2.ports['P1'],
                                   port2=Total.term_ports['T1'],
                                   path_type='straight',
                                   width_type='straight',
                                   layer=self.layer)
                R2 = RouteBasic(route=route)
                r2 = spira.SRef(R2)
                r2.rotate(angle=route.port2.orientation,
                          center=R2.port1.midpoint)
                r2.move(midpoint=(0,0), destination=Total.term_ports['T1'].midpoint)
                Total += r2

                route = RouteShape(port1=b2.ports['P2'],
                                port2=b1.ports['P2'],
                                path_type='straight',
                                width_type='straight',
                                layer=self.layer)
                R3 = RouteBasic(route=route)
                r3 = spira.SRef(R3)
                r3.move(midpoint=(0,0), destination=b1.ports['P2'].midpoint)
                Total += r3

            if (p2[1] <= p1[1]) & (p2[0] < p1[0]):
                elems += self.quadrant_one

        return elems

    def create_ports(self, ports):

        p1=[self.port1.midpoint[0], self.port1.midpoint[1]]
        p2=[self.port2.midpoint[0], self.port2.midpoint[1]]

        ports += spira.Term(name='T1', width=self.port1.width, orientation=90)

        if self.port1.orientation != self.port2.orientation:
            ports += spira.Term(name='T2',
                midpoint=list(np.subtract(p2, p1)),
                orientation=-90,
                width=self.port2.width
            )
        else:
            ports += spira.Term(name='T2',
                midpoint=list(np.subtract(p2, p1)),
                #   orientation=-90,
                orientation=90,
                width=self.port2.width
            )
        return ports


if __name__ == '__main__':

    # p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2*1e6)
    # p2 = spira.Term(name='P2', midpoint=(30*1e6,45*1e6), orientation=0, width=1.5*1e6)
    # rm = RouteManhattan(port1=p1, port2=p2, radius=7.5*1e6)

    p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2)

    # 1st Quadrant
    # p2 = spira.Term(name='P2', midpoint=(50,25), orientation=0, width=1.5)
    # 2nd Quadrant
    # p2 = spira.Term(name='P2', midpoint=(-50,25), orientation=0, width=1.5)
    # 3rd Quadrant
    p2 = spira.Term(name='P2', midpoint=(-50,0), orientation=0, width=2)

    rm = RouteManhattan180(port1=p1, port2=p2, radius=1)
    # rm = RouteManhattan(port1=p1, port2=p2, radius=1)

    rm.output()












