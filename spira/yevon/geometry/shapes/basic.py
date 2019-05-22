import gdspy
import math
import numpy as np
from spira.settings import DEG2RAD
from spira.yevon.geometry.coord import CoordField
from spira.yevon.geometry.shapes.shape import *
from spira.core.parameters.variables import *
from spira.yevon.utils import geometry as geom


class RectangleShape(Shape):
    """ Creates a rectangular shape. """

    p1 = CoordField(default=(0,0), doc='Bottom left corner coordinate.')
    p2 = CoordField(default=(2*1e6,2*1e6), doc='Top right corner coodinate.')

    def create_points(self, points):
        points = [[self.p1[0], self.p1[1]],
                  [self.p1[0], self.p2[1]],
                  [self.p2[0], self.p2[1]],
                  [self.p2[0], self.p1[1]]]
        return points


class BoxShape(Shape):
    """ Creates a box shape. """

    width = NumberField(default=1*1e6, doc='Width of the box shape.')
    height = NumberField(default=1*1e6, doc='Height of the box shape.')

    def create_points(self, points):
        cx = self.center[0]
        cy = self.center[1]
        dx = 0.5 * self.width
        dy = 0.5 * self.height
        points = [(cx + dx, cy + dy),
                  (cx - dx, cy + dy),
                  (cx - dx, cy - dy),
                  (cx + dx, cy - dy)]
        return points


class CircleShape(Shape):
    """ Creates a circle shape. """

    box_size = CoordField(default=(2.0*1e6, 2.0*1e6), doc='The width and height of the circle as a coordinate.')
    start_angle = FloatField(default=0.0, doc='Starting angle of the circle shape.')
    end_angle = FloatField(default=360.0, doc='Degree to which the circle must be completed.')
    angle_step = IntegerField(default=3, doc='The smoothness of the circle.')

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
        points = pts
        return points


class ConvexShape(Shape):

    radius = FloatField(default=1.0*1e6)
    num_sides = IntegerField(default=6)

    def create_points(self, pts):
        if self.radius == 0.0:
            pts.append(self.center)
            return pts
        angle_step = 2 * math.pi / self.num_sides
        for i in range(0, self.num_sides):
            x0 = self.radius * np.cos((i + 0.5) * angle_step + math.pi / 2)
            y0 = self.radius * np.sin((i + 0.5) * angle_step + math.pi / 2)
            pts.append((self.center[0] + x0, self.center[1] + y0))
        points = pts
        return points


class BasicTriangle(Shape):

    a = FloatField(default=2*1e6)
    b = FloatField(default=0.5*1e6)
    c = FloatField(default=1*1e6)

    def create_points(self, points):
        p1 = [0, 0]
        p2 = [p1[0]+self.b, p1[1]]
        p3 = [p1[0], p1[1]+self.a]
        points = np.array([p1, p2, p3])
        return points


class TriangleShape(BasicTriangle):

    def create_points(self, points):
        points = super().create_points(points)
        triangle = BasicTriangle(a=self.a, b=self.b, c=self.c)
        # triangle.reflect()
        # print(points)
        points = list(points)
        points.extend(triangle.points)
        return points


class ArrowShape(TriangleShape):

    # TODO: Implement point_list properties.
    def create_points(self, points):
        points = super().create_points(points)
        height = 3*self.c
        box = BoxShape(width=self.b/2, height=height)
        box.move(pos=(0, -height/2))
        points.extend(box.points)
        return points


class CrossShape(Shape):
    """ Thickness sets the width of the arms. """

    box_size = NumberField(default=20*1e6)
    thickness = NumberField(default=5*1e6)

    def create_points(self, points):
        points += [(self.center[0]  - self.box_size / 2.0, self.center[1] - self.thickness / 2.0),
                (self.center[0] - self.box_size / 2.0, self.center[1] + self.thickness / 2.0),
                (self.center[0] - self.thickness / 2.0, self.center[1] + self.thickness / 2.0),
                (self.center[0] - self.thickness / 2.0, self.center[1] + self.box_size / 2.0),
                (self.center[0] + self.thickness / 2.0, self.center[1] + self.box_size / 2.0),
                (self.center[0] + self.thickness / 2.0, self.center[1] + self.thickness / 2.0),
                (self.center[0] + self.box_size / 2.0, self.center[1] + self.thickness / 2.0),
                (self.center[0] + self.box_size / 2.0, self.center[1] - self.thickness / 2.0),
                (self.center[0] + self.thickness / 2.0, self.center[1] - self.thickness / 2.0),
                (self.center[0] + self.thickness / 2.0, self.center[1] - self.box_size / 2.0),
                (self.center[0] - self.thickness / 2.0, self.center[1] - self.box_size / 2.0),
                (self.center[0] - self.thickness / 2.0, self.center[1] - self.thickness / 2.0),
                (self.center[0] - self.box_size / 2.0, self.center[1] - self.thickness / 2.0)]
        return points


class WedgeShape(Shape):
    """ wedge, or symmetric trapezium. specified by the center of baselines and the length of the baselines """

    begin_coord = CoordField(default=(0,0))
    end_coord = CoordField(default=(10*1e6,0))
    begin_width = NumberField(default=3*1e6)
    end_width = NumberField(default=1*1e6)

    def create_points(self, points):
        dist = geom.distance(self.end_coord, self.begin_coord)
        cosangle = (self.end_coord[0] - self.begin_coord[0]) / dist
        sinangle = (self.end_coord[1] - self.begin_coord[1]) / dist
        points = [(self.begin_coord[0] + sinangle * self.begin_width / 2.0, self.begin_coord[1] - cosangle * self.begin_width / 2.0),
               (self.begin_coord[0] - sinangle * self.begin_width / 2.0, self.begin_coord[1] + cosangle * self.begin_width / 2.0),
               (self.end_coord[0] - sinangle * self.end_width / 2.0, self.end_coord[1] + cosangle * self.end_width / 2.0),
               (self.end_coord[0] + sinangle * self.end_width / 2.0, self.end_coord[1] - cosangle * self.end_width / 2.0)]
        return points


class ParabolicShape(Shape):
    """ parabolic wedge (taper) """

    begin_coord = CoordField(default=(0,0))
    end_coord = CoordField(default=(0,0))
    begin_width = NumberField(default=3*1e6)
    end_width = NumberField(default=1*1e6)

    def create_points(self, pts):
        if (self.begin_width > self.end_width):
            ew = self.begin_width
            ec = self.begin_coord
            bw = self.end_width
            bc = self.end_coord
        else:
            bw = self.begin_width
            bc = self.begin_coord
            ew = self.end_width
            ec = self.end_coord

        length = geom.distance(ec, bc)
        angle = geom.angle_rad(ec, bc)
        sinangle = np.sin(angle)
        cosangle = np.cos(angle)

        dx = 0.01

        if abs(ew - bw) < dx:
            pts.extend([(bc[0] + sinangle * bw / 2.0, bc[1] - cosangle * bw / 2.0),
                        (bc[0] - sinangle * bw / 2.0, bc[1] + cosangle * bw / 2.0),
                        (ec[0] - sinangle * bw / 2.0, ec[1] + cosangle * ew / 2.0),
                        (ec[0] + sinangle * bw / 2.0, ec[1] - cosangle * ew / 2.0),
                        (bc[0] + sinangle * bw / 2.0, bc[1] - cosangle * bw / 2.0)])
            return pts

        if length < 0.0025:
            return pts

        a = 4.0 * length / (ew ** 2 - bw ** 2)
        y0 = a * bw ** 2 / 4.0
        y = y0
        width = bw

        east_shape = [(bc[0] + sinangle * bw / 2.0, bc[1] - cosangle * bw / 2.0)]
        west_shape = [(bc[0] - sinangle * bw / 2.0, bc[1] + cosangle * bw / 2.0)]

        READY = False
        while (not READY):
            width = width + 4 * dx + 4 * math.sqrt(dx * (width + dx))
            y = a * width ** 2 / 4.0

            if (y - y0 > length):
                READY = True
                coord = ec
                width = ew
            else:
                coord = (bc[0] + (y - y0) * cosangle, bc[1] + (y - y0) * sinangle)

            east_shape.append((coord[0] + sinangle * width / 2.0, coord[1] - cosangle * width / 2.0))
            west_shape.append((coord[0] - sinangle * width / 2.0, coord[1] + cosangle * width / 2.0))

        east_shape.reverse()
        pts += west_shape
        pts += east_shape
        return pts



