import gdspy
import numpy as np

from spira.yevon.utils import clipping
from spira.yevon.gdsii.polygon import Polygon
from spira.yevon.gdsii.elem_list import ElementalList
from spira.yevon.aspects.clipper import __ClipperAspects__
from spira.yevon.aspects.geometry import __GeometryAspects__


class PolygonAspects(__GeometryAspects__):
    """

    Examples
    --------
    """

    @property
    def points(self):
        return self.shape.points

    @property
    def area(self):
        return gdspy.Polygon(self.shape.points).area()

    @property
    def bbox(self):
        return self.bbox_info.bounding_box()


class PolygonClipperAspects(__ClipperAspects__):
    """

    Examples
    --------
    """

    def __and__(self, other):
        if self.layer == other.layer:
            shapes = self.shape.__and__(other.shape)
            elems = [Polygon(shape=s, layer=self.layer) for s in shapes]
            return elems
        return ElementalList([])

    def __sub__(self, other):
        if self.layer == other.layer:
            shapes = self.shape.__sub__(other.shape)
            elems = [Polygon(shape=s, layer=self.layer) for s in shapes]
            return elems
        return ElementalList([self])

    def __or__(self, other):
        if self.layer == other.layer:
            shapes = self.shape.__or__(other.shape)
            elems = [Polygon(shape=s, layer=self.layer) for s in shapes]
            return elems
        return ElementalList([self, other])

