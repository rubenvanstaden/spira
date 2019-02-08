import spira
import numpy as np
from spira import param
from spira.lgm.route.basic import RouteShape
from spira.lgm.route.basic import RouteBasic
from spira.lgm.route.arc_bend import ArcRoute, Arc
from spira.gdsii.utils import scale_coord_up as scu
from spira.lgm.route.manhattan import __Manhattan__


class Route90(__Manhattan__):
    """ Route ports that has a 180 degree difference. """

    def create_quadrant_one(self):

        # p1=[self.port1.midpoint[0], self.port1.midpoint[1]]
        # p2=[self.port2.midpoint[0], self.port2.midpoint[1]]

        p1, p2 = self.p1, self.p2

        self.b1.connect(port=self.b1.ports['P2'], destination=self.term_ports['T1'])
        h = (p2[1]-p1[1]) - self.radius
        self.b1.move(midpoint=self.b1.ports['P2'], destination=[0, h])
        # h = 2*(p2[0]-p1[0]) - self.radius
        # h = (p2[1]-p1[1]) - self.radius
        # self.b1.move(midpoint=self.b1.ports['P2'], destination=[h, 0])

        r1 = self._generate_route(self.b1.ports['P2'], self.term_ports['T1'])
        r2 = self._generate_route(self.b1.ports['P1'], self.term_ports['T2'])

        D = spira.Cell(name='Route_Q1_90')
        # D += [self.b1, r1]
        D += [self.b1, r1, r2]

        D += self.term_ports['T1']
        D += self.term_ports['T2']

        D.rotate(angle=self.port1.orientation, center=self.p1)
        D.move(midpoint=self.term_ports['T1'], destination=self.port1)

        return spira.SRef(D)

        # return [self.b1, r1, r2]

    def create_quadrant_two(self):

        # p1=[self.port1.midpoint[0], self.port1.midpoint[1]]
        # p2=[self.port2.midpoint[0], self.port2.midpoint[1]]

        p1, p2 = self.p1, self.p2

        self.b1.connect(port=self.b1.ports['P1'], destination=self.term_ports['T1'])
        h = (p2[1]-p1[1]) - self.radius
        self.b1.move(midpoint=self.b1.ports['P1'].midpoint, destination=[self.term_ports['T1'].midpoint[0], h])

        r1 = self._generate_route(self.b1.ports['P1'], self.term_ports['T1'])
        r2 = self._generate_route(self.b1.ports['P2'], self.term_ports['T2'])

        D = spira.Cell(name='Route_Q2_90')
        # D += [self.b1, r1]
        D += [self.b1, r1, r2]

        D += self.term_ports['T1']
        D += self.term_ports['T2']

        D.rotate(angle=self.port1.orientation, center=self.p1)
        D.move(midpoint=self.term_ports['T1'], destination=self.port1)

        return spira.SRef(D)

        # return [self.b1, r1, r2]

    def create_quadrant_three(self):

        # p1=[self.port1.midpoint[0], self.port1.midpoint[1]]
        # p2=[self.port2.midpoint[0], self.port2.midpoint[1]]

        p1, p2 = self.p1, self.p2

        self.b2.connect(port=self.b2.ports['P1'], destination=self.term_ports['T1'])
        h = p2[1] + self.radius
        self.b2.move(midpoint=self.b2.ports['P1'], destination=[0, h])

        r1 = self._generate_route(self.b2.ports['P1'], self.term_ports['T1'])
        r2 = self._generate_route(self.b2.ports['P2'], self.term_ports['T2'])

        return [self.b2, r1, r2]

    def create_quadrant_four(self):

        # p1=[self.port1.midpoint[0], self.port1.midpoint[1]]
        # p2=[self.port2.midpoint[0], self.port2.midpoint[1]]

        p1, p2 = self.p1, self.p2

        self.b2.connect(port=self.b2.ports['P2'], destination=self.term_ports['T1'])
        h = p2[1] + self.radius
        self.b2.move(midpoint=self.b2.ports['P2'], destination=[0, h])
        # h = self.term_ports['T1'][1]
        # print(h)
        # self.b2.move(midpoint=self.b2.ports['P2'], destination=[0, h])

        r1 = self._generate_route(self.b2.ports['P2'], self.term_ports['T1'])
        r2 = self._generate_route(self.b2.ports['P1'], self.term_ports['T2'])

        D = spira.Cell(name='Route_Q4_90')
        D += [self.b1, r1, r2]

        D += self.term_ports['T1']
        D += self.term_ports['T2']

        D.rotate(angle=self.port1.orientation, center=self.p1)
        D.move(midpoint=self.term_ports['T1'], destination=self.port1)

        return spira.SRef(D)

        # return [self.b2, r2]
        # return [self.b2, r1, r2]


class RouteManhattan90(Route90):

    def create_elementals(self, elems):

        # p1 = [self.port1.midpoint[0], self.port1.midpoint[1]]
        # p2 = [self.port2.midpoint[0], self.port2.midpoint[1]]

        p1, p2 = self.p1, self.p2

        if (p2[1] > p1[1]) and (p2[0] > p1[0]):
            print('Q1')
            elems += self.quadrant_one

        if (p2[1] > p1[1]) and (p2[0] < p1[0]):
            print('Q2')
            elems += self.quadrant_two

        if (p2[1] < p1[1]) and (p2[0] < p1[0]):
            print('Q3')
            elems += self.quadrant_three

        if (p2[1] < p1[1]) and (p2[0] > p1[0]):
            print('Q4')
            elems += self.quadrant_four

        return elems

    def create_ports(self, ports):

        # FIXME!!!!
        # p1 = [self.port1.midpoint[0], self.port1.midpoint[1]]
        # p2 = [self.port2.midpoint[0], self.port2.midpoint[1]]

        p1, p2 = self.p1, self.p2

        # angle = self.port1.orientation
        # if np.round(np.abs(np.mod(angle, 360)), 3) != 180:

        a1 = self.port1.orientation
        a2 = self.port2.orientation
        print(a1, a2)

        # angle_diff = self.port1.orientation - self.port2.orientation
        # angle = np.round(np.abs(np.mod(angle_diff, 360)), 3)

        angle_diff = self.port2.orientation - self.port1.orientation
        angle = np.round(np.abs(np.mod(angle_diff, 360)), 3)

        print(angle)

        # if (a2 == a1-90) or (a2 == a1+270):
        if angle == 90:
            print('A')
            ports += spira.Term(name='T1', 
                width=self.port1.width, 
                orientation=0
                # orientation=self.port1.orientation
            )
            ports += spira.Term(name='T2',
                midpoint=list(np.subtract(p2, p1)),
                width=self.port2.width,
                orientation=90
                # orientation=self.port2.orientation
            )
        else:
            print('B')
            ports += spira.Term(name='T1', 
                width=self.port1.width, 
                orientation=0
                # orientation=self.port1.orientation
            )
            ports += spira.Term(name='T2',
                midpoint=list(np.subtract(p2, p1)),
                width=self.port2.width,
                orientation=-90
                # orientation=self.port2.orientation
            )

        return ports


