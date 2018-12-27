import spira
import numpy as np
from spira import param
from spira import shapes


class NtronShape(shapes.Shape):
    """  """

    def create_points(self, points):


        return points


class YtronShape(shapes.Shape):
    """  """

    rho = param.IntegerField(default=1)
    arm_lengths = param.PointField(default=(500, 300))
    source_length = param.IntegerField(default=500)
    arm_widths = param.PointField(default=(200, 200))
    theta = param.FloatField(default=2.5)
    theta_resolution = param.FloatField(default=10)

    def create_points(self, points):

        theta = self.theta * np.pi/180
        theta_resolution = self.theta_resolution * np.pi/180
        thetalist = np.linspace(-(np.pi-theta),-theta, int((np.pi-2*theta)/theta_resolution) + 2)
        semicircle_x = self.rho * np.cos(thetalist)
        semicircle_y = self.rho * np.sin(thetalist)+self.rho

        xc = self.rho * np.cos(theta)
        yc = self.rho * np.sin(theta)
        arm_x_left = self.arm_lengths[0] * np.sin(theta)
        arm_y_left = self.arm_lengths[0] * np.cos(theta)
        arm_x_right = self.arm_lengths[1] * np.sin(theta)
        arm_y_right = self.arm_lengths[1] * np.cos(theta)

        xpts = semicircle_x.tolist() + [xc+arm_x_right, xc+arm_x_right+self.arm_widths[1], 
                                        xc+self.arm_widths[1], xc+self.arm_widths[1], 
                                        0, -(xc+self.arm_widths[0]), -(xc+self.arm_widths[0]), 
                                        -(xc+arm_x_left+self.arm_widths[0]), -(xc+arm_x_left)] 
        ypts = semicircle_y.tolist() + [yc+arm_y_right, yc+arm_y_right, yc, yc-self.source_length, 
                                        yc-self.source_length, yc-self.source_length, yc, 
                                        yc+arm_y_left, yc+arm_y_left]

        points = np.array([zip(xpts, ypts)])

        return points
