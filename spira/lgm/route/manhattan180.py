import spira
import numpy as np
from spira import param, shapes
from spira import pc# from spira.lgm.route.arc_bend import ArcRoute, Arc
from spira.lgm.route.route_shaper import RouteSimple
from spira.lgm.route.route_shaper import RouteGeneral
from spira.utils import scale_coord_up as scu
from spira.lgm.route.manhattan import __Manhattan__


class RouteBase180(__Manhattan__):

    def create_quadrant_one(self):

        self.b1.connect(port=self.b1.ports['P2'], destination=self.term_ports['T1'])
        h = (self.p2[1]-self.p1[1])/2 - self.radius
        self.b1.move(midpoint=self.b1.ports['P2'], destination=[0, h])

        # self.b2.connect(port=self.b1.ports['P2'], destination=self.b2.ports['P1'])
        self.b2.connect(port=self.b2.ports['P1'], destination=self.b1.ports['P1'])
        h = (self.p2[1]-self.p1[1])/2 + self.radius
        # self.b2.move(midpoint=self.b2.ports['P1'], destination=[self.term_ports['T2'].midpoint[0], h])
        self.b2.move(midpoint=self.b2.ports['P2'], destination=[self.term_ports['T2'].midpoint[0], h])

        r1 = self.route_straight(self.b1.ports['P2'], self.term_ports['T1'])
        r2 = self.route_straight(self.b2.ports['P2'], self.term_ports['T2'])
        r3 = self.route_straight(self.b2.ports['P1'], self.b1.ports['P1'])

        D = spira.Cell(name='Q1')
        D += [self.b1, self.b2, r1, r2, r3]

        D += self.term_ports['T1']
        D += self.term_ports['T2']

        D.rotate(angle=self.port1.orientation, center=self.p1)
        D.move(midpoint=self.term_ports['T1'], destination=self.port1)

        return spira.SRef(D)

    def create_quadrant_two(self):

        self.b1.connect(port=self.b1.ports['P1'], destination=self.term_ports['T1'])
        h = (self.p2[1]-self.p1[1])/2 - self.radius
        self.b1.move(midpoint=self.b1.ports['P1'], destination=[0, h])

        # self.b2.connect(port=self.b2.ports['P1'], destination=self.b1.ports['P2'])
        self.b2.connect(port=self.b2.ports['P2'], destination=self.b1.ports['P2'])
        h = (self.p2[1]-self.p1[1])/2 + self.radius
        self.b2.move(midpoint=self.b2.ports['P1'], destination=[self.term_ports['T2'].midpoint[0], h])

        r1 = self.route_straight(self.b2.ports['P1'], self.term_ports['T2'])
        r2 = self.route_straight(self.b1.ports['P1'], self.term_ports['T1'])
        r3 = self.route_straight(self.b2.ports['P2'], self.b1.ports['P2'])

        D = spira.Cell(name='Q2')
        D += [self.b1, self.b2, r1, r2, r3]

        D += self.term_ports['T1']
        D += self.term_ports['T2']

        D.rotate(angle=self.port1.orientation, center=self.p1)
        D.move(midpoint=self.term_ports['T1'], destination=self.port1)

        return spira.SRef(D)

    def create_quadrant_three(self):

        self.b1.connect(port=self.b1.ports['P2'], destination=self.term_ports['T1'])
        # h = self.p2[1] + (self.p1[1]-self.p2[1])/2 + self.radius
        h = (self.p1[1]-self.p2[1])/2 + self.radius
        self.b1.move(midpoint=self.b1.ports['P2'], destination=[0, h])

        self.b2.connect(port=self.b2.ports['P2'], destination=self.b1.ports['P1'])
        # h = self.p2[1] + (self.p1[1]-self.p2[1])/2 - self.radius
        h = (self.p1[1]-self.p2[1])/2 - self.radius
        self.b2.move(midpoint=self.b2.ports['P1'], destination=[self.term_ports['T2'].midpoint[0], h])

        r1 = self.route_straight(self.b2.ports['P1'], self.term_ports['T2'])
        r2 = self.route_straight(self.b1.ports['P2'], self.term_ports['T1'])
        r3 = self.route_straight(self.b2.ports['P2'], self.b1.ports['P1'])

        D = spira.Cell(name='Q3')
        D += [self.b1, self.b2, r1, r2, r3]

        D += self.term_ports['T1']
        D += self.term_ports['T2']

        D.rotate(angle=self.port1.orientation, center=self.p1)
        D.move(midpoint=self.term_ports['T1'], destination=self.port1)

        return spira.SRef(D)

    def create_quadrant_four(self):

        self.b1.connect(port=self.b1.ports['P1'], destination=self.term_ports['T1'])
        # h = self.p2[1] + (self.p1[1]-self.p2[1])/2 + self.radius
        h = (self.p1[1]-self.p2[1])/2 + self.radius
        self.b1.move(midpoint=self.b1.ports['P1'], destination=[0, h])

        self.b2.connect(port=self.b2.ports['P1'], destination=self.b1.ports['P2'])
        # h = self.p2[1] + (self.p1[1]-self.p2[1])/2 - self.radius
        h = (self.p1[1]-self.p2[1])/2 - self.radius
        self.b2.move(midpoint=self.b2.ports['P2'], destination=[self.term_ports['T2'].midpoint[0], h])

        r1 = self.route_straight(self.b1.ports['P1'], self.term_ports['T1'])
        r2 = self.route_straight(self.b2.ports['P2'], self.term_ports['T2'])
        r3 = self.route_straight(self.b2.ports['P1'], self.b1.ports['P2'])

        D = spira.Cell(name='Q4')
        D += [self.b1, self.b2, r1, r2, r3]

        D += self.term_ports['T1']
        D += self.term_ports['T2']

        D.rotate(angle=self.port1.orientation, center=self.p1)
        D.move(midpoint=self.term_ports['T1'], destination=self.port1)

        return spira.SRef(D)


class RouteParallel(__Manhattan__):

    parallel = param.DataField(fdef_name='create_parallel_route')
    quadrant_one_parallel = param.DataField(fdef_name='create_quadrant_one_parallel')
    q1 = param.DataField(fdef_name='create_q1_180')
    q2 = param.DataField(fdef_name='create_q2_180')
    q3 = param.DataField(fdef_name='create_q3_180')
    q4 = param.DataField(fdef_name='create_q4_180')

    def create_parallel_route(self):
        print('ebfwjekfwefjkj')

        p1, p2 = self.p1, self.p2
        b1, b2 = self.b2, self.b1

        dx = max(p1[0], p2[0])
        dy = max(p1[1], p2[1])

        if p2[0] > p1[0]:
            b1, b2 = self.b1, self.b2
        h = p2[1] + self.length
        d1 = [0, h]
        d2 = [self.term_ports['T2'].midpoint[0], h]

        b1.connect(port=b1.ports['P2'], destination=self.term_ports['T1'])
        b1.move(midpoint=b1.ports['P2'], destination=d1)

        b2.connect(port=b2.ports['P2'], destination=b1.ports['P1'])
        b2.move(midpoint=b2.ports['P1'], destination=d2)

        r1 = self.route_straight(b1.ports['P2'], self.term_ports['T1'])
        r2 = self.route_straight(b2.ports['P1'], self.term_ports['T2'])
        r3 = self.route_straight(b1.ports['P1'], b2.ports['P2'])

        D = spira.Cell(name='Parallel')
        D += [self.b1, self.b2, r1, r2, r3]

        t1 = self.term_ports['T1']
        t2 = self.term_ports['T2']

        t1.rotate(angle=self.port1.orientation)
        t2.rotate(angle=self.port1.orientation)

        D.rotate(angle=self.port1.orientation, center=self.p1)
        D.move(midpoint=self.term_ports['T1'], destination=self.port1)

        return spira.SRef(D)

    def create_quadrant_one_parallel(self):

        p1 = [self.port1.midpoint[0], self.port1.midpoint[1]]
        p2 = [self.port2.midpoint[0], self.port2.midpoint[1]]

        b1, b2 = self.b2, self.b1
        d1, d2 = [0,0], [0,0]

        if self.port1.orientation == 0:
            dy = max(p1[1], p2[1])
            if p2[0] > p1[0]:
                b1, b2 = self.b1, self.b2
            h = dy + self.length
            d1 = [0, h]
            d2 = [self.term_ports['T2'].midpoint[0], h] 
        elif self.port1.orientation == 90:
            dx = max(p1[0], p2[0])
            if p2[1] > p1[1]:
                b1, b2 = self.b1, self.b2
            h = dx - self.length
            d1 = [h, 0]
            d2 = [h, self.term_ports['T2'].midpoint[1]]
        elif self.port1.orientation == -90:
            dx = min(p1[0], p2[0])
            if p1[1] > p2[1]:
                b1, b2 = self.b1, self.b2
            h = dx + self.length
            d1 = [h, 0]
            d2 = [h, self.term_ports['T2'].midpoint[1]]
        elif self.port1.orientation == 180:
            dy = min(p1[1], p2[1])
            if p1[0] > p2[0]:
                b1, b2 = self.b1, self.b2
            elif p2[0] > p1[0]:
                b1, b2 = self.b2, self.b1
            h = dy - self.length
            d1 = [0, h]
            d2 = [self.term_ports['T2'].midpoint[0], h] 

        b1.connect(port=b1.ports['P2'], destination=self.term_ports['T1'])
        b1.move(midpoint=b1.ports['P2'], destination=d1)

        b2.connect(port=b2.ports['P1'], destination=b1.ports['P1'])
        b2.move(midpoint=b2.ports['P2'], destination=d2)

        r1 = self.route_straight(b1.ports['P2'], self.term_ports['T1'])
        r2 = self.route_straight(b2.ports['P2'], self.term_ports['T2'])
        r3 = self.route_straight(b1.ports['P1'], b2.ports['P1'])

        return [self.b1, self.b2, r1, r2, r3]

    def create_q1_180(self):

        b1 = self.b1
        b2 = self.b2

        b1.connect(port=b1.ports['P2'], destination=self.term_ports['T1'])
        h = self.p2[1] + self.radius + self.length
        b1.move(midpoint=b1.ports['P2'], destination=[0, h])

        b2.connect(port=b2.ports['P1'], destination=b1.ports['P1'])
        b2.move(midpoint=b2.ports['P2'], destination=[self.term_ports['T2'].midpoint[0], h])

        r1 = self.route_straight(b1.ports['P2'], self.term_ports['T1'])
        r2 = self.route_straight(b2.ports['P2'], self.term_ports['T2'])
        r3 = self.route_straight(b1.ports['P1'], b2.ports['P1'])

        D = spira.Cell(name='SameQ1')
        D += [self.b1, self.b2, r1, r2, r3]

        D += self.term_ports['T1']
        D += self.term_ports['T2']

        D.rotate(angle=self.port1.orientation, center=self.p1)
        D.move(midpoint=self.term_ports['T1'], destination=self.port1)

        return spira.SRef(D)

    def create_q2_180(self):

        b1 = self.b1
        b2 = self.b2

        b1.connect(port=b1.ports['P1'], destination=self.term_ports['T2'])
        h = self.p2[1] + self.radius + self.length
        b1.move(midpoint=b1.ports['P1'], destination=[0, h])

        b2.connect(port=b2.ports['P2'], destination=b1.ports['P2'])
        b2.move(midpoint=b2.ports['P1'], destination=[self.term_ports['T2'].midpoint[0], h])

        r1 = self.route_straight(b1.ports['P1'], self.term_ports['T1'])
        r2 = self.route_straight(b2.ports['P1'], self.term_ports['T2'])
        r3 = self.route_straight(b1.ports['P2'], b2.ports['P2'])

        D = spira.Cell(name='SameQ2')
        D += [self.b1, self.b2, r1, r2, r3]

        D += self.term_ports['T1']
        D += self.term_ports['T2']

        D.rotate(angle=self.port1.orientation, center=self.p1)
        D.move(midpoint=self.term_ports['T1'], destination=self.port1)

        return spira.SRef(D)

    def create_q3_180(self):

        b1 = self.b1
        b2 = self.b2

        b1.connect(port=b1.ports['P1'], destination=self.term_ports['T2'])
        h = self.p1[1] + self.radius + self.length
        b1.move(midpoint=b1.ports['P1'], destination=[0, h])

        b2.connect(port=b2.ports['P2'], destination=b1.ports['P2'])
        b2.move(midpoint=b2.ports['P1'], destination=[self.term_ports['T2'].midpoint[0], h])

        r1 = self.route_straight(b1.ports['P1'], self.term_ports['T1'])
        r2 = self.route_straight(b2.ports['P1'], self.term_ports['T2'])
        r3 = self.route_straight(b1.ports['P2'], b2.ports['P2'])

        D = spira.Cell(name='SameQ3')
        D += [self.b1, self.b2, r1, r2, r3]

        D += self.term_ports['T1']
        D += self.term_ports['T2']

        D.rotate(angle=self.port1.orientation, center=self.p1)
        D.move(midpoint=self.term_ports['T1'], destination=self.port1)

        return spira.SRef(D)

    def create_q4_180(self):

        b1 = self.b1
        b2 = self.b2

        b2.connect(port=b2.ports['P1'], destination=self.term_ports['T1'])
        h = self.p1[1] + self.radius + self.length
        b2.move(midpoint=b2.ports['P1'], destination=[0, h])

        b1.connect(port=b1.ports['P2'], destination=b2.ports['P2'])
        b1.move(midpoint=b1.ports['P1'], destination=[self.term_ports['T2'].midpoint[0], h])

        r1 = self.route_straight(b2.ports['P1'], self.term_ports['T1'])
        r2 = self.route_straight(b1.ports['P1'], self.term_ports['T2'])
        r3 = self.route_straight(b1.ports['P2'], b2.ports['P2'])

        D = spira.Cell(name='SameQ4')
        D += [self.b1, self.b2, r1, r2, r3]

        D += self.term_ports['T1']
        D += self.term_ports['T2']

        D.rotate(angle=self.port1.orientation, center=self.p1)
        D.move(midpoint=self.term_ports['T1'], destination=self.port1)

        return spira.SRef(D)


class Route180(RouteBase180, RouteParallel):
    """ Route ports that has a 180 degree difference. """

    def create_elementals(self, elems):

        p1, p2 = self.p1, self.p2

        if self.port1.orientation == self.port2.orientation:
            if (p1[1] == p2[1]) or (p1[0] == p2[0]):
                R = self.parallel
            if (p2[1] > p1[1]) and (p2[0] > p1[0]):
                print('Q1 Equal Angles')
                R = self.q1
            if (p2[1] > p1[1]) and (p2[0] < p1[0]):
                print('Q2 Equal Angles')
                R = self.q2
            if (p2[1] < p1[1]) and (p2[0] < p1[0]):
                print('Q3 Equal Angles')
                R = self.q3
            if (p2[1] < p1[1]) and (p2[0] > p1[0]):
                print('Q4 Equal Angles')
                R = self.q4
        elif np.round(np.abs(np.mod(self.port1.orientation - self.port2.orientation,360)),3) != 180:
            raise ValueError('[DEVICE] route() error: Ports do not face each other (orientations must be 180 apart)')    
        else:
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

        # elems += R
                
        points = []
        for e in R.ref.flatten():
            if isinstance(e, spira.Polygons):
                for p in e.points:
                    points.append(p)
        route_shape = shapes.Shape(points=points)
        route_shape.apply_merge
        poly = pc.Polygon(points=route_shape.points, ps_layer=self.ps_layer, enable_edges=False) 
        elems += poly

        return elems

    def create_ports(self, ports):

        angle_diff = self.port1.orientation - self.port2.orientation
        if self.port1.orientation == self.port2.orientation:
            ports += spira.Term(name='T1',
                width=self.port1.width,
                orientation=0
            )
            ports += spira.Term(name='T2',
                midpoint=list(np.subtract(self.p2, self.p1)),
                width=self.port2.width,
                orientation=0
            )
        elif np.round(np.abs(np.mod(angle_diff, 360)), 3) != 180:
            raise ValueError("2. [DEVICE] route() error: Ports do not " +
                "face each other (orientations must be 180 apart)")
        else:
            ports += spira.Term(name='T1',
                width=self.port1.width,
                orientation=0
            )
            ports += spira.Term(name='T2',
                midpoint=list(np.subtract(self.p2, self.p1)),
                width=self.port2.width,
                orientation=180
            )

        return ports

