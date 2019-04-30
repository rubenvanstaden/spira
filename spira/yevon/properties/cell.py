import gdspy
import spira.all as spira
import numpy as np
from spira.yevon.gdsii.base import __Group__
from spira.yevon.properties.geometry import __GeometryProperties__
from spira.yevon.geometry.coord import Coord


class CellProperties(__Group__, __GeometryProperties__):

    __gdspy_cell__ = None

    def get_gdspy_cell(self):
        if self.__gdspy_cell__ is None:
            self.set_gdspy_cell()
        return self.__gdspy_cell__

    def set_gdspy_cell(self):
        glib = gdspy.GdsLibrary(name=self.name)
        cell = spira.Cell(name=self.name, elementals=self.elementals)
        self.__gdspy_cell__ = cell.construct_gdspy_tree(glib)

    def convert_references(self, c, c2dmap):
        for e in c.elementals.flat_elems():
            G = c2dmap[c]
            if isinstance(e, spira.SRef):
                # if e.transformation is None:
                #     tf = spira.Translation(e.midpoint) 
                # else:
                #     tf = e.transformation + spira.Translation(e.midpoint)
                # T = e.transformation

                # print('\n--- Convert Ref ---')
                # print(tf)
                # print(type(tf))
                # print('--------------------\n')
                # if tf is not None:
                #     e = tf.appl
                # print(e)
                # if not isinstance(e.midpoint, Coord):
                #     raise ValueError('Not Coord')
                #     # e.midpoint = e.midpoint.convert_to_array()
                
                if isinstance(e.midpoint, Coord):
                    origin = e.midpoint.convert_to_array()

                # if not isinstance(e.midpoint, Coord):
                #     e.midpoint = Coord(e.midpoint[0], e.midpoint[1])
    
                # T = spira.Translation(e.midpoint)

                # if T is not None:
                #     origin = T(e.midpoint)
                #     origin = origin.convert_to_array()
                # else:
                #     origin = e.midpoint.convert_to_array()

                G.add(
                    gdspy.CellReference(
                        ref_cell=c2dmap[e.ref],
                        origin=origin,
                        # origin=e.midpoint,
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
        cell = self.get_gdspy_cell()
        bbox = cell.get_bounding_box()
        if bbox is None:
            bbox = ((0,0),(0,0))
        return np.array(bbox)


