import gdspy
import spira.all as spira
import numpy as np
from spira.yevon.gdsii.base import __Group__
from spira.yevon.properties.geometry import __GeometryProperties__


class CellProperties(__Group__, __GeometryProperties__):

    __gdspy_cell__ = None
    __gdspy_cell__witout_posts__ = None

    def flat_copy(self, level=-1):
        C = spira.Cell(
            name='{}_{}'.format(self.name, 'flat'),
            elementals=self.elementals.flat_copy(level=level)
        )
        return C

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
                if e.transformation is not None:
                    e = e.transformation.apply_to_object(e)
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
            G = c.commit_to_gdspy(cell=c)
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
        cell = self.__get_gdspy_cell__()
        bbox = cell.get_bounding_box()
        if bbox is None:
            bbox = ((0,0),(0,0))
        return np.array(bbox)


