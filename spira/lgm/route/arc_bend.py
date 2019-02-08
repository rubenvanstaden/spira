import spira
import numpy as np
from spira import param


class ArcRoute(spira.Route):

    gdslayer = param.LayerField(name='ArcLayer', number=91)
    radius = param.FloatField(default=5*1e6)
    width = param.FloatField(default=1*1e6)
    theta = param.FloatField(default=45)
    start_angle = param.FloatField(default=0)
    angle_resolution = param.FloatField(default=15)
    angle1 = param.DataField(fdef_name='create_angle1')
    angle2 = param.DataField(fdef_name='create_angle2')

    def create_angle1(self):
        angle1 = (self.start_angle + 0) * np.pi/180
        return angle1

    def create_angle2(self):
        angle2 = (self.start_angle + self.theta + 0) * np.pi/180
        return angle2

    def create_port_input(self):
        midpoint = self.radius*np.cos(self.angle1), self.radius*np.sin(self.angle1)
        orientation = self.start_angle - 0 + 180*(self.theta<0)
        port = spira.Term(name='P1',
            midpoint=midpoint,
            width=self.width,
            length=0.2*1e6,
            orientation=orientation + 180
        )
        return port

    def create_port_output(self):
        midpoint = self.radius*np.cos(self.angle2), self.radius*np.sin(self.angle2)
        orientation = self.start_angle + self.theta + 180 - 180*(self.theta<0)
        port = spira.Term(name='P2',
            midpoint=midpoint,
            width=self.width,
            length=0.2*1e6,
            orientation=orientation + 180
        )
        return port

    def create_points(self, points):

        inner_radius = self.radius - self.width/2.0
        outer_radius = self.radius + self.width/2.0
        z = int(np.ceil(abs(self.theta) / self.angle_resolution))
        t = np.linspace(self.angle1, self.angle2, z)

        inner_points_x = (inner_radius*np.cos(t)).tolist()
        inner_points_y = (inner_radius*np.sin(t)).tolist()
        outer_points_x = (outer_radius*np.cos(t)).tolist()
        outer_points_y = (outer_radius*np.sin(t)).tolist()
        xpts = np.array(inner_points_x + outer_points_x[::-1])
        ypts = np.array(inner_points_y + outer_points_y[::-1])

        points = [[list(p) for p in list(zip(xpts, ypts))]]

        return points


class RectRoute(spira.Route):

    gdslayer = param.LayerField(name='ArcLayer', number=91)
    radius = param.FloatField(default=5*1e6)
    width = param.FloatField(default=1*1e6)
    size = param.MidPointField(default=(3*1e6,3*1e6))

    def create_port_input(self):
        port = spira.Term(name='P1',
            midpoint=[0, -self.size[1]],
            width=self.width,
            length=0.2*1e6,
            orientation=180
        )
        return port

    def create_port_output(self):
        port = spira.Term(name='P2',
            midpoint=[-self.size[0], 0],
            width=self.width,
            length=0.2*1e6,
            orientation=90
        )
        return port

    def create_points(self, points):

        w = self.width/2
        s1, s2 = self.size
        pts = [[w,w], [-s1,w], [-s1,-w], [-w,-w], [-w,-s2], [w,-s2]]

        points = np.array([pts])

        return points


class RectRouteTwo(spira.Route):

    gdslayer = param.LayerField(name='ArcLayer', number=91)
    radius = param.FloatField(default=5*1e6)
    width = param.FloatField(default=1*1e6)
    size = param.MidPointField(default=(3*1e6,3*1e6))

    def create_port_input(self):
        port = spira.Term(name='P1',
            midpoint=[0, self.size[1]],
            width=self.width,
            length=0.2*1e6,
            orientation=0
        )
        return port

    def create_port_output(self):
        port = spira.Term(name='P2',
            midpoint=[-self.size[0], 0],
            width=self.width,
            length=0.2*1e6,
            orientation=90
        )
        return port

    def create_points(self, points):

        w = self.width/2
        s1, s2 = self.size
        pts = [[w,-w], [-s1,-w], [-s1,w], [-w,w], [-w,s2], [w,s2]]

        points = np.array([pts])

        return points


class Arc(spira.RouteToCell):
    pass


class Rect(spira.RouteToCell):
    pass


if __name__ == '__main__':

    rect_route = RectRouteTwo()
    rect = Rect(shape=rect_route)
    rect.output()

    # rect_route = RectRoute()
    # rect = Rect(shape=rect_route)
    # rect.output()
    # # rect.rotate(aegle=0)
    # # rect.reflect(p1=(0,-10), p2=(-11,-10))
    # # rect.reflect()
    # # S = spira.SRef(rect)
    # # S.reflect(p1=(0,0), p2=(1,0))
    # # cell = spira.Cell()
    # # cell += S


    # arc_route = ArcRoute(start_angle=0, theta=90)
    # arc = Arc(shape=arc_route)
    # arc.output()











