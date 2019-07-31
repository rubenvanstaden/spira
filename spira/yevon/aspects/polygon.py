import gdspy
import hashlib
import numpy as np

from spira.yevon.utils import clipping
from spira.yevon.gdsii.polygon import Polygon
from spira.yevon.gdsii.elem_list import ElementList
from spira.yevon.aspects.clipper import __ClipperAspects__
from spira.yevon.aspects.geometry import __GeometryAspects__
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


class PolygonAspects(__GeometryAspects__):
    pass


class PolygonClipperAspects(__ClipperAspects__):
    """

    """

    def __and__(self, other):
        if self.layer == other.layer:
            s1 = self.shape.transform_copy(self.transformation)
            s2 = other.shape.transform_copy(other.transformation)
            shapes = s1.__and__(s2)
            elems = [Polygon(shape=s, layer=self.layer) for s in shapes]
            return elems
        return ElementList([])

    def __sub__(self, other):
        if self.layer == other.layer:
            s1 = self.shape.transform_copy(self.transformation)
            s2 = other.shape.transform_copy(other.transformation)
            shapes = s1.__sub__(s2)
            elems = [Polygon(shape=s, layer=self.layer) for s in shapes]
            return elems
        return ElementList([self])

    def __or__(self, other):
        if self.layer == other.layer:
            s1 = self.shape.transform_copy(self.transformation)
            s2 = other.shape.transform_copy(other.transformation)
            shapes = s1.__or__(s2)
            elems = [Polygon(shape=s, layer=self.layer) for s in shapes]
            return elems
        return ElementList([self, other])

    # NOTE: Does not require to check for layer equivalence.
    def intersection(self, other):
        from copy import deepcopy
        s1 = self.shape.transform_copy(self.transformation)
        s2 = other.shape.transform_copy(other.transformation)
        shapes = s1.__and__(s2)
        elems = [Polygon(shape=s, layer=self.layer) for s in shapes]
        return elems

