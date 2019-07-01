import spira.all as spira
import numpy as np
from spira.core.parameters.variables import *
from spira.yevon.geometry.coord import CoordParameter
from spira.core.parameters.descriptor import Parameter
from spira.yevon.geometry.shapes.shape import *


class YtronShape(Shape):
    """ Shape for generating a yTron device. """

    rho = NumberParameter(default=0.2)
    arm_lengths = CoordParameter(default=(5,3))
    source_length = NumberParameter(default=5)
    arm_widths = CoordParameter(default=(2, 2))
    theta = NumberParameter(default=2.5)
    theta_resolution = NumberParameter(default=10.0)

    xc = Parameter(fdef_name='create_xc')
    yc = Parameter(fdef_name='create_yc')
    arm_x_left = Parameter(fdef_name='create_arm_x_left')
    arm_y_left = Parameter(fdef_name='create_arm_y_left')
    arm_x_right = Parameter(fdef_name='create_arm_x_right')
    arm_y_right = Parameter(fdef_name='create_arm_y_right')
    rad_theta = Parameter(fdef_name='create_rad_theta')
    
    def create_rad_theta(self):
        return self.theta * np.pi/180

    def create_xc(self):
        return self.rho * np.cos(self.rad_theta)

    def create_yc(self):
        return self.rho * np.sin(self.rad_theta)

    def create_arm_x_left(self):
        return self.arm_lengths[0] * np.sin(self.rad_theta)

    def create_arm_y_left(self):
        return self.arm_lengths[0] * np.cos(self.rad_theta)

    def create_arm_x_right(self):
        return self.arm_lengths[1] * np.sin(self.rad_theta)

    def create_arm_y_right(self):
        return self.arm_lengths[1] * np.cos(self.rad_theta)

    def create_points(self, points):

        theta = self.theta * np.pi/180
        theta_resolution = self.theta_resolution * np.pi/180
        theta_norm = int((np.pi-2*theta)/theta_resolution) + 2
        thetalist = np.linspace(-(np.pi-theta), -theta, theta_norm)
        semicircle_x = self.rho * np.cos(thetalist)
        semicircle_y = self.rho * np.sin(thetalist)+self.rho

        xpts = semicircle_x.tolist() + [
            self.xc + self.arm_x_right, 
            self.xc + self.arm_x_right + self.arm_widths[1],
            self.xc + self.arm_widths[1], 
            self.xc + self.arm_widths[1],
            0, -(self.xc + self.arm_widths[0]), 
            -(self.xc + self.arm_widths[0]),
            -(self.xc + self.arm_x_left + self.arm_widths[0]), 
            -(self.xc + self.arm_x_left)
        ]

        ypts = semicircle_y.tolist() + [
            self.yc + self.arm_y_right, 
            self.yc + self.arm_y_right, 
            self.yc, self.yc - self.source_length,
            self.yc - self.source_length, 
            self.yc - self.source_length, 
            self.yc, self.yc + self.arm_y_left, 
            self.yc + self.arm_y_left
        ]

        points = np.array(list(zip(xpts, ypts)))

        return points


class NtronShape(Shape):
    """ Shape for generating a nTron device. """



    def create_points(self, points):



        return points


