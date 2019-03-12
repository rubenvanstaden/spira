import spira
import numpy as np
from spira import param
from spira.lgm.shapes.basic import BoxShape
from spira.process.processlayer import ProcessLayer


class Box(ProcessLayer):

    w = param.FloatField(default=1)
    h = param.FloatField(default=1)
    center = param.PointField()

    def create_elementals(self, elems):
        shape = BoxShape(width=self.w, height=self.h)
        shape.apply_merge
        ply = spira.Polygons(shape=shape, gdslayer=self.player.layer)
        ply.center = self.center
        elems += ply
        return elems
