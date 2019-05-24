import os
import spira.all as spira
import gdspy
import pathlib
import numpy as np
from spira.yevon.utils.geometry import c3d
from spira.yevon.utils.geometry import scale_coord_down as scd
from spira.yevon.utils.geometry import scale_coord_up as scu
from spira.yevon.utils.geometry import scale_polygon_down as spd
from spira.yevon.utils.geometry import scale_polygon_up as spu
from copy import copy, deepcopy
from spira.core.transforms import *

import numpy as np
from numpy.linalg import norm
from spira.validatex.lvs.detection import *


def current_path(filename):
    return '{}/{}.gds'.format(os.getcwd(), filename)


def debug_path(filename):
    debug_dir = os.getcwd() + '/debug/'
    pathlib.Path(debug_dir).mkdir(parents=True, exist_ok=True)
    path = debug_dir + filename + '.gds'
    return path


# def map_references(c, c2dmap):
#     for e in c.elementals.sref:
#         if e.ref in c2dmap.keys():
#             e.ref = c2dmap[e.ref]
#             e._parent_ports = e.ref.ports
#             e._local_ports = {(port.name, port.gds_layer.number, port.midpoint[0], port.midpoint[1]):deepcopy(port) for port in e.ref.ports}
#             e.port_locks = {(port.name, port.gds_layer.number, port.midpoint[0], port.midpoint[1]):port.locked for port in e.ref.ports}
#             # e._local_ports = {port.node_id:deepcopy(port) for port in e.ref.ports}
#             # e.port_locks = {port.node_id:port.locked for port in e.ref.ports}


def wrap_labels(cell, c2dmap):
    for l in cell.get_labels():
        D = c2dmap[cell]
        if isinstance(l, gdspy.Label):
            D += spira.Label(
                position=scu(l.position),
                text=l.text,
                gds_layer=spira.Layer(number=int(l.layer))
            )


def wrap_references(cell, c2dmap):
    """ Move all cell centers to the origin. """
    for e in cell.elements:
        if isinstance(e, gdspy.CellReference):
            ref_device = deepcopy(c2dmap[e.ref_cell])
            center = Coord(ref_device.center[0], ref_device.center[1])
            # ref_device.center = (0,0)
            D = ref_device.move(midpoint=center, destination=(0,0))

            point = scu(e.origin)
            midpoint = Coord(point[0], point[1])
            S = spira.SRef(reference=D, midpoint=(0,0))

            if e.x_reflection == True:
                T = Reflection(reflection=True)
                center = T.apply_to_coord(center)
                S.transform(T)

            if e.rotation is not None:
                T = Rotation(rotation=e.rotation)
                center = T.apply_to_coord(center)
                S.transform(T)

            m = midpoint + center
            origin = Coord(m[0], m[1])
            
            T = Translation(translation=origin)
            # S.transform(T)
            S.midpoint = Coord(S.midpoint[0], S.midpoint[1])
            S.midpoint.transform(T)

            # if e.rotation is not None:
            #     # T = Rotation(rotation=e.rotation, center=origin)
            #     T = Rotation(rotation=e.rotation)
            #     S.transform(T)
            #     # S.midpoint.transform(T)

            c2dmap[cell] += S


# def wrap_references(cell, c2dmap):
#     """ Move all cell centers to the origin. """
#     for e in cell.elements:
#         if isinstance(e, gdspy.CellReference):
#             ref_device = deepcopy(c2dmap[e.ref_cell])
#             center = ref_device.center
#             ref_device.move(midpoint=center, destination=(0,0))

#             midpoint = np.array(scu(e.origin))
#             S = spira.SRef(structure=ref_device)

#             if e.x_reflection == True:
#                 center = __reflect__(points=center)
#             if e.rotation is not None:
#                 center = __rotate__(points=center, angle=e.rotation)

#             tf = {
#                 'midpoint': midpoint + center,
#                 'rotation': e.rotation,
#                 'magnification': e.magnification,
#                 'reflection': e.x_reflection
#             }

#             S.transform(tf)
#             c2dmap[cell] += S


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

    cell_list = spira.ElementalList()
    c2dmap = {}
    for cell in gdsii_lib.cell_dict.values():
        D = spira.Cell(name=cell.name)
        for e in cell.elements:
            if isinstance(e, gdspy.PolygonSet):
                for points in e.polygons:
                    layer = spira.Layer(number=int(e.layers[0]), datatype=int(e.datatypes[0]))
                    D += spira.Polygon(shape=spu([points]), gds_layer=layer)
            elif isinstance(e, gdspy.Polygon):
                layer = spira.Layer(number=int(e.layers), datatype=int(e.datatype))
                D += spira.Polygon(shape=spu([e.points]), gds_layer=layer)
        c2dmap.update({cell:D})
        cell_list += cell

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






