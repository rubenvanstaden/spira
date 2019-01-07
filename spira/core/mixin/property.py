import gdspy
import spira
import numpy as np
from copy import deepcopy
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
    
    @center.setter
    def center(self, destination):
        self.move(destination=destination, midpoint=self.center)


class CellMixin(__Properties__):

    def __wrapper__(self, c, c2dmap):
        for e in c.elementals.flat_elems():
            G = c2dmap[c]
            if isinstance(e, spira.SRef):
                G.add(gdspy.CellReference(
                    ref_cell=c2dmap[e.ref],
                    midpoint=e.midpoint,
                    rotation=e.rotation,
                    magnification=e.magnification,
                    x_reflection=e.reflection)
                )

    def construct_gdspy_tree(self, glib):
        d = self.dependencies()
        c2dmap = {}
        for c in d:
            G = c.commit_to_gdspy()
            c2dmap.update({c:G})
        for c in d:
            self.__wrapper__(c, c2dmap)
            if c.name not in glib.cell_dict.keys():
                glib.add(c2dmap[c])
        for p in self.get_ports():
            p.commit_to_gdspy(cell=c2dmap[self])
        return c2dmap[self]

    @property
    def bbox(self):
        glib = gdspy.GdsLibrary(name=self.name)
        cell = deepcopy(self)
        cell = self.construct_gdspy_tree(glib)
        bbox = cell.get_bounding_box()
        if bbox is None:
            bbox = ((0,0),(0,0))
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

    @property
    def center(self):
        c = np.sum(self.bbox, 0)/2
        c = np.around(c, decimals=0)
        # c = np.around(c, decimals=3)
        return c

    @center.setter
    def center(self, destination):
        self.move(destination=destination, midpoint=self.center)


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

