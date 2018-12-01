import spira
import numpy as np
import spira.kernel.parameters as param
from spira.routing.arc_bend import ArcFractal


class SubArcSeries(spira.Cell):

    gdslayer = param.LayerField(number=99)
    radius = param.FloatField(default=20)
    width = param.FloatField(default=1.0)
    angular_coverage = param.FloatField(default=30)
    num_steps = param.IntegerField(default=1)
    angle_resolution = param.FloatField(default=0.1)
    start_angle = param.IntegerField(default=0)

    def _regular_bend(self, prev_port):
        """ Now connect a regular bend for
        the normal curved portion. """
        B = ArcFractal(radius=self.radius,
                       width=self.width,
                       theta=45 - np.rad2deg(self.angular_coverage),
                       start_angle=self.angular_coverage,
                       angle_resolution=self.angle_resolution,
                       gdslayer=spira.Layer(number=88))

        b = spira.SRef(B)

        b.connect(port='P1', destination=prev_port)

        p0 = b.ports['P2']
        prev_port = spira.Port(name='P2',
                         midpoint=p0.midpoint,
                         width=p0.width,
                         orientation=p0.orientation)

        return [b, prev_port]

    def create_elementals(self, elems):

        self.angular_coverage = np.deg2rad(self.angular_coverage)
        inc_rad = (self.radius**-1) / self.num_steps
        angle_step = self.angular_coverage / self.num_steps

        print('inc_rad: {}'.format(inc_rad))
        print('angle_step: {}'.format(angle_step))

        arcs = []
        for x in range(self.num_steps):
            A = ArcFractal(radius=1/((x+1)*inc_rad),
                           width=self.width,
                           theta=np.rad2deg(angle_step),
                           start_angle=x * np.rad2deg(angle_step),
                           angle_resolution=self.angle_resolution,
                           gdslayer=self.gdslayer)

            a = spira.SRef(A)
            elems += a
            arcs.append(a)
            if x > 0:
                a.connect(port='P1', destination=prevPort)
            prevPort = a.ports['P2']

        elems += arcs[0].ports['P1']

        elems += self._regular_bend(prevPort)

        return elems


class ArcSeries(spira.Cell):

    gdslayer = param.LayerField(number=91)
    radius = param.FloatField(default=20)
    width = param.FloatField(default=1.0)
    angular_coverage = param.FloatField(default=30)
    num_steps = param.IntegerField(default=1)
    angle_resolution = param.FloatField(default=0.1)
    start_angle = param.IntegerField(default=0)
    direction = param.StringField(default='ccw')

    def create_elementals(self, elems):

        D = SubArcSeries(
            gdslayer = self.gdslayer,
            radius = self.radius,
            width = self.width,
            angular_coverage = self.angular_coverage,
            num_steps = self.num_steps,
            angle_resolution = self.angle_resolution,
            start_angle = self.start_angle
        )

        s1 = spira.SRef(D)
        s2 = spira.SRef(D)

        s2.reflect(p1=[0,0], p2=[1,1])
        s2.connect(port='P2', destination=s1.ports['P2'])

        elems += s1
        elems += s2

        elems += s1.ports['P1'].modified_copy(name='Port_1')
        elems += s2.ports['P1'].modified_copy(name='Port_2')

        return elems


class GradualFractal(spira.Cell):

    """
    Creates a 90-degree bent waveguide the bending radius is
    gradually increased until it reaches the minimum
    value of the radius at the "angular coverage" angle.
    It essentially creates a smooth transition to a bent waveguide
    mode. User can control number of steps provided. Direction
    determined by start angle and cw or ccw switch with the
    default 10 "num_steps" and 15 degree coverage,
    effective radius is about 1.5*radius.
    """

    gdslayer = param.LayerField(number=91)
    radius = param.FloatField(default=20)
    width = param.FloatField(default=1.0)
    angular_coverage = param.FloatField(default=20)
    num_steps = param.IntegerField(default=5)
    angle_resolution = param.FloatField(default=0.01)
    start_angle = param.IntegerField(default=0)
    direction = param.StringField(default='ccw')

    def create_elementals(self, elems):

        D = ArcSeries(
            gdslayer = self.gdslayer,
            radius = self.radius,
            width = self.width,
            angular_coverage = self.angular_coverage,
            num_steps = self.num_steps,
            angle_resolution = self.angle_resolution,
            start_angle = self.start_angle
        )

        # D.xmin, D.ymin = 0, 0

        # Orient to default settings...
        # D.reflect(p1=[0,0], p2=[1,1])
        # D.reflect(p1=[0,0], p2=[1,0])

        # D.rotate(angle=self.start_angle, center=D.center)
        # D.center = [0, 0]

        s1 = spira.SRef(D)
        elems += s1

        return elems


if __name__ == '__main__':

    from spira import settings
    from spira.templates.library import library

    settings.set_library(library)

    gradual = GradualFractal()
    elems = spira.ElementList()
    elems += spira.SRef(gradual)
    # S = spira.SRef(gradual)
    # S.ports
    gradual.output(name='gradual_bend')
