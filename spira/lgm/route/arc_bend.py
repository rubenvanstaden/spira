import spira
import numpy as np
from spira import param
from spira.gdsii.utils import scale_coord_up as scu
from spira.gdsii.utils import scale_polygon_up as spu


class ArcRoute(spira.Route):

    gdslayer = param.LayerField(name='ArcLayer', number=91)
    radius = param.FloatField(default=5)
    width = param.FloatField(default=1)
    theta = param.FloatField(default=45)
    start_angle = param.FloatField(default=0)
    angle_resolution = param.FloatField(default=1)
    angle1 = param.DataField(fdef_name='create_angle1')
    angle2 = param.DataField(fdef_name='create_angle2')

    def create_angle1(self):
        angle1 = (self.start_angle) * np.pi/180
        return angle1

    def create_angle2(self):
        angle2 = (self.start_angle + self.theta) * np.pi/180
        return angle2

    def create_port_input(self):
        midpoint = self.radius*np.cos(self.angle1), self.radius*np.sin(self.angle1)
        orientation = self.start_angle - 90 + 180*(self.theta<0)
        port = spira.Term(name='P1',
            midpoint=midpoint,
            width=self.width,
            length=0.2,
            orientation=orientation
        )
        return port

    def create_port_output(self):
        midpoint = self.radius*np.cos(self.angle2), self.radius*np.sin(self.angle2)
        orientation = self.start_angle + self.theta + 90 - 180*(self.theta<0)
        port = spira.Term(name='P2',
            midpoint=midpoint,
            width=self.width,
            length=0.2,
            orientation=orientation
        )
        return port

    def create_points(self, points):

        inner_radius = self.radius - self.width/2.0
        outer_radius = self.radius + self.width/2.0
        t = np.linspace(self.angle1, self.angle2, np.ceil(abs(self.theta) / self.angle_resolution))

        inner_points_x = (inner_radius*np.cos(t)).tolist()
        inner_points_y = (inner_radius*np.sin(t)).tolist()
        outer_points_x = (outer_radius*np.cos(t)).tolist()
        outer_points_y = (outer_radius*np.sin(t)).tolist()
        xpts = np.array(inner_points_x + outer_points_x[::-1])
        ypts = np.array(inner_points_y + outer_points_y[::-1])

        points = [[list(p) for p in list(zip(xpts, ypts))]]

        return points


class Arc(spira.RouteToCell):
    pass


if __name__ == '__main__':

    arc_route = ArcRoute(theta=90)
    arc = Arc(shape=arc_route)
    arc.output()











