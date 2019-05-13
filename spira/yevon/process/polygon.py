import spira.all as spira
import numpy as np
from copy import deepcopy
from spira.core import param
# from spira import shapes
from spira.yevon.geometry import shapes
from spira.yevon.visualization import color
from spira.yevon.process.processlayer import ProcessLayer

from spira.core.param.variables import *
from spira.yevon.visualization.color import ColorField
from spira.yevon.geometry.coord import CoordField
from spira.core.elem_list import ElementalListField


class Polygon(ProcessLayer):

    color = ColorField(default=color.COLOR_BLUE_VIOLET)
    points = ElementalListField()

    # def __deepcopy__(self, memo):
    #     return Polygon(
    #         points=self.points,
    #         elementals=deepcopy(self.elementals),
    #         ps_layer=self.ps_layer,
    #         # polygon=deepcopy(self.polygon),
    #         node_id=deepcopy(self.node_id),
    #     )

    def create_elementals(self, elems):
        ply = spira.Polygon(shape=self.points, gds_layer=self.layer)

        # if self.transformation is not None:
        #     ply.transform_copy(self.transformation)
            
        elems += ply
        return elems






