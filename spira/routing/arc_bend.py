import spira
import numpy as np
import spira.kernel.parameters as param
from spira.kernel.utils import scale_coord_up as scu
from spira.kernel.utils import scale_polygon_up as spu


class ArcFractal(spira.Cell):

    # gdslayer = param.IntegerField(default=91)
    gdslayer = param.LayerField(name='ArcLayer', number=91)
    radius = param.FloatField(default=2)
    width = param.FloatField(default=0.5)
    theta = param.FloatField(default=45)
    start_angle = param.FloatField(default=0)
    angle_resolution = param.FloatField(default=2.5)

    poly = param.DataField(fdef_name='create_polygon')
    angle1 = param.DataField(fdef_name='create_angle1')
    angle2 = param.DataField(fdef_name='create_angle2')
    port1 = param.DataField(fdef_name='create_port1')
    port2 = param.DataField(fdef_name='create_port2')

    def create_angle1(self):
        angle1 = (self.start_angle) * np.pi/180
        return angle1

    def create_angle2(self):
        angle2 = (self.start_angle + self.theta) * np.pi/180
        return angle2

    def create_port1(self):
        midpoint = self.radius*np.cos(self.angle1), self.radius*np.sin(self.angle1)
        orientation = self.start_angle - 90 + 180*(self.theta<0)
        port = spira.Port(name='P1', midpoint=midpoint, width=self.width/3, length=self.width, orientation=orientation)
        return port

    def create_port2(self):
        midpoint = self.radius*np.cos(self.angle2), self.radius*np.sin(self.angle2)
        orientation = self.start_angle + self.theta + 90 - 180*(self.theta<0)
        port = spira.Port(name='P2', midpoint=midpoint, width=self.width/3, length=self.width, orientation=orientation)
        return port

    def create_polygon(self):
        inner_radius = self.radius - self.width/2.0
        outer_radius = self.radius + self.width/2.0
        t = np.linspace(self.angle1, self.angle2, np.ceil(abs(self.theta) / self.angle_resolution))

        inner_points_x = (inner_radius*np.cos(t)).tolist()
        inner_points_y = (inner_radius*np.sin(t)).tolist()
        outer_points_x = (outer_radius*np.cos(t)).tolist()
        outer_points_y = (outer_radius*np.sin(t)).tolist()
        xpts = np.array(inner_points_x + outer_points_x[::-1])
        ypts = np.array(inner_points_y + outer_points_y[::-1])

        poly = [list(p) for p in list(zip(xpts, ypts))]
        pp = spira.Polygons(polygons=spu([poly]), gdslayer=self.gdslayer)
        return pp

    def create_elementals(self, elems):

        elems += self.poly
        elems += self.port1
        elems += self.port2

        return elems


class Route90(spira.Cell):

    def create_elementals(self, elems):
        pass


if __name__ == '__main__':

    from spira import settings                                                                                            
    from spira.templates.library import library                                                                      

    settings.set_library(library)                                                                                         

    arc = ArcFractal(theta=90)
    elems = spira.ElementList()
    S = spira.SRef(arc)
    # print(S.ref.ports)
    # p1 = S.ports
    # elems += S
    arc.output(name='arc_bend')
