import spira.all as spira
from spira.all import RDD

import numpy as np
from spira.core.parameters.variables import *
from spira.yevon.geometry.coord import CoordParameter
from spira.core.parameters.descriptor import Parameter
from spira.yevon.geometry import shapes


class YtronShape(spira.Shape):
    """ Class for generating a yTron shape. """

    rho = NumberParameter(default=0.2, doc='Angle of concave bend between the arms.')
    arm_lengths = CoordParameter(default=(5,3), doc='Length or the left and right arms, respectively.')
    source_length = NumberParameter(default=5, doc='Length of the source arm.')
    arm_widths = CoordParameter(default=(2,2), doc='Width of the left and right arms, respectively.')
    theta = NumberParameter(default=3, doc='Angle of the left and right arms.')
    theta_resolution = NumberParameter(default=10, doc='Smoothness of the concave bend.')

    xc = Parameter(fdef_name='create_xc')
    yc = Parameter(fdef_name='create_yc')
    arm_x_left = Parameter(fdef_name='create_arm_x_left')
    arm_y_left = Parameter(fdef_name='create_arm_y_left')
    arm_x_right = Parameter(fdef_name='create_arm_x_right')
    arm_y_right = Parameter(fdef_name='create_arm_y_right')
    rad_theta = Parameter(fdef_name='create_rad_theta')
    ml = Parameter(fdef_name='create_midpoint_left')
    mr = Parameter(fdef_name='create_midpoint_right')
    ms = Parameter(fdef_name='create_midpoint_source')

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

    def create_midpoint_left(self):
        xc = -(self.xc + self.arm_x_left + self.arm_widths[0]/2)
        yc = self.yc + self.arm_y_left
        return [xc, yc]

    def create_midpoint_right(self):
        xc = self.xc + self.arm_x_right + self.arm_widths[1]/2
        yc = self.yc + self.arm_y_right
        return [xc, yc]

    def create_midpoint_source(self):
        xc = (self.arm_widths[1] - self.arm_widths[0])/2
        yc = -self.source_length + self.yc
        return [xc, yc]

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


class YtronDevice(spira.Device):

    shape = spira.ShapeParameter(restriction=spira.RestrictType([YtronShape]))

    def create_elements(self, elems):
        elems += spira.Polygon(shape=self.shape, layer=RDD.PLAYER.M1.METAL)
        return elems

    def create_ports(self, ports):

        left_arm_width = self.shape.arm_widths[0]
        rigth_arm_width = self.shape.arm_widths[1]
        src_arm_width = self.shape.arm_widths[0] + self.shape.arm_widths[1] + 2*self.shape.xc

        ports += spira.Port(name='Pl_M1', midpoint=self.shape.ml, width=left_arm_width, orientation=90)
        ports += spira.Port(name='Pr_M1', midpoint=self.shape.mr, width=rigth_arm_width, orientation=90)
        ports += spira.Port(name='Psrc_M1', midpoint=self.shape.ms, width=src_arm_width, orientation=270)

        return ports


if __name__ == '__main__':

    # shape = shapes.CircleShape()
    shape = YtronShape(theta_resolution=100)

    D = YtronDevice(shape=shape)
    D.gdsii_output(name='YtronDevice')

