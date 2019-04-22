import spira.all as spira
import numpy as np
from copy import deepcopy
from spira.yevon.geometry.shapes.basic import BoxShape
from spira.yevon.process.processlayer import ProcessLayer

from spira.core.param.variables import *
from spira.yevon.geometry.coord import CoordField


class Box(ProcessLayer):

    w = NumberField(default=1.0)
    h = NumberField(default=1.0)
    center = CoordField(default=(0,0))

    # def __deepcopy__(self, memo):
    #     return Box(
    #         # elementals=deepcopy(self.elementals),
    #         # polygon=deepcopy(self.polygon),
    #         ps_layer=self.ps_layer,
    #         node_id=deepcopy(self.node_id),
    #     )

    def create_elementals(self, elems):
        shape = BoxShape(width=self.w, height=self.h)
        shape.apply_merge
        ply = spira.Polygon(shape=shape, gds_layer=self.ps_layer.layer)

        if self.transformation is not None:
            ply.transform_copy(self.transformation)

        ply.center = self.center
        elems += ply
        return elems
