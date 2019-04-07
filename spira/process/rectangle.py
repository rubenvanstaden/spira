import spira
import numpy as np
from copy import deepcopy
from spira.core import param
from spira import shapes
from spira.process.processlayer import ProcessLayer


class Rectangle(ProcessLayer):

    p1 = param.PointField(default=(0,0))
    p2 = param.PointField(default=(2,2))
    
    def __deepcopy__(self, memo):
        return Rectangle(
            # elementals=deepcopy(self.elementals),
            # polygon=deepcopy(self.polygon),
            ps_layer=self.ps_layer,
            node_id=deepcopy(self.node_id),
        )

    def create_elementals(self, elems):
        shape = shapes.RectangleShape(p1=self.p1, p2=self.p2)
        shape.apply_merge
        ply = spira.Polygons(shape=shape, gds_layer=self.ps_layer.layer)
        # if self.pc_transformation is not None:
        #     ply.transform(transform=self.pc_transformation.apply())
        elems += ply
        return elems
