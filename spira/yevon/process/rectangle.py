import spira.all as spira
import numpy as np
from copy import deepcopy
from spira.yevon.geometry import shapes
from spira.yevon.process.processlayer import ProcessLayer

from spira.yevon.geometry.coord import CoordField


class Rectangle(ProcessLayer):
    """

    Example
    -------
    >>> p = pc.Rectangle(p1=(0,0), p2=(10,0), ps_layer=RDD.PLAYER.M6)
    >>> [SPiRA: Rectangle] ()
    """

    p1 = CoordField(default=(0,0))
    p2 = CoordField(default=(2,2))
    
    def create_elementals(self, elems):
        self.shape = shapes.RectangleShape(p1=self.p1, p2=self.p2)
        elems += spira.Polygon(shape=self.shape, gds_layer=self.ps_layer.layer)
        return elems
        