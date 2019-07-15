import spira.all as spira
import numpy as np
from spira.yevon.geometry import shapes
from spira.yevon.geometry.route.route_shaper import RouteSimple, RouteGeneral
from spira.yevon.geometry.route.manhattan import __Manhattan__

from copy import deepcopy


class Route90Base(__Manhattan__):
    """ Route ports that has a 180 degree difference. """

    def create_quadrant_one(self):

        p1, p2 = self.p1, self.p2

        h = (p2[1]-p1[1]) - self.radius
        self.b1.distance_alignment(port=self.b1.ports['P2'], destination=self.ports['T1'], distance=h)

        r1 = self.route_straight(self.b1.ports['P2'], self.ports['T1'])
        r2 = self.route_straight(self.b1.ports['P1'], self.ports['T2'])

        D = spira.Cell(name='Route_Q1_90')
        D += self.b1
        D += r1
        D += r2

        # D += self.ports['T1']
        # D += self.ports['T2']

        # D._rotate(rotation=self.port1.orientation, center=self.p1)
        # D.move(midpoint=self.ports['T1'], destination=self.port1)

        return spira.SRef(D)

    def create_quadrant_two(self):

        p1, p2 = self.p1, self.p2

        h = (p2[1]-p1[1]) - self.radius
        self.b1.distance_alignment(port=self.b1.ports['P1'], destination=self.ports['T1'], distance=h)

        r1 = self.route_straight(self.b1.ports['P1'], self.ports['T1'])
        r2 = self.route_straight(self.b1.ports['P2'], self.ports['T2'])

        D = spira.Cell(name='Route_Q2_90')

        D += self.b1
        D += r1
        D += r2

        # D += self.ports['T1']
        # D += self.ports['T2']

        # D._rotate(rotation=self.port1.orientation, center=self.p1)
        # D.move(midpoint=self.ports['T1'], destination=self.port1)

        return spira.SRef(D)

    def create_quadrant_three(self):

        p1, p2 = self.p1, self.p2
        
        # t1 = deepcopy(self.ports['T1'])
        # t2 = deepcopy(self.ports['T2'])
        
        # self.b2.connect(port=self.b2.ports['P1'], destination=t1)
        # h = p2[1] + self.radius
        # self.b2.move(midpoint=self.b2.ports['P1'], destination=[0, h])

        # # r1 = self.route_straight(self.b2.ports['P1'], t1)
        # # r2 = self.route_straight(self.b2.ports['P2'], t2)

        # # self.b2.connect(port=self.b2.ports['P1'], destination=self.ports['T1'])
        # # h = p2[1] + self.radius
        # # self.b2.move(midpoint=self.b2.ports['P1'], destination=[0, h])

        # # r1 = self.route_straight(self.b2.ports['P1'], self.ports['T1'])
        # # r2 = self.route_straight(self.b2.ports['P2'], self.ports['T2'])

        D = spira.Cell(name='Route_Q4_90')

        D += self.b1

        # D += self.ports['T1']
        # D += self.ports['T2']

        # D._rotate(rotation=self.port1.orientation, center=self.p1)
        # D.move(midpoint=self.ports['T1'], destination=self.port1)

        return spira.SRef(D)

    def create_quadrant_four(self):

        p1, p2 = self.p1, self.p2

        self.b2.connect(port=self.b2.ports['P2'], destination=self.ports['T1'])
        h = p2[1] + self.radius
        self.b2.move(midpoint=self.b2.ports['P2'], destination=[0, h])

        r1 = self.route_straight(self.b2.ports['P2'], self.ports['T1'])
        r2 = self.route_straight(self.b2.ports['P1'], self.ports['T2'])

        D = spira.Cell(name='Route_Q4_90')
        D += [self.b2, r1, r2]

        D += self.ports['T1']
        D += self.ports['T2']

        # D.rotate(angle=self.port1.orientation, center=self.p1)
        D._rotate(rotation=self.port1.orientation, center=self.p1)
        D.move(midpoint=self.ports['T1'], destination=self.port1)

        return spira.SRef(D)


class Route90(Route90Base):

    def create_elements(self, elems):

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

        # points = []
        # for e in R.reference.flatten():
        #     if isinstance(e, spira.Polygon):
        #         for p in e.points:
        #             points.append(p)
        # route_shape = shapes.Shape(points=points)
        # route_shape.apply_merge
        # poly = pc.Polygon(points=route_shape.points, layer=self.layer, enable_edges=False)
        # elems += poly

        elems += R

        return elems
        
    def create_ports(self, ports):

        p1, p2 = self.p1, self.p2

        a1 = self.port1.orientation
        a2 = self.port2.orientation

        angle_diff = self.port2.orientation - self.port1.orientation
        angle = np.round(np.abs(np.mod(angle_diff, 360)), 3)
        a = np.mod(self.port1.orientation, 360)

        p1_angle = np.mod(self.port1.orientation, 360)

        if angle == 90:
            ports += spira.Port(name='T1',
                width=self.port1.width,
                orientation=90
            )
            ports += spira.Port(name='T2',
                midpoint=list(np.subtract(p2, p1)),
                width=self.port2.width,
                orientation=180
            )
        else:
            ports += spira.Port(name='T1',
                width=self.port1.width,
                orientation=90
            )
            ports += spira.Port(name='T2',
                midpoint=list(np.subtract(p2, p1)),
                width=self.port2.width,
                orientation=0
            )

        return ports


