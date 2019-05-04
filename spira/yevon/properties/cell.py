import gdspy
import spira.all as spira
import numpy as np
from copy import deepcopy
from spira.yevon.gdsii.base import __Group__
from spira.yevon.properties.geometry import __GeometryProperties__
from spira.yevon.geometry.coord import Coord


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
        # print(name)
        glib = gdspy.GdsLibrary(name=name)
        cell = spira.Cell(name=name, elementals=deepcopy(self.elementals))
        # cell = spira.Cell(name=self.name, elementals=self.elementals)
        self.__gdspy_cell__ = cell.construct_gdspy_tree(glib)

    def convert_references(self, c, c2dmap):
        for e in c.elementals.flat_elems():
            G = c2dmap[c]
            if isinstance(e, spira.SRef):

                if not isinstance(e.midpoint, Coord):
                    e.midpoint = Coord(e.midpoint[0], e.midpoint[1])

                # if e.transformation is None:
                #     tf = spira.Translation(e.midpoint) 
                # else:
                #     tf = e.transformation + spira.Translation(e.midpoint)

                # tf = e.transformation
                # if tf is not None:
                #     e.midpoint = tf.apply_to_coord(e.midpoint)

                if isinstance(e.midpoint, Coord):
                    origin = e.midpoint.convert_to_array()
                else:
                    origin = e.midpoint

                G.add(
                    gdspy.CellReference(
                        ref_cell=c2dmap[e.ref],
                        origin=origin,
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
            self.convert_references(c, c2dmap)
            if c.name not in glib.cell_dict.keys():
                glib.add(c2dmap[c])
        return c2dmap[self]

    @property
    def bbox(self):
        D = deepcopy(self)
        D.name = '{}_copy'.format(D.name)
        cell = D.get_gdspy_cell()

        # print(cell)
        # for e in cell.elements:
        #     print(e)

        bbox = cell.get_bounding_box()
        if bbox is None:
            bbox = ((0,0),(0,0))
        return np.array(bbox)


