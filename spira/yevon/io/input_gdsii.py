import os
import gdspy
import pathlib
import numpy as np
from numpy.linalg import norm
import spira.all as spira
from copy import copy, deepcopy
from spira.core.transforms import *
from spira.yevon.io.input import InputBasic


__all__ = ['InputGdsii']


class InputGdsii(InputBasic):
    """  """

    def __init__(self, file_name, **kwargs):
        if file_name is None:
            raise ValueError('No GDSII file name specified.')
        super().__init__(file_name=file_name, **kwargs)

    def parse(self):

        gdsii_lib = gdspy.GdsLibrary(name='SPiRA-cell')
        gdsii_lib.read_gds(self.file_name)
        top_level_gdspy_cells = gdsii_lib.top_level()

        if self.cell_name is not None:
            if self.cell_name not in gdsii_lib.cell_dict:
                error_message = "[SPiRA] import_gds() The requested gdspy_cell (named {}) is not present in file {}"
                raise ValueError(error_message.format(self.cell_name, self.file_name))
            topgdspy_cell = gdsii_lib.cell_dict[self.cell_name]
        elif self.cell_name is None and len(top_level_gdspy_cells) == 1:
            topgdspy_cell = top_level_gdspy_cells[0]
        elif self.cell_name is None and len(top_level_gdspy_cells) > 1:
            # TODO: Add this to logger.
            print('Multiple toplevel gdspy_cells found:')
            for gdspy_cell in top_level_gdspy_cells:
                print(gdspy_cell)
            raise ValueError('[SPiRA] import_gds() There are multiple' +
                            'top-level gdspy_cells, you must specify self.cell_name' +
                            'to select of one of them')

        c2dmap = {}
        for gdspy_cell in gdsii_lib.cell_dict.values():
            D = spira.Cell(name=gdspy_cell.name)
            for e in gdspy_cell.polygons:

                for i, p in enumerate(e.polygons):
                    n = e.layers[i]
                    d = e.datatypes[i]
                    # print(n, d)
                    layer = spira.Layer(number=int(n), datatype=int(d))
                    L = self.map_layer(layer)
                    # print(L)
                    # D += spira.Polygon(shape=p, layer=L)
                    ply = spira.Polygon(shape=p, layer=L)
                    # print(ply)
                    D += ply

                # print(e.datatypes)

                # key = (e.layer)

                # # FIXME: Maybe check the datatype and add layer mapping.
                # for n, p in zip(e.layers, e.polygons):
                #     layer = spira.Layer(number=int(n), datatype=int(0))
                #     L = self.map_layer(layer)
                #     D += spira.Polygon(shape=p, layer=L)

            c2dmap.update({gdspy_cell: D})

        for gdspy_cell in gdsii_lib.cell_dict.values():
            self._create_references(gdspy_cell, c2dmap)
            # self._create_labels(gdspy_cell, c2dmap)

        return c2dmap[topgdspy_cell]

    def _create_references(self, gdspy_cell, c2dmap):
        """ Move all gdspy_cell centers to the origin. """

        for e in gdspy_cell.references:
            ref_device = deepcopy(c2dmap[e.ref_cell])
            center = ref_device.center
            # print(e)
            # print(center)
            D = ref_device.move(midpoint=center, destination=(0,0))

            midpoint = Coord(e.origin[0], e.origin[1])
            S = spira.SRef(reference=D, midpoint=(0,0))

            # FIXME: Reflection still causes errors.
            if e.x_reflection == True:
                T = Reflection(reflection=True)
                center = T.apply_to_coord(center)
                S.transform(T)

            if e.rotation is not None:
                T = Rotation(rotation=e.rotation)
                center = T.apply_to_coord(center)
                S.transform(T)

            # midpoint.move(center)
            midpoint.translate(center)
            S.translate(midpoint)

            c2dmap[gdspy_cell] += S

    def _create_labels(self, gdspy_cell, c2dmap):
        for l in gdspy_cell.get_labels():
            D = c2dmap[gdspy_cell]
            if isinstance(l, gdspy.Label):
                D += spira.Label(position=l.position, text=l.text, layer=spira.Layer(number=l.layer))

