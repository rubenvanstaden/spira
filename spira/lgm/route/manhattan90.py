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

        p1=[self.port1.midpoint[0], self.port1.midpoint[1]]
        p2=[self.port2.midpoint[0], self.port2.midpoint[1]]

        self.b1.connect(port=self.b1.ports['P2'], destination=self.term_ports['T1'])
        h = (p2[1]-p1[1]) - self.radius
        self.b1.move(midpoint=self.b1.ports['P2'], destination=[0, h])

        r1 = self._generate_route(self.b1.ports['P2'], self.term_ports['T1'])
        r2 = self._generate_route(self.b1.ports['P1'], self.term_ports['T2'])

        return [self.b1, r1, r2]

    def create_quadrant_two(self):

        p1=[self.port1.midpoint[0], self.port1.midpoint[1]]
        p2=[self.port2.midpoint[0], self.port2.midpoint[1]]

        self.b1.connect(port=self.b1.ports['P1'], destination=self.term_ports['T1'])
        h = (p2[1]-p1[1]) - self.radius
        self.b1.move(midpoint=self.b1.ports['P1'].midpoint, destination=[self.term_ports['T1'].midpoint[0], h])

        r1 = self._generate_route(self.b1.ports['P1'], self.term_ports['T1'])
        r2 = self._generate_route(self.b1.ports['P2'], self.term_ports['T2'])

        return [self.b1, r1, r2]

    def create_quadrant_three(self):

        p1=[self.port1.midpoint[0], self.port1.midpoint[1]]
        p2=[self.port2.midpoint[0], self.port2.midpoint[1]]

        self.b2.connect(port=self.b2.ports['P1'], destination=self.term_ports['T1'])
        h = p2[1] + self.radius
        self.b2.move(midpoint=self.b2.ports['P1'], destination=[0, h])

        r1 = self._generate_route(self.b2.ports['P1'], self.term_ports['T1'])
        r2 = self._generate_route(self.b2.ports['P2'], self.term_ports['T2'])

        return [self.b2, r1, r2]

    def create_quadrant_four(self):

        p1=[self.port1.midpoint[0], self.port1.midpoint[1]]
        p2=[self.port2.midpoint[0], self.port2.midpoint[1]]

        self.b2.connect(port=self.b2.ports['P2'], destination=self.term_ports['T1'])
        h = p2[1] + self.radius
        self.b2.move(midpoint=self.b2.ports['P2'], destination=[0, h])

        r1 = self._generate_route(self.b2.ports['P2'], self.term_ports['T1'])
        r2 = self._generate_route(self.b2.ports['P1'], self.term_ports['T2'])

        return [self.b2, r1, r2]


class RouteManhattan90(Route90):

    def create_elementals(self, elems):

        p1 = [self.port1.midpoint[0], self.port1.midpoint[1]]
        p2 = [self.port2.midpoint[0], self.port2.midpoint[1]]

        if (p2[1] > p1[1]) and (p2[0] > p1[0]):
            elems += self.quadrant_one

        if (p2[1] > p1[1]) and (p2[0] < p1[0]):
            elems += self.quadrant_two

        if (p2[1] < p1[1]) and (p2[0] < p1[0]):
            elems += self.quadrant_three

        if (p2[1] < p1[1]) and (p2[0] > p1[0]):
            elems += self.quadrant_four

        return elems

    def create_ports(self, ports):

        p1 = [self.port1.midpoint[0], self.port1.midpoint[1]]
        p2 = [self.port2.midpoint[0], self.port2.midpoint[1]]

        ports += spira.Term(name='T1', 
            width=self.port1.width, 
            orientation=self.port1.orientation
        )
        ports += spira.Term(name='T2',
            midpoint=list(np.subtract(p2, p1)),
            width=self.port2.width,
            orientation=self.port2.orientation
        )

        return ports


