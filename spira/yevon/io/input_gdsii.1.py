import os
import gdspy
import pathlib
import numpy as np
import spira.all as spira
from copy import copy, deepcopy
from spira.core.transforms import *
from spira.yevon.io.input import BasicInput
from numpy.linalg import norm
# from spira.validatex.lvs.detection import *


class InputGdsii(BasicInput):
    pass


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
            D += spira.Label(position=l.position, text=l.text, layer=spira.Layer(number=l.layer))


def wrap_references(cell, c2dmap):
    """ Move all cell centers to the origin.
    `cell` is of type gdspy.Cell.
    """

    for e in cell.references:
        ref_device = deepcopy(c2dmap[e.ref_cell])
        center = ref_device.center
        D = ref_device.move(midpoint=center, destination=(0,0))

        midpoint = Coord(e.origin[0], e.origin[1])
        S = spira.SRef(reference=D, midpoint=(0,0))

        if e.x_reflection == True:
            T = Reflection(reflection=True)
            center = T.apply_to_coord(center)
            S.transform(T)

        if e.rotation is not None:
            T = Rotation(rotation=e.rotation)
            center = T.apply_to_coord(center)
            S.transform(T)

        midpoint.move(center)
        S.translate(midpoint)

        c2dmap[cell] += S


def import_gds(filename, cellname=None, flatten=False, pcell=True):
    """  """

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

    cell_list = []
    c2dmap = {}
    for cell in gdsii_lib.cell_dict.values():
        D = spira.Cell(name=cell.name)
        for e in cell.polygons:

            # FIXME: Maybe check the datatype and add layer mapping.
            for n, p in zip(e.layers, e.polygons):
                layer = spira.Layer(number=int(n), datatype=0)
                D += spira.Polygon(shape=p, layer=layer)

        c2dmap.update({cell:D})
        cell_list.append(cell)

    for cell in cell_list:
        wrap_references(cell, c2dmap)
        # wrap_labels(cell, c2dmap)

    top_spira_cell = c2dmap[topcell]

    if flatten == True:
        C = spira.Cell(name='import_gds')
    else:
        C = top_spira_cell

    if pcell is True:
        D = parameterize_cell(C)
    else:
        D = C

    return D


def parameterize_cell(cell):
    """ Parameterizes a hand-crafted layout. """

    C = device_detector(cell=cell)
    D = circuit_detector(cell=C)

    return D






