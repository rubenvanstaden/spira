import spira.all as spira
import numpy as np
from copy import deepcopy
from spira.yevon.geometry import shapes
from spira.yevon.geometry.shapes.shape import PointArrayField
from spira.yevon.visualization import color
from spira.yevon.process.processlayer import ProcessLayer

from spira.core.parameters.variables import *
from spira.yevon.visualization.color import ColorField
from spira.yevon.geometry.coord import CoordField
from spira.yevon.gdsii.elem_list import ElementalListField


class Polygon(ProcessLayer):

    color = ColorField(default=color.COLOR_BLUE_VIOLET)
    points = PointArrayField()

    def create_elementals(self, elems):
        self.shape = shapes.Shape(points=self.points)
        elems += spira.Polygon(shape=self.shape, gds_layer=self.layer)
        return elems






