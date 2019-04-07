import gdspy
import spira
import numpy as np
from copy import deepcopy
from spira.core.elem_list import ElementList
from spira.utils import scale_polygon_down as spd
from spira.utils import scale_polygon_up as spu
from spira.utils import scale_coord_down as scd


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
    def dx(self):
        return (self.xmax - self.xmin)

    @property
    def dy(self):
        return (self.ymax - self.ymin)

    @property
    def pbox(self):
        (a,b), (c,d) = self.bbox
        points = [[[a,b], [c,b], [c,d], [a,d]]]
        return points

    @property
    def center(self):
        return np.sum(self.bbox, 0)/2
    
    @center.setter
    def center(self, destination):
        self.move(destination=destination, midpoint=self.center)

    @property
    def xpos(self):
        return self.center[0]

    @property
    def ypos(self):
        return self.center[1]


class PolygonMixin(__Properties__):

    @property
    def points(self):
        return self.shape.points

    @property
    def ply_area(self):
        ply = gdspy.PolygonSet(self.shape.points, verbose=False)
        return ply.area()

    @property
    def bbox(self):
        self.polygons = np.array(self.points)
        return self.get_bounding_box()


class CellMixin(__Properties__):

    __gdspy_cell__ = None
    __gdspy_cell__witout_posts__ = None

    def __get_gdspy_cell__(self):
        # TODO: Test gdspy cell here.
        if self.__gdspy_cell__ is None:
            self.__set_gdspy_cell__()
        return self.__gdspy_cell__

    def __set_gdspy_cell__(self):
        glib = gdspy.GdsLibrary(name=self.name)
        cell = spira.Cell(name=self.name, elementals=self.elementals)
        self.__gdspy_cell__ = cell.construct_gdspy_tree(glib)

    def __set_gdspy_cell_withut_ports__(self):
        glib = gdspy.GdsLibrary(name=self.name)
        cell = deepcopy(self)
        # self.__gdspy_cell__witout_posts__ = cell.construct_gdspy_tree(glib)
        self.__gdspy_cell__ = cell.construct_gdspy_tree(glib)

    def __wrapper__(self, c, c2dmap):
        for e in c.elementals.flat_elems():
            G = c2dmap[c]
            if isinstance(e, spira.SRef):
                G.add(
                    gdspy.CellReference(
                        ref_cell=c2dmap[e.ref],
                        origin=e.midpoint,
                        rotation=e.rotation,
                        magnification=e.magnification,
                        x_reflection=e.reflection
                    )
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
        # cell = self.__set_gdspy_cell_withut_ports__()
        cell = self.__get_gdspy_cell__()
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

