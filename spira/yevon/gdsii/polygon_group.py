import gdspy

from copy import deepcopy
from spira.yevon.utils import clipping
from spira.yevon.gdsii.group import Group
from spira.yevon.gdsii.polygon import Polygon
from spira.yevon.gdsii.elem_list import ElementalList
from spira.yevon.gdsii.base import __LayerElemental__
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = ['PolygonGroup']


class PolygonGroup(Group, __LayerElemental__):
    """ 
    Collection of polygon elementals. Boolean
    operation can be applied on these polygons.

    Example
    -------
    >>> cp = spira.PolygonGroup()
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)       

    def __repr__(self):
        class_string = "[SPiRA: PolygonGroup] (polygons {}, process {}, purpose {})"
        return class_string.format(self.count, self.process, self.purpose)

    def __str__(self):
        return self.__repr__()

    def __and__(self, other):
        el = ElementalList()
        for e1 in self.elementals:
            for e2 in other.elementals:
                e1 = deepcopy(e1)
                e2 = deepcopy(e2)
                if e1.shape != e2.shape:
                    polygons = e1.intersection(e2)
                    for p in polygons:
                        p.layer.purpose = RDD.PURPOSE.INTERSECTED
                    for p in polygons:
                        el += p
        self.elementals = el
        return self

    def __xor__(self, other):
        pts1, pts2 = [], []
        for e in self.elementals:
            s1 = e.shape.transform_copy(e.transformation)
            pts1.append(s1.points)
        for e in other.elementals:
            s1 = e.shape.transform_copy(e.transformation)
            pts2.append(s1.points)

        if (len(pts1) > 0) and (len(pts2) > 0):
            p1 = gdspy.PolygonSet(polygons=pts1)
            p2 = gdspy.PolygonSet(polygons=pts2)
    
            ply = gdspy.fast_boolean(p1, p2, operation='not')
            elems = ElementalList()
            for points in ply.polygons:
                elems += Polygon(shape=points, layer=self.layer)
            self.elementals = elems
        return self

    def __or__(self, other):
        raise ValueError('Not Implemented!')

    @property
    def intersect(self):
        elems = ElementalList()
        el1 = deepcopy(self.elementals)
        el2 = deepcopy(self.elementals)
        for i, e1 in enumerate(el1):
            for j, e2 in enumerate(el2):
                if e1.shape != e2.shape:
                    # polygons = e1.intersection(e2)
                    polygons = e1 & e2
                    for p in polygons:
                        p.layer.purpose = RDD.PURPOSE.INTERSECTED
                    for p in polygons:
                        elems += p
        self.elementals = elems
        return self

    @property
    def merge(self):
        elems = ElementalList()
        if len(self.elementals) > 1:
            points = []
            for e in self.elementals:
                shape = e.shape.transform(e.transformation)
                points.append(shape.points)
            merged_points = clipping.boolean(subj=points, clip_type='or')
            for uid, pts in enumerate(merged_points):
                elems += Polygon(shape=pts, layer=self.layer)
        else:
            elems = self.elementals
        self.elementals = elems
        return self

    @property
    def count(self):
        return len(self.elementals)

    @property
    def process(self):
        layer = RDD.GDSII.IMPORT_LAYER_MAP[self.layer]
        return layer.process

    @property
    def purpose(self):
        layer = RDD.GDSII.IMPORT_LAYER_MAP[self.layer]
        return layer.purpose

    @property
    def center(self):
        return self.bbox_info.center




