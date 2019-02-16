import spira
import numpy as np
from spira import param, shapes
from demo.pdks.ply.base import ProcessLayer


class Polygon(ProcessLayer):

    color = param.ColorField(default='#C0C0C0')
    points = param.ElementalListField()

    # def validate_parameters(self):
    #     if self.w < self.player.data.WIDTH:
    #         return False
    #     if self.h < self.player.data.WIDTH:
    #         return False
    #     return True

    def create_polygon(self):
        ply = spira.Polygons(shape=self.points, gdslayer=self.layer)
        return ply






