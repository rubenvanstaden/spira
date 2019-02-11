import spira
import numpy as np
from spira import param
from spira import shapes


class YtronShape(shapes.Shape):
    """ Shape for generating a yTron device. """

    rho = param.FloatField(default=0.2*1e6)
    arm_lengths = param.PointField(default=(5*1e6, 3*1e6))
    source_length = param.FloatField(default=5*1e6)
    arm_widths = param.PointField(default=(2*1e6, 2*1e6))
    theta = param.FloatField(default=2.5)
    theta_resolution = param.FloatField(default=10)

    xc = param.DataField(fdef_name='create_xc')
    yc = param.DataField(fdef_name='create_yc')
    arm_x_left = param.DataField(fdef_name='create_arm_x_left')
    arm_y_left = param.DataField(fdef_name='create_arm_y_left')
    arm_x_right = param.DataField(fdef_name='create_arm_x_right')
    arm_y_right = param.DataField(fdef_name='create_arm_y_right')
    rad_theta = param.DataField(fdef_name='create_rad_theta')

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

        points = np.array([list(zip(xpts, ypts))])

        return points


class NtronShape(shapes.Shape):
    """ Shape for generating a nTron device. """

    def create_points(self, points):


        return points


if __name__ == "__main__":

    ytron = YtronShape()
    cell = spira.Cell(name='yTron')
    cell += spira.Polygons(shape=ytron)
    cell.output()
