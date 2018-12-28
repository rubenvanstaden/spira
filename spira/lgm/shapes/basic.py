import gdspy
import spira
import math
import numpy as np
from spira import param
from spira.settings import DEG2RAD
from spira.lgm.shapes.shape import Shape

from spira.gdsii.elemental.polygons import PolygonAbstract
from spira.gdsii.elemental.polygons import Polygons
from spira.gdsii.utils import scale_polygon_up as spu
from spira.gdsii.utils import scale_coord_down as scd
from spira.core.initializer import FieldInitializer


class RectangleShape(Shape):

    p1 = param.PointField()
    p2 = param.PointField()

    def create_points(self, points):
        pts = [[self.p1[0], self.p1[1]], [self.p1[0], self.p2[1]],
               [self.p2[0], self.p2[1]], [self.p2[0], self.p1[1]]]
        points = np.array([pts])
        return points


class BoxShape(Shape):

    width = param.FloatField(default=1)
    height = param.FloatField(default=1)

    def create_points(self, points):
        cx = self.center[0]
        cy = self.center[1]
        dx = 0.5 * self.width
        dy = 0.5 * self.height
        pts = [(cx + dx, cy + dy),
               (cx - dx, cy + dy),
               (cx - dx, cy - dy),
               (cx + dx, cy - dy)]
        points = np.array([pts])
        return points


class CircleShape(Shape):

    box_size = param.PointField(default=(1.0, 1.0))
    start_angle = param.FloatField(default=0.0)
    end_angle = param.FloatField(default=360.0)
    angle_step = param.FloatField(default=3)

    def create_points(self, points):
        sa = self.start_angle * DEG2RAD
        ea = self.end_angle * DEG2RAD 
        h_radius = self.box_size[0] / 2.0
        v_radius = self.box_size[1] / 2.0
        n_s = float(self.end_angle - self.start_angle) / self.angle_step
        n_steps = int(math.ceil(abs(n_s))) * np.sign(n_s)
        if n_steps == 0: 
            if sa == ea:
                pts = np.array([[math.cos(sa) * h_radius+self.center[0],
                                 math.sin(sa) * v_radius+self.center[1]]])
            else:
                pts = np.array([[math.cos(sa) * h_radius+self.center[0],
                                 math.sin(sa) * v_radius+self.center[1]],
                                [math.cos(ea) * h_radius+self.center[0],
                                 math.sin(ea) * v_radius+self.center[1]]])
            return pts

        angle_step = float(ea - sa) / n_steps
        if self.clockwise:
            angle_step = -angle_step
            sign = -1
        else:
            sign = +1
        while sign * sa > sign * ea:
            ea += sign * 2 * math.pi

        angles = np.arange(sa, ea + 0.5 * angle_step, angle_step)
        pts = np.column_stack((np.cos(angles), np.sin(angles))) \
                               * np.array([(h_radius, v_radius)]) \
                               + np.array([(self.center[0], self.center[1])])

        points = np.array([pts])

        return points


class ConvexPolygon(Shape):

    radius = param.FloatField(default=1.0)
    num_sides = param.IntegerField(default=6)
    
    def create_points(self, pts):
        if self.radius == 0.0:
            pts.append(self.center)
            return pts
        angle_step = 2 * math.pi / self.num_sides
        for i in range(0, self.num_sides):
            x0 = self.radius * np.cos((i + 0.5) * angle_step + math.pi / 2)
            y0 = self.radius * np.sin((i + 0.5) * angle_step + math.pi / 2)
            pts.append((self.center[0] + x0, self.center[1] + y0))
        points = np.array([pts])
        return points


class BasicTriangle(Shape):

    a = param.FloatField(default=2)
    b = param.FloatField(default=0.5)
    c = param.FloatField(default=1)

    def create_points(self, points):
        p1 = [0, 0]
        p2 = [p1[0]+self.b, p1[1]]
        p3 = [p1[0], p1[1]+self.a]
        pts = np.array([p1, p2, p3])
        points = [pts]
        return points


class TriangleShape(BasicTriangle):

    def create_points(self, points):
        points = super().create_points(points)
        triangle = BasicTriangle(a=self.a, b=self.b, c=self.c)
        triangle.reflect()
        points.extend(triangle.points)
        return points


class ArrowShape(TriangleShape):

    # TODO: Implement point_list properties.
    def create_points(self, points):
        points = super().create_points(points)
        height = 3*self.c
        box = BoxShape(width=self.b/2, height=height)
        box.move(pos=(0,-height/2))
        points.extend(box.points)
        return points


if __name__ == '__main__':
    # shape = CircleShape()
    # shape = ConvexPolygon()
    shape = ArrowShape()
    shape.apply_merge

    ply = spira.Polygons(shape=shape, gdslayer=spira.Layer(number=13))
    cell = spira.Cell(name='yTron')
    cell += ply
    cell.output()


