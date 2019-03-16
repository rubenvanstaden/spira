import spira
import numpy as np
from spira import param, shapes, pc
from spira.lgm.route.route_shaper import RouteSimple, RouteGeneral
from spira.lgm.route.manhattan import __Manhattan__


class Route90(__Manhattan__):
    """ Route ports that has a 180 degree difference. """

    def create_quadrant_one(self):

        p1, p2 = self.p1, self.p2

        self.b1.connect(port=self.b1.ports['P2'], destination=self.term_ports['T1'])
        h = (p2[1]-p1[1]) - self.radius
        self.b1.move(midpoint=self.b1.ports['P2'], destination=[0, h])

        r1 = self.route_straight(self.b1.ports['P2'], self.term_ports['T1'])
        r2 = self.route_straight(self.b1.ports['P1'], self.term_ports['T2'])

        D = spira.Cell(name='Route_Q1_90')
        D += [self.b1, r1, r2]

        D += self.term_ports['T1']
        D += self.term_ports['T2']

        D.rotate(angle=self.port1.orientation, center=self.p1)
        D.move(midpoint=self.term_ports['T1'], destination=self.port1)

        return spira.SRef(D)

    def create_quadrant_two(self):

        p1, p2 = self.p1, self.p2

        self.b1.connect(port=self.b1.ports['P1'], destination=self.term_ports['T1'])
        h = (p2[1]-p1[1]) - self.radius
        self.b1.move(midpoint=self.b1.ports['P1'].midpoint, destination=[self.term_ports['T1'].midpoint[0], h])

        r1 = self.route_straight(self.b1.ports['P1'], self.term_ports['T1'])
        r2 = self.route_straight(self.b1.ports['P2'], self.term_ports['T2'])

        D = spira.Cell(name='Route_Q2_90')
        D += [self.b1, r1, r2]

        D += self.term_ports['T1']
        D += self.term_ports['T2']

        D.rotate(angle=self.port1.orientation, center=self.p1)
        D.move(midpoint=self.term_ports['T1'], destination=self.port1)

        return spira.SRef(D)

    def create_quadrant_three(self):

        p1, p2 = self.p1, self.p2

        self.b2.connect(port=self.b2.ports['P1'], destination=self.term_ports['T1'])
        h = p2[1] + self.radius
        self.b2.move(midpoint=self.b2.ports['P1'], destination=[0, h])

        r1 = self.route_straight(self.b2.ports['P1'], self.term_ports['T1'])
        r2 = self.route_straight(self.b2.ports['P2'], self.term_ports['T2'])

        D = spira.Cell(name='Route_Q4_90')
        D += [self.b1, r1, r2]

        D += self.term_ports['T1']
        D += self.term_ports['T2']

        D.rotate(angle=self.port1.orientation, center=self.p1)
        D.move(midpoint=self.term_ports['T1'], destination=self.port1)

        return spira.SRef(D)

    def create_quadrant_four(self):

        p1, p2 = self.p1, self.p2

        self.b2.connect(port=self.b2.ports['P2'], destination=self.term_ports['T1'])
        h = p2[1] + self.radius
        self.b2.move(midpoint=self.b2.ports['P2'], destination=[0, h])

        r1 = self.route_straight(self.b2.ports['P2'], self.term_ports['T1'])
        r2 = self.route_straight(self.b2.ports['P1'], self.term_ports['T2'])

        D = spira.Cell(name='Route_Q4_90')
        D += [self.b2, r1, r2]

        D += self.term_ports['T1']
        D += self.term_ports['T2']

        D.rotate(angle=self.port1.orientation, center=self.p1)
        D.move(midpoint=self.term_ports['T1'], destination=self.port1)

        return spira.SRef(D)


class Route90(Route90):

    def create_elementals(self, elems):

        p1, p2 = self.p1, self.p2

        if (p2[1] > p1[1]) and (p2[0] > p1[0]):
            print('Q1')
            R = self.quadrant_one

        if (p2[1] > p1[1]) and (p2[0] < p1[0]):
            print('Q2')
            R = self.quadrant_two

        if (p2[1] < p1[1]) and (p2[0] < p1[0]):
            print('Q3')
            R = self.quadrant_three

        if (p2[1] < p1[1]) and (p2[0] > p1[0]):
            print('Q4')
            R = self.quadrant_four

        points = []
        for e in R.ref.flatten():
            if isinstance(e, spira.Polygons):
                for p in e.points:
                    points.append(p)
        route_shape = shapes.Shape(points=points)
        route_shape.apply_merge
        poly = pc.Polygon(points=route_shape.points, ps_layer=self.ps_layer, enable_edges=False)
        elems += poly

        # elems += R

        return elems
        
    # def create_metals(self, elems):

    #     p1, p2 = self.p1, self.p2

    #     if (p2[1] > p1[1]) and (p2[0] > p1[0]):
    #         print('Q1')
    #         elems += self.quadrant_one

    #     if (p2[1] > p1[1]) and (p2[0] < p1[0]):
    #         print('Q2')
    #         elems += self.quadrant_two

    #     if (p2[1] < p1[1]) and (p2[0] < p1[0]):
    #         print('Q3')
    #         elems += self.quadrant_three

    #     if (p2[1] < p1[1]) and (p2[0] > p1[0]):
    #         print('Q4')
    #         elems += self.quadrant_four

    #     return elems

    def create_ports(self, ports):

        p1, p2 = self.p1, self.p2

        a1 = self.port1.orientation
        a2 = self.port2.orientation

        angle_diff = self.port2.orientation - self.port1.orientation
        angle = np.round(np.abs(np.mod(angle_diff, 360)), 3)
        a = np.mod(self.port1.orientation, 360)

        p1_angle = np.mod(self.port1.orientation, 360)

        if angle == 90:
            ports += spira.Term(name='T1',
                width=self.port1.width,
                orientation=0
            )
            ports += spira.Term(name='T2',
                midpoint=list(np.subtract(p2, p1)),
                width=self.port2.width,
                orientation=90
            )
        else:
            ports += spira.Term(name='T1',
                width=self.port1.width,
                orientation=0
            )
            ports += spira.Term(name='T2',
                midpoint=list(np.subtract(p2, p1)),
                width=self.port2.width,
                orientation=-90
            )

        return ports


