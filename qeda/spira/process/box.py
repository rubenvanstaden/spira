import spira
import numpy as np
from copy import deepcopy
from core import param
from spira.geometry.shapes.basic import BoxShape
from spira.process.processlayer import ProcessLayer


class Box(ProcessLayer):

    w = param.NumberField(default=1.0)
    h = param.NumberField(default=1.0)
    center = param.CoordField()

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
