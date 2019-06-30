import math
import gdspy
import numpy as np

from spira.yevon import constants
from spira.yevon.geometry.coord import CoordParameter
from spira.yevon.geometry.shapes.shape import *
from spira.core.parameters.variables import *
from spira.yevon.utils import geometry as geom
from spira.core.transforms.reflection import shape_reflect


class RectangleShape(Shape):
    """ Creates a rectangular shape. """

    p1 = CoordParameter(default=(0,0), doc='Bottom left corner coordinate.')
    p2 = CoordParameter(default=(2,2), doc='Top right corner coodinate.')

    def create_points(self, points):
        points = [[self.p1[0], self.p1[1]],
                  [self.p1[0], self.p2[1]],
                  [self.p2[0], self.p2[1]],
                  [self.p2[0], self.p1[1]]]
        return points


class BoxShape(Shape):
    """ Creates a box shape. """

    width = NumberParameter(default=1, doc='Width of the box shape.')
    height = NumberParameter(default=1, doc='Height of the box shape.')

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

    box_size = CoordParameter(default=(2.0, 2.0), doc='The width and height of the circle as a coordinate.')
    start_angle = FloatParameter(default=0.0, doc='Starting angle of the circle shape.')
    end_angle = FloatParameter(default=360.0, doc='Degree to which the circle must be completed.')
    angle_step = IntegerParameter(default=3, doc='The smoothness of the circle.')

    def create_points(self, points):
        sa = self.start_angle * constants.DEG2RAD
        ea = self.end_angle * constants.DEG2RAD 
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

    radius = FloatParameter(default=1.0)
    num_sides = IntegerParameter(default=6)

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


class CrossShape(Shape):
    """ Thickness sets the width of the arms. """

    box_size = NumberParameter(default=20)
    thickness = NumberParameter(default=5)

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

    begin_coord = CoordParameter(default=(0,0))
    end_coord = CoordParameter(default=(10,0))
    begin_width = NumberParameter(default=3)
    end_width = NumberParameter(default=1)

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

    begin_coord = CoordParameter(default=(0,0))
    end_coord = CoordParameter(default=(0,0))
    begin_width = NumberParameter(default=3)
    end_width = NumberParameter(default=1)

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


class BasicTriangle(Shape):

    a = FloatParameter(default=2)
    b = FloatParameter(default=0.5)
    c = FloatParameter(default=1)

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
        triangle = shape_reflect(triangle, reflection=False)
        # points = list(points)
        # points.extend(triangle.points)
        # return points
        return triangle.points


# class ArrowShape(TriangleShape):

#     # TODO: Implement point_list properties.
#     def create_points(self, points):
#         points = super().create_points(points)
#         height = 3*self.c
#         box = BoxShape(width=self.b/2, height=height)
#         box.move(pos=(0, -height/2))
#         points.extend(box.points)
#         return points


class ArrowShape(Shape):

    width = FloatParameter(default=1)
    length = FloatParameter(default=10)
    head = FloatParameter(default=3)

    def create_points(self, points):
        w = self.width
        l = self.length
        h = self.head
        cx = self.center[0]
        cy = self.center[1]
        overhang = h * 0.25
        points = np.array([
            [cx-l/2, cy-w/2], [cx-l/2, cy+w/2], [cx+(l/2-h), cy+w/2], 
            [cx+(l/2-h), w+overhang], [cx+l/2, cy-w/2]
        ])
        # points = np.array([
        #     [0,0], [l,0], [l-h, w+overhang], [l-h,w], [0,w]
        # ])
        return points


