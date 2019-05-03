import os
import spira.all as spira
import gdspy
import pathlib
import numpy as np
from spira.yevon.utils import c3d
from spira.yevon.utils import scale_coord_down as scd
from spira.yevon.utils import scale_coord_up as scu
from spira.yevon.utils import scale_polygon_down as spd
from spira.yevon.utils import scale_polygon_up as spu
from copy import copy, deepcopy
from spira.core.transforms import *

import numpy as np
from numpy.linalg import norm


# def __reflect__(points, p1=(0,0), p2=(1,0)):
#     points = np.array(points); p1 = np.array(p1); p2 = np.array(p2)
#     if np.asarray(points).ndim == 1:
#         t = np.dot((p2-p1), (points-p1))/norm(p2-p1)**2
#         pts = 2*(p1 + (p2-p1)*t) - points
#     if np.asarray(points).ndim == 2:
#         t = np.dot((p2-p1), (p2-p1))/norm(p2-p1)**2
#         pts = np.array([2*(p1 + (p2-p1)*t) - p for p in points])
#     return pts


# def __rotate__(points, angle=45, center=(0,0)):
#     angle = angle*np.pi/180
#     ca = np.cos(angle)
#     sa = np.sin(angle)
#     sa = np.array((-sa, sa))
#     c0 = np.array(center)
#     if np.asarray(points).ndim == 2:
#         pts = (points - c0) * ca + (points - c0)[:,::-1] * sa + c0
#         pts = np.round(pts, 6)
#     if np.asarray(points).ndim == 1:
#         pts = (points - c0) * ca + (points - c0)[::-1] * sa + c0
#         pts = np.round(pts, 6)
#     return pts


def current_path(filename):
    return '{}/{}.gds'.format(os.getcwd(), filename)


def debug_path(filename):
    debug_dir = os.getcwd() + '/debug/'
    pathlib.Path(debug_dir).mkdir(parents=True, exist_ok=True)
    path = debug_dir + filename + '.gds'
    return path


def map_references(c, c2dmap):
    for e in c.elementals.sref:
        if e.ref in c2dmap.keys():
            e.ref = c2dmap[e.ref]
            e._parent_ports = e.ref.ports
            e._local_ports = {(port.name, port.gds_layer.number, port.midpoint[0], port.midpoint[1]):deepcopy(port) for port in e.ref.ports}
            e.port_locks = {(port.name, port.gds_layer.number, port.midpoint[0], port.midpoint[1]):port.locked for port in e.ref.ports}
            # e._local_ports = {port.node_id:deepcopy(port) for port in e.ref.ports}
            # e.port_locks = {port.node_id:port.locked for port in e.ref.ports}


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
            print(ref_device.center)
            ref_device.center = (0,0)
            # ref_device.move(midpoint=center, destination=(0,0))
            print('origin center: {}'.format(ref_device.center))
            print('')

            point = scu(e.origin)
            midpoint = Coord(point[0], point[1])
            S = spira.SRef(reference=ref_device, midpoint=(0,0))

            if e.x_reflection == True:
                T = Reflection(reflection=True)
                center = T.apply_to_coord(center)
                S.transform(T)

            if e.rotation is not None:
                angle = e.rotation
                T = Rotation(rotation=angle)
                center = T.apply_to_coord(center)
                S.transform(T)

            # origin = Coord(center[0], center[1])
            # m = midpoint
            # m = center
            m = midpoint + center
            # m = midpoint - center
            origin = Coord(m[0], m[1])

            T = Translation(translation=origin)
            S.transform(T)
            print(S.transformation)

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


def import_gds(filename, cellname=None, flatten=False, dups_layer={}):
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

    cell_list = spira.ElementList()
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
        wrap_labels(cell, c2dmap)

    top_spira_cell = c2dmap[topcell]
    if flatten == True:
        D = spira.Cell(name='import_gds')
        return D
    else:
        return top_spira_cell






