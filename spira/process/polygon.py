import spira
import numpy as np
from spira import param, shapes
from spira.visualization import color
from spira.process.processlayer import ProcessLayer


class Polygon(ProcessLayer):

    color = param.ColorField(default=color.COLOR_BLUE_VIOLET)
    points = param.ElementalListField()

    def create_elementals(self, elems):
        elems += spira.Polygons(shape=self.points, gdslayer=self.player.layer)
        return elems






