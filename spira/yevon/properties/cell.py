import gdspy
import numpy as np
import spira.all as spira

from copy import deepcopy
from spira.yevon.gdsii.group import __Group__
from spira.yevon.geometry.coord import Coord
from spira.yevon.properties.geometry import __GeometryProperties__


class CellProperties(__Group__, __GeometryProperties__):

    _cid = 0

    __gdspy_cell__ = None

    def get_gdspy_cell(self):
        # if self.__gdspy_cell__ is None:
        #     self.set_gdspy_cell()
        self.set_gdspy_cell()
        return self.__gdspy_cell__

    def set_gdspy_cell(self):
        name = '{}_{}'.format(self.name, CellProperties._cid)
        CellProperties._cid += 1
        glib = gdspy.GdsLibrary(name=name)
        cell = spira.Cell(name=name, elementals=deepcopy(self.elementals))
        # cell = spira.Cell(name=self.name, elementals=self.elementals)
        self.__gdspy_cell__ = cell.construct_gdspy_tree(glib)

    def convert_references(self, c, c2dmap):
        # for e in c.elementals:
        for e in c.elementals.flat_elems():
            G = c2dmap[c]
            if isinstance(e, spira.SRef):

                # if not isinstance(e.midpoint, Coord):
                #     e.midpoint = Coord(e.midpoint[0], e.midpoint[1])

                # FIXME: Has to be removed for layout transformations.
                T = e.transformation
                # T = e.transformation + spira.Translation(e.midpoint)
                e.midpoint = T.apply_to_coord(e.midpoint)

                ref = gdspy.CellReference(
                    ref_cell=c2dmap[e.ref],
                    origin=e.midpoint.to_numpy_array(),
                    rotation=e.rotation,
                    magnification=e.magnification,
                    x_reflection=e.reflection
                )

                # T = e._translation
                # ref.translate(dx=T[0], dy=T[1])

                G.add(ref)

    def construct_gdspy_tree(self, glib):
        d = self.dependencies()
        c2dmap = {}
        for c in d:
            G = c.commit_to_gdspy(cell=c)
            c2dmap.update({c:G})
        for c in d:
            self.convert_references(c, c2dmap)
            if c.name not in glib.cell_dict.keys():
                glib.add(c2dmap[c])
        return c2dmap[self]

    @property
    def bbox(self):
        D = deepcopy(self)
        cell = D.get_gdspy_cell()
        bbox = cell.get_bounding_box()
        if bbox is None:
            bbox = ((0,0),(0,0))
        return np.array(bbox)


