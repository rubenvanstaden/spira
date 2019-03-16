import spira
import numpy as np
from spira import param, shapes
from spira.process.processlayer import ProcessLayer


class Rectangle(ProcessLayer):

    p1 = param.PointField(default=(0,0))
    p2 = param.PointField(default=(2,2))

    def create_elementals(self, elems):
        shape = shapes.RectangleShape(p1=self.p1, p2=self.p2)
        shape.apply_merge
        elems += spira.Polygons(shape=shape, gds_layer=self.ps_layer.layer)
        return elems
