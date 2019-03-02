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


class RoutePointShape(shapes.Shape):

    width = param.FloatField(default=1*1e8)
    angles = param.DataField(fdef_name='create_angles')

    def get_path(self):
        try:
            return self.__path__
        except:
            raise ValueError('Path not set for {}'.format(self.__class__.__name__))

    def set_path(self, value):
        self.__path__ = np.asarray(value)
    
    path = param.FunctionField(get_path, set_path)

    def create_angles(self):
        dxdy = self.path[1:] - self.path[:-1]
        angles = (np.arctan2(dxdy[:,1], dxdy[:,0])).tolist()
        angles = np.array([angles[0]] + angles + [angles[-1]])
        return angles

    def create_points(self, points):
        diff_angles = (self.angles[1:] - self.angles[:-1])
        mean_angles = (self.angles[1:] + self.angles[:-1])/2
        dx = self.width/2*np.cos((mean_angles - pi/2))/np.cos((diff_angles/2))
        dy = self.width/2*np.sin((mean_angles - pi/2))/np.cos((diff_angles/2))
        left_points = self.path.T - np.array([dx,dy])
        right_points = self.path.T + np.array([dx,dy])
        all_points = np.concatenate([left_points.T, right_points.T[::-1]])
        points = np.array([all_points])
        return points


class RouteBasic(spira.Cell):

    route = param.ShapeField()
    connect_layer = param.LayerField(doc='GDSII layer to which the route connects.')

    m1 = param.DataField(fdef_name='create_midpoint1')
    m2 = param.DataField(fdef_name='create_midpoint2')

    w1 = param.DataField(fdef_name='create_width1')
    w2 = param.DataField(fdef_name='create_width2')

    o1 = param.DataField(fdef_name='create_orientation1')
    o2 = param.DataField(fdef_name='create_orientation2')

    port1 = param.DataField(fdef_name='create_port1')
    port2 = param.DataField(fdef_name='create_port2')
    llayer = param.DataField(fdef_name='create_layer')

    def create_layer(self):
        ll = spira.Layer(
            number=self.connect_layer.number,
            datatype=RDD.PURPOSE.TERM.datatype
        )
        return ll

    def create_midpoint1(self):
        midpoint = (0,0)
        if isinstance(self.route, RoutePointShape):
            midpoint = self.route.path[0]
        return midpoint

    def create_midpoint2(self):
        midpoint = (0,0)
        if isinstance(self.route, RoutePointShape):
            midpoint = self.route.path[-1]
        elif isinstance(self.route, RouteShape):
            midpoint = [self.route.x_dist, self.route.y_dist]
        return midpoint

    def create_width1(self):
        width = (0,0)
        if isinstance(self.route, RoutePointShape):
            width = self.route.width
        elif isinstance(self.route, RouteShape):
            width = self.route.width1
        return width

    def create_width2(self):
        width = (0,0)
        if isinstance(self.route, RoutePointShape):
            width = self.route.width
        elif isinstance(self.route, RouteShape):
            width = self.route.width2
        return width

    def create_orientation1(self):
        orientation = 0
        if isinstance(self.route, RoutePointShape):
            # orientation = self.route.angles[0]*180/pi+180
            orientation = self.route.angles[0]*180/pi+90
        elif isinstance(self.route, RouteShape):
            orientation = 180
        return orientation

    def create_orientation2(self):
        orientation = 0
        if isinstance(self.route, RoutePointShape):
            # orientation = self.route.angles[-1]*180/pi
            orientation = self.route.angles[-1]*180/pi-90
        elif isinstance(self.route, RouteShape):
            orientation = 0
        return orientation

    def create_port1(self):
        term = spira.Term(name='TERM1',
            # midpoint=(0,0),
            midpoint=self.m1,
            # width=self.route.width1,
            # width=self.w1,
            width=self.w1[0],
            length=0.2*1e6,
            # orientation=180,
            orientation=self.o1,
            gdslayer=self.llayer
        )
        term.rotate(angle=-90)
        return term

    def create_port2(self):
        term = spira.Term(name='TERM2',
            # midpoint=[self.route.x_dist, self.route.y_dist],
            midpoint=self.m2,
            # width=self.route.width2,
            # width=self.w2,
            width=self.w2[0],
            length=0.2*1e6,
            # orientation=0,
            orientation=self.o2,
            gdslayer=self.llayer
        )
        term.rotate(angle=-90)
        return term

    def create_elementals(self, elems):
        ply = spira.Polygons(shape=self.route, gdslayer=self.connect_layer)
        ply.rotate(angle=-90)
        elems += ply
        return elems

    def create_ports(self, ports):
        ports += self.port1
        ports += self.port2
        return ports


# class Route(spira.Cell):

#     port1 = param.PortField(default=None)
#     port2 = param.PortField(default=None)

#     path = param.PointArrayField()
#     width = param.FloatField(default=1*1e8)

#     player = param.PhysicalLayerField()

#     route_shape = param.DataField(fdef_name='create_route_shape')

#     # def validate_parameters(self):
#     #     if self.port1.width < self.player.data.WIDTH:
#     #         return False
#     #     if self.port2.width < self.player.data.WIDTH:
#     #         return False
#     #     return True

#     def determine_type(self):
#         if self.path:
#             self.__type__ = 'path'
#         if self.port1 and self.port2:
#             self.__type__ = 'straight'

#     def create_route_shape(self):
#         if self.__type__ == 'straight':
#             route_shape = RouteShape(
#                 port1=self.port1,
#                 port2=self.port2,
#                 path_type='straight',
#                 width_type='straight'
#             )
#         elif self.__type__ == 'path':
#             route_shape = RoutePointShape(
#                 path=self.path,
#                 width=self.width
#             )
#         else:
#             raise ValueError('Routing type algorithm does not exist.')
#         return route_shape

#     def create_elementals(self, elems):

#         R1 = RouteBasic(route=self.route_shape, connect_layer=self.player.layer)
#         r1 = spira.SRef(R1)

#         if self.__type__ == 'straight':
#             r1.rotate(angle=self.port2.orientation-180, center=R1.port1.midpoint)
#             r1.move(midpoint=(0,0), destination=self.port1.midpoint)
#         if self.__type__ == 'path':
#             r1.connect(port=r1.ports['TERM1'], destination=self.port1)

#         elems += r1

#         # for e in r1.flatten():
#         #     elems += e

#         return elems


if __name__ == '__main__':

    # # p1 = spira.Term(name='P1', midpoint=(0,0), orientation=90, width=2)
    # # p2 = spira.Term(name='P2', midpoint=(0,30), orientation=-90, width=1)

    # p1 = spira.Term(name='P1', midpoint=(0,0), orientation=180, width=2*1e6)
    # p2 = spira.Term(name='P2', midpoint=(30*1e6,0), orientation=0, width=2*1e6)

    # route = RouteShape(port1=p1, port2=p2, path_type='straight', width_type='straight')

    # # p1 = spira.Term(name='P1', midpoint=(0,0), orientation=-90, width=1)
    # # p2 = spira.Term(name='P2', midpoint=(30,30), orientation=90, width=1)

    # # route = RouteShape(port1=p1, port2=p2, path_type='sine', width_type='straight')

    # route.points

    # D = RouteBasic(route=route)

    # D.rotate(angle=p1.orientation-D.port1.orientation, center=D.port1.midpoint)
    # D.move(midpoint=p1, destination=D.port1)

    # D.output()

    # ------------------------ RoutePoints ----------------------------------

    route = RoutePointShape(
        # path=[(0,0), (4*1e6,0), (4*1e6,8*1e6)],
        path=[(0,0), (0,-5*1e6), (10*1e6,-5*1e6), (10*1e6,0), (15*1e6,0)],
        width=1*1e6
    )

    # R1 = RouteBasic(route=route, connect_layer=self.player.layer)
    # r1 = spira.SRef(R1)
    # r1.rotate(angle=self.port2.orientation-180, center=R1.port1.midpoint)
    # r1.move(midpoint=(0,0), destination=self.port1.midpoint)

    D = RouteBasic(route=route)

    # D.rotate(angle=p1.orientation-D.port1.orientation, center=D.port1.midpoint)
    # D.move(midpoint=p1, destination=D.port1)

    D.output()



