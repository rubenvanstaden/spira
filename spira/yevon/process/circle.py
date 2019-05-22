import spira.all as spira
from spira.yevon.geometry import shapes
from spira.yevon.process.processlayer import ProcessLayer

from spira.core.parameters.variables import *
from spira.yevon.geometry.coord import CoordField
from spira.yevon.visualization.color import ColorField
from spira.core.parameters.descriptor import DataField


class Circle(ProcessLayer):

    center = CoordField()
    box_size = CoordField(default=(1.0*1e6, 1.0*1e6))
    angle_step = IntegerField(default=20)
    color = ColorField(default='#C0C0C0')
    points = DataField(fdef_name='create_points')

    def create_elementals(self, elems):
        shape = shapes.CircleShape(box_size=self.box_size, angle_step=self.angle_step)
        ply = spira.Polygon(shape=shape, gds_layer=self.ps_layer.layer)
        ply.center = self.center
        elems += ply
        return elems