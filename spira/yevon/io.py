import os
import gdspy
import pathlib
import numpy as np
import spira.all as spira

from spira.yevon.utils.geometry import scale_coord_down as scd
from spira.yevon.utils.geometry import scale_coord_up as scu
from spira.yevon.utils.geometry import scale_polygon_down as spd
from spira.yevon.utils.geometry import scale_polygon_up as spu
from copy import copy, deepcopy
from spira.core.transforms import *

from numpy.linalg import norm
from spira.validatex.lvs.detection import *


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
    """ Move all cell centers to the origin. """

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

        # # T = Translation(midpoint)

        # # # T = t1 + t2
        # # # # T = S.transformation + Translation(translation=origin)

        # # S.midpoint = center + midpoint
        # print(center)
        # print(S.transformation)
        # print(S.reference.elements)
        # # # S.reference.elements.transform(-Translation(center))
        # # t3 = -Translation(center)
        # # for e in S.reference.elements.sref:
        # #     e.midpoint += [-center[0], center[0]]
        # #     # e.midpoint = t3.apply_to_coord(e.midpoint)
        # #     # e.transform(t3)
        # print(S.reference.elements)
        # print('')

        # # S.midpoint.transform(t2)
        # # S.transform(T)

        # c2dmap[cell] += S


# def wrap_references(cell, c2dmap):
#     """ Move all cell centers to the origin. """
#     for e in cell.references:
#         ref_device = deepcopy(c2dmap[e.ref_cell])
#         center = Coord(ref_device.center[0], ref_device.center[1])
#         # ref_device.center = (0,0)
#         D = ref_device.move(midpoint=center, destination=(0,0))

#         point = scu(e.origin)
#         midpoint = Coord(point[0], point[1])
#         S = spira.SRef(reference=D, midpoint=(0,0))

#         if e.x_reflection == True:
#             T = Reflection(reflection=True)
#             center = T.apply_to_coord(center)
#             S.transform(T)

#         if e.rotation is not None:
#             T = Rotation(rotation=e.rotation)
#             center = T.apply_to_coord(center)
#             S.transform(T)

#         m = midpoint + center
#         origin = Coord(m[0], m[1])
        
#         T = Translation(translation=origin)
#         # S.transform(T)
#         S.midpoint = Coord(S.midpoint[0], S.midpoint[1])
#         S.midpoint.transform(T)

#         # if e.rotation is not None:
#         #     # T = Rotation(rotation=e.rotation, center=origin)
#         #     T = Rotation(rotation=e.rotation)
#         #     S.transform(T)
#         #     # S.midpoint.transform(T)

#         c2dmap[cell] += S


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

            # FIXME: Maybe check the datatype.
            for n, p in zip(e.layers, e.polygons):
                layer = spira.Layer(number=n, datatype=0)
                D += spira.Polygon(shape=p, layer=layer)

            # if isinstance(e, gdspy.PolygonSet):
            #     for points in e.polygons:
            #         layer = spira.Layer(number=int(e.layers[0]), datatype=int(e.datatypes[0]))
            #         # D += spira.Polygon(shape=spu([points]), layer=layer)
            #         D += spira.Polygon(shape=spu([points]), layer=layer)
            # elif isinstance(e, gdspy.Polygon):
            #     layer = spira.Layer(number=int(e.layers), datatype=int(e.datatype))
            #     # D += spira.Polygon(shape=spu([e.points]), layer=layer)
            #     D += spira.Polygon(shape=spu([e.points]), layer=layer)

        c2dmap.update({cell:D})
        cell_list.append(cell)

    for cell in cell_list:
        wrap_references(cell, c2dmap)
        # wrap_labels(cell, c2dmap)

    # top_spira_cell = c2dmap[topcell]
    # if flatten == True:
    #     D = spira.Cell(name='import_gds')
    #     return D
    # else:
    #     return top_spira_cell

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






