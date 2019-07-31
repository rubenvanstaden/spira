import math
import spira.all as spira
from spira import shapes


class __ShapeContainer__(shapes.Shape):
    original_shape = param.ShapeParameter()


class ShapeNormal(__ShapeContainer__):

    def __init__(self, original_shape, **kwargs):
        super().__init__(original_shape=original_shape, **kwargs)

    def create_points(self, pts):
        points = np.array(self.original_shape.points)
        return points


class BezierCurve(__ShapeContainer__):
    """ polynomial bezier curve based on a shape with control points """
    steps = param.FloatParameter(default=100)

    def __init__(self, original_shape, **kwargs):
        super().__init__(original_shape=original_shape, **kwargs)

    def create_points(self, pts):
        step = 1.0 / self.steps
        t = np.arange(0.0, 1.0 + 0.5 * step, step)
        P = np.array(self.original_shape.points[0])
        Px = np.outer(P[:, 0], np.ones(np.size(t)))
        Py = np.outer(P[:, 1], np.ones(np.size(t)))

        for j in range(len(self.original_shape.points[0]) - 1,  0, -1):
            Px = Px[0:j, :] + np.diff(Px, 1, 0) * t
            Py = Py[0:j, :] + np.diff(Py, 1, 0) * t

        pts = np.transpose(np.row_stack((Px, Py)))
        points = np.array([pts])

        return points

 
class BasicSpline(shapes.Shape):
    """  """

    radius = param.FloatParameter(default=5)
    angle = param.FloatParameter(default=10)
    angle_step = param.FloatParameter(default=2)

    def create_points(self,pts):
        DEG2RAD = np.pi / 180.0
        alpha = self.angle * DEG2RAD
        c = math.sin(alpha)
        if self.angle == 45.0:
            t = 0.5
        else:
            c2 = c**2
            t = math.sin(math.atan(((1.0-c2)/c2)**0.125))**2

        L = self.radius * 2 * t * (1-t) / (3* (t**4 + (1-t)**4)**1.5)

        q0_0 = np.array([-L, 0])
        q0_1 = np.array([0,0])
        q0_2 = np.array([0,0])
        q0_3 = np.array([0, L])
        
        q1_0 = t * q0_0 + (1-t) * q0_1
        q2_0 = t**2 * q0_0 + 2*t*(1-t) * q0_1 + (1-t)**2 * q0_2
        q3_0 = t**3 * q0_0 + 3*t**2*(1-t) * q0_1 + 3 * t * (1-t)**2 * q0_2 + (1-t)**3 * q0_3

        S = shapes.Shape(points=[[q0_0, q1_0, q2_0, q3_0]])

        steps = int(math.ceil(2.0* self.angle / self.angle_step))
        return BezierCurve(original_shape=S, steps=steps).points


# class AdiabaticSplineCircleSplineShape(Shape):
#     start_point = param.CoordParameter()
#     turn_point = param.CoordParameter()
#     end_point = param.CoordParameter()
    
#     radius = param.FloatParameter(required = True)
#     angle_step = param.FloatParameter(default=1)
#     adiabatic_angles = param.FloatParameter(default=0)
    
#     def define_points(self,pts):
#         alpha_in = self.adiabatic_angles[0]
#         alpha_out = self.adiabatic_angles[1]
#         turn_angle = turn_deg(self.start_point, self.turn_point, self.end_point)
        
#         if (alpha_in + alpha_out) > abs(turn_angle):
#             alpha_in = alpha_out = 0.5 * abs(turn_angle)
    
#         bend_angle = abs(turn_angle) - alpha_in-alpha_out
        
#         # first section
#         if alpha_in > 0.0:
#             S5 = BasicSpline(radius = self.radius, angle = alpha_in, angle_step = self.angle_step)
#         else:
#             S5 = Shape((- self.radius, 0))
    
#         # middle section
#         if bend_angle > 0.0:
#             S5 += ShapeBendRelative(start_point = S5[-1],
#                                     input_angle = alpha_in,
#                                     angle_amount = bend_angle,
#                                     radius = self.radius,
#                                     angle_step = self.angle_step,
#                                     )
            
#         # last section
#         if alpha_out > 0.0:
#             S6 = Shape(BasicSpline(radius = self.radius, angle = alpha_out, angle_step = self.angle_step))
#         else:
#             S6 = Shape((-self.radius, 0))
#         S6.h_mirror()
#         S6.rotate((0, 0), abs(turn_angle))
#         S6.reverse()
#         S6.move(S5[-1] - S6[0])
        
#         # transform to match the right position
        
#         S = S5 + S6
        
#         if turn_angle < 0:
#             S.v_mirror()
    
#         L = straight_line_from_point_angle((0.0,0.0), turn_angle)
#         d = L.distance(S[-1])
    
#         ep = S[-1]
#         if abs(turn_angle) == 90.0:
#             d = ep.x
#         else:
#             d = ep.x - ep.y*math.cos(turn_angle * DEG2RAD)/ math.sin(turn_angle*DEG2RAD)
        
#         S.move((-d, 0.0))
#         S.rotate((0.0,0.0), orientation(self.turn_point, self.start_point))
#         S.move(self.turn_point)
#         S.remove_identicals()
        
#         return S.points


# s = Shape([[(0.0, 0.0), (1.0, 1.0), (2.0, -1.0), (3.0, 0.0)]])
s = shapes.Shape([[(0.0, 3.0), (10.0, 3.0), (15.0, 0.0), (18.0, 0.0)]])
s1 = ShapeNormal(original_shape=s)
s2 = BezierCurve(original_shape=s)
s3 = BasicSpline()

p1 = np.array(s1.points[0])
p2 = np.array(s2.points[0])
p3 = np.array(s3.points[0])

x1, y1 = p1.transpose()
x, y = p2.transpose()
x3, y3 = p3.transpose()

import numpy as np
from scipy import interpolate

import matplotlib.pyplot as plt
# plt.plot(x1, y1, 'bo-')
# plt.plot(x, y, 'r-')
plt.plot(x3, y3, 'r-')

# plt.figure()
# plt.plot(x, y, 'ro', xpts, ypts, 'b')
# plt.legend(['Points', 'Interpolated B-spline', 'True'],loc='best')
# plt.axis([min(x)-1, max(x)+1, min(y)-1, max(y)+1])
# plt.title('B-Spline interpolation')
plt.show()

