import spira
import numpy as np
from spira import param
from spira.lgm.route.arc_bend import ArcRoute, Arc
from spira.lgm.route.basic import RouteShape
from spira.lgm.route.basic import RouteBasic


class __Manhattan__(spira.Cell):

    port1 = param.DataField()
    port2 = param.DataField()

    length = param.FloatField(default=20)
    gdslayer = param.LayerField(number=13)
    radius = param.IntegerField(default=1)
    bend_type = param.StringField(default='circular')

    b1 = param.DataField(fdef_name='create_arc_bend_1')
    b2 = param.DataField(fdef_name='create_arc_bend_2')
    b3 = param.DataField(fdef_name='create_arc_bend_3')
    b4 = param.DataField(fdef_name='create_arc_bend_4')

    p1 = param.DataField(fdef_name='create_port1_position')
    p2 = param.DataField(fdef_name='create_port2_position')

    quadrant_one = param.DataField(fdef_name='create_quadrant_one')
    quadrant_two = param.DataField(fdef_name='create_quadrant_two')
    quadrant_three = param.DataField(fdef_name='create_quadrant_three')
    quadrant_four = param.DataField(fdef_name='create_quadrant_four')

    def _generate_route(self, p1, p2):
        route = RouteShape(
            port1=p1, port2=p2,
            path_type='straight',
            width_type='straight'
        )
        R1 = RouteBasic(route=route, connect_layer=self.gdslayer)
        r1 = spira.SRef(R1)
        r1.rotate(angle=p2.orientation-180, center=R1.port1.midpoint)
        r1.move(midpoint=(0,0), destination=p1.midpoint)
        return r1

    def create_port1_position(self):
        p1 = [self.port1.midpoint[0], self.port1.midpoint[1]]
        if self.port1.orientation == 90:
            p1 = [self.port1.midpoint[1], -self.port1.midpoint[0]]
        if self.port1.orientation == 180:
            p1 = [-self.port1.midpoint[0], -self.port1.midpoint[1]]
        if self.port1.orientation == 270:
            p1 = [-self.port1.midpoint[1], self.port1.midpoint[0]]
        return p1

    def create_port2_position(self):
        p2 = [self.port2.midpoint[0], self.port2.midpoint[1]]
        if self.port1.orientation == 90:
            p2 = [self.port2.midpoint[1], -self.port2.midpoint[0]]
        if self.port1.orientation == 180:
            p2 = [-self.port2.midpoint[0], -self.port2.midpoint[1]]
        if self.port1.orientation == 270:
            p2 = [-self.port2.midpoint[1], self.port2.midpoint[0]]
        return p2

    def create_arc_bend_1(self):
        if self.bend_type == 'circular':
            B1 = Arc(shape=ArcRoute(radius=self.radius,
                width=self.port1.width,
                # gdslayer=self.gdslayer,
                gdslayer=spira.Layer(number=18),
                start_angle=0, theta=90)
            )
            return spira.SRef(B1)

    def create_arc_bend_2(self):
        if self.bend_type == 'circular':
            B2 = Arc(shape=ArcRoute(radius=self.radius,
                width=self.port1.width,
                # gdslayer=self.gdslayer,
                gdslayer=spira.Layer(number=18),
                start_angle=0, theta=-90)
            )
            return spira.SRef(B2)

    def create_arc_bend_3(self):
        if self.bend_type == 'circular':
            B1 = Arc(shape=ArcRoute(radius=self.radius,
                width=self.port1.width,
                # gdslayer=self.gdslayer,
                gdslayer=spira.Layer(number=18),
                start_angle=0, theta=90)
            )
            return spira.SRef(B1)

    def create_arc_bend_4(self):
        if self.bend_type == 'circular':
            B2 = Arc(shape=ArcRoute(radius=self.radius,
                width=self.port1.width,
                # gdslayer=self.gdslayer,
                gdslayer=spira.Layer(number=18),
                start_angle=-90, theta=-90)
            )
            return spira.SRef(B2)













