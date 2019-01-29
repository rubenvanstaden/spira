import os
import spira
import gdspy
import pathlib
import numpy as np
from spira.gdsii.utils import c3d
from spira.gdsii.utils import scale_coord_down as scd
from spira.gdsii.utils import scale_coord_up as scu
from spira.gdsii.utils import scale_polygon_down as spd
from spira.gdsii.utils import scale_polygon_up as spu
from spira import LOG


def current_path(filename):
    return '{}/{}.gds'.format(os.getcwd(), filename)


def debug_path(filename):
    debug_dir = os.getcwd() + '/debug/'
    pathlib.Path(debug_dir).mkdir(parents=True, exist_ok=True)
    path = debug_dir + filename + '.gds'
    return path


def wrap_labels(cell, c2dmap):
    for l in cell.get_labels():
        D = c2dmap[cell]
        if isinstance(l, gdspy.Label):
            D += spira.Label(
                position=scu(l.position),
                text=l.text,
                gdslayer=spira.Layer(number=l.layer),
                str_anchor=l.anchor
            )


def wrap_references(cell, c2dmap):
    """ Move all cell centers to the origin. """
    for e in cell.elements:
        if isinstance(e, gdspy.CellReference):
            D = c2dmap[cell]
            ref_device = c2dmap[e.ref_cell]
            o = ref_device.center
            ref_device.move(midpoint=o, destination=(0,0))

            if e.rotation is None:
                e.rotation = 0

            S = spira.SRef(structure=ref_device)

            pos = [0, 0]

            # Q1
            if (o[0] >= 0) and (o[1] > 0):
                pos = -o
            # Q2
            elif (o[0] < 0) and (o[1] >= 0):
                pos = o
            # Q3
            elif (o[0] <= 0) and (o[1] < 0):
                pos = -o
            # Q4
            elif (o[0] > 0) and (o[1] <= 0):
                pos = o

            tf = {
                'midpoint': scu(e.origin) + pos,
                'rotation': e.rotation,
                'magnification': e.magnification,
                'reflection': e.x_reflection
            }

            S.transform(tf)
            D += S


def import_gds(filename, cellname=None, flatten=False, duplayer={}):
    """  """

    LOG.header('Imported GDS file -> \'{}\''.format(filename))

    gdsii_lib = gdspy.GdsLibrary(name='SPiRA-Cell')
    gdsii_lib.read_gds(filename)
    top_level_cells = gdsii_lib.top_level()

    if cellname is not None:
        if cellname not in gdsii_lib.cell_dict:
            raise ValueError("[SPiRA] import_gds() The requested cell " +
                             "(named {}) is not present in file {}".format(cellname, filename))
        topcell = gdsii_lib.cell_dict[cellname]
    elif cellname is None and len(top_level_cells) == 1:
        topcell = top_level_cells[0]
    elif cellname is None and len(top_level_cells) > 1:

        # TODO: Add this to logger.
        print('Multiple toplevel cells found:')
        for cell in top_level_cells:
            print(cell)

        raise ValueError('[SPiRA] import_gds() There are multiple' +
                         'top-level cells, you must specify cellname' +
                         'to select of one of them')

    cell_list = spira.ElementList()
    c2dmap = {}
    for cell in gdsii_lib.cell_dict.values():
        D = spira.Cell(name=cell.name)
        for e in cell.elements:
            if isinstance(e, gdspy.PolygonSet):
                for points in e.polygons:
                    layer = spira.Layer(number=e.layers[0], datatype=e.datatypes[0])
                    D += spira.Polygons(shape=spu([points]), gdslayer=layer)
            elif isinstance(e, gdspy.Polygon):
                layer = spira.Layer(number=e.layers, datatype=e.datatype)
                D += spira.Polygons(shape=spu([e.points]), gdslayer=layer)
        c2dmap.update({cell:D})
        cell_list += cell

    for cell in cell_list:
        wrap_references(cell, c2dmap)
        wrap_labels(cell, c2dmap)

    top_spira_cell = c2dmap[topcell]
    if flatten == True:
        D = spira.Cell(name='import_gds')
        return D
    else:
        return top_spira_cell






