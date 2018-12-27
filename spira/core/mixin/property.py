import gdspy
import numpy as np
from spira.core.lists import ElementList


class __Properties__(object):

    @property
    def xmax(self):
        return self.bbox[1][0]

    @property
    def ymax(self):
        return self.bbox[1][1]

    @property
    def xmin(self):
        return self.bbox[0][0]

    @property
    def ymin(self):
        return self.bbox[0][1]

    @property
    def center(self):
        return np.sum(self.bbox, 0)/2


class CellMixin(__Properties__):

    @property
    def bbox(self):
        bbox = self.get_bounding_box()
        if bbox is None:  bbox = ((0,0),(0,0))
        return np.array(bbox)

    @property
    def terms(self):
        from spira.gdsii.elemental.term import Term
        terms = ElementList()
        for p in self.ports:
            if isinstance(p, Term):
                terms += p
        return terms

    @property
    def term_ports(self):
        from spira.gdsii.elemental.term import Term
        terms = {}
        for p in self.ports:
            if isinstance(p, Term):
                terms[p.name] = p
        return terms


class PolygonMixin(__Properties__):

    @property
    def points(self):
        return self.shape.points

    @property
    def ply_area(self):
        ply = gdspy.PolygonSet(self.shape.points)
        return ply.area()

    @property
    def bbox(self):
        # self.polygons = self.points
        bb = self.get_bounding_box()
        assert len(bb) == 2
        return bb

