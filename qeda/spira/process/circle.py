import spira
from core import param
from spira import shapes
from spira.process.processlayer import ProcessLayer


class Circle(ProcessLayer):

    center = param.CoordField()
    box_size = param.CoordField(default=(1.0*1e6, 1.0*1e6))
    angle_step = param.IntegerField(default=20)
    color = param.ColorField(default='#C0C0C0')
    points = param.DataField(fdef_name='create_points')

    def create_elementals(self, elems):
        shape = shapes.CircleShape(box_size=self.box_size, angle_step=self.angle_step)
        ply = spira.Polygon(shape=shape, gds_layer=self.ps_layer.layer)
        ply.center = self.center
        elems += ply
        return elems