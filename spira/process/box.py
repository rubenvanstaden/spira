import spira
import numpy as np
from copy import deepcopy
from spira import param
from spira.lgm.shapes.basic import BoxShape
from spira.process.processlayer import ProcessLayer


class Box(ProcessLayer):

    w = param.NumberField(default=1.0)
    h = param.NumberField(default=1.0)
    center = param.PointField()
    
    def __deepcopy__(self, memo):
        return Box(
            # elementals=deepcopy(self.elementals),
            # polygon=deepcopy(self.polygon),
            ps_layer=self.ps_layer,
            node_id=deepcopy(self.node_id),
        )

    def create_elementals(self, elems):
        shape = BoxShape(width=self.w, height=self.h)
        shape.apply_merge
        ply = spira.Polygons(shape=shape, gds_layer=self.ps_layer.layer)
        ply.center = self.center
        # if self.pc_transformation is not None:
        #     # print('!!!!!!!!!!!!!!!!!!!!')
        #     ply.transform(transform=self.pc_transformation.apply())
        elems += ply
        return elems
