import spira
from spira import param
from spira import shapes
from demo.pdks.ply.base import Base


class Box(Base):

    w = param.FloatField(default=1)
    h = param.FloatField(default=1)
    center = param.PointField()

    def validate_parameters(self):
        if self.w < self.player.data.WIDTH:
            return False
        if self.h < self.player.data.WIDTH:
            return False
        return True

    def create_polygon(self):
        shape = shapes.BoxShape(center=self.center, width=self.w, height=self.h)
        ply = spira.Polygons(shape=shape, gdslayer=self.player.layer)
        return ply

