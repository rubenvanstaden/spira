import spira
import gdspy
import numpy as np
from spira import param
from spira import shapes
from numpy.linalg import norm
from spira.rdd import get_rule_deck
from numpy import sqrt, pi, cos, sin, log, exp, sinh, mod


RDD = get_rule_deck()


class RouteShape(shapes.Shape):

    port1 = param.DataField()
    port2 = param.DataField()

    num_path_pts = param.IntegerField(default=99)

    path_type = param.StringField(default='sine')
    width_type = param.StringField(default='straight')
    width1 = param.FloatField(default=None)
    width2 = param.FloatField(default=None)

    x_dist = param.FloatField()
    y_dist = param.FloatField()

    def create_points(self, points):

        point_a = np.array(self.port1.midpoint)
        if self.width1 is None:
            self.width1 = self.port1.width
        point_b = np.array(self.port2.midpoint)
        if self.width2 is None:
            self.width2 = self.port2.width
        if round(abs(mod(self.port1.orientation - self.port2.orientation, 360)), 3) != 180:
            raise ValueError('Ports do not face eachother.')
        orientation = self.port1.orientation - 90

        separation = point_b - point_a
        distance = norm(separation)
        rotation = np.arctan2(separation[1], separation[0]) * 180/pi
        angle = rotation - orientation
        forward_distance = distance*cos(angle*pi/180)
        lateral_distance = distance*sin(angle*pi/180)

        xf = forward_distance
        yf = lateral_distance

        self.x_dist = xf
        self.y_dist = yf

        if self.path_type == 'straight':
            curve_fun = lambda t: [xf*t, yf*t]
            curve_deriv_fun = lambda t: [xf + t*0, 0 + t*0]
        if self.path_type == 'sine':
            curve_fun = lambda t: [xf*t, yf*(1-cos(t*pi))/2]
            curve_deriv_fun = lambda t: [xf + t*0, yf*(sin(t*pi)*pi)/2]

        if self.width_type == 'straight':
            width_fun = lambda t: (self.width2 - self.width1)*t + self.width1
        if self.width_type == 'sine':
            width_fun = lambda t: (self.width2 - self.width1)*(1-cos(t*pi))/2 + self.width1

        route_path = gdspy.Path(width=self.width1, initial_point=(0,0))

        route_path.parametric(
            curve_fun, curve_deriv_fun, 
            number_of_evaluations=self.num_path_pts,
            max_points=199, 
            final_width=width_fun, 
            final_distance=None
        )

        points = route_path.polygons

        return points


class RouteBasic(spira.Cell):

    route = param.ShapeField()
    connect_layer = param.LayerField(doc='GDSII layer to which the route connects.')

    port1 = param.DataField(fdef_name='create_port1')
    port2 = param.DataField(fdef_name='create_port2')
    llayer = param.DataField(fdef_name='create_layer')

    def create_layer(self):
        ll = spira.Layer(number=self.connect_layer.number, datatype=RDD.PURPOSE.TERM.datatype)
        return ll

    def create_elementals(self, elems):
        ply = spira.Polygons(shape=self.route, gdslayer=self.connect_layer)
        ply.rotate(angle=-90)
        elems += ply
        return elems

    def create_port1(self):
        term = spira.Term(name='TERM1',
            midpoint=(0,0),
            width=self.route.width1,
            length=0.2,
            orientation=180,
            gdslayer=self.llayer
        )
        term.rotate(angle=-90)
        return term

    def create_port2(self):
        term = spira.Term(name='TERM2',
            midpoint=[self.route.x_dist, self.route.y_dist],
            width=self.route.width2,
            length=0.2,
            orientation=0,
            gdslayer=self.llayer
        )
        term.rotate(angle=-90)
        return term

    def create_ports(self, ports):

        ports += self.port1
        ports += self.port2

        return ports


class Route(spira.Cell):

    port1 = param.DataField()
    port2 = param.DataField()
    player = param.PhysicalLayerField()

    def validate_parameters(self):
        if self.port1.width < self.player.data.WIDTH:
            return False
        if self.port2.width < self.player.data.WIDTH:
            return False
        return True

    def create_elementals(self, elems):

        route = RouteShape(
            port1=self.port1,
            port2=self.port2,
            path_type='straight',
            width_type='straight'
        )

        R1 = RouteBasic(route=route, connect_layer=self.player.layer)
        r1 = spira.SRef(R1)
        r1.rotate(angle=self.port2.orientation-180, center=R1.port1.midpoint)
        r1.move(midpoint=(0,0), destination=self.port1.midpoint)

        elems += r1

        return elems


if __name__ == '__main__':

    # p1 = spira.Term(name='P1', midpoint=(0,0), orientation=90, width=2)
    # p2 = spira.Term(name='P2', midpoint=(0,30), orientation=-90, width=1)

    p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2)
    p2 = spira.Term(name='P2', midpoint=(30,0), orientation=180, width=2)

    route = RouteShape(port1=p1, port2=p2, path_type='straight', width_type='straight')

    # p1 = spira.Term(name='P1', midpoint=(0,0), orientation=-90, width=1)
    # p2 = spira.Term(name='P2', midpoint=(30,30), orientation=90, width=1)

    # route = RouteShape(port1=p1, port2=p2, path_type='sine', width_type='straight')

    route.points

    D = RouteBasic(route=route)

    D.rotate(angle = p1.orientation - D.port1.orientation, center = D.port1.midpoint)
    D.move(midpoint = p1, destination = D.port1)

    D.output()

