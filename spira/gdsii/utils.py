import math
import spira
import pyclipper
import numpy as np

from spira.settings import SCALE_DOWN, SCALE_UP


st = pyclipper.scale_to_clipper
sf = pyclipper.scale_from_clipper


def get_purpose_layers(cell, players):
    elems = spira.ElementList()
    for ply in cell.elementals.polygons:
        for phys in players:
            if ply.gdslayer == phys.layer:
                elems += ply
    return elems


def bool_operation(subj, clip=None, method=None, closed=True):
    """ Angusj clipping library """

    from spira.gdsii.elemental.polygons import PolygonAbstract

    scale = 1

    pc = pyclipper.Pyclipper()

    if issubclass(type(subj), PolygonAbstract):
        subj = subj.polygons
    if issubclass(type(clip), PolygonAbstract):
        clip = clip.polygons

    if clip is not None:
        pc.AddPaths(st(clip, scale), pyclipper.PT_CLIP, True)
    pc.AddPaths(st(subj, scale), pyclipper.PT_SUBJECT, closed)

    subj = None
    if method == 'difference':
        subj = pc.Execute(pyclipper.CT_DIFFERENCE,
                          pyclipper.PFT_NONZERO,
                          pyclipper.PFT_NONZERO)
    elif method == 'union':
        subj = pc.Execute(pyclipper.CT_UNION,
                          pyclipper.PFT_NONZERO,
                          pyclipper.PFT_NONZERO)
    elif method == 'intersection':
        subj = pc.Execute(pyclipper.CT_INTERSECTION,
                          pyclipper.PFT_NONZERO,
                          pyclipper.PFT_NONZERO)
    elif method == 'exclusive':
        subj = pc.Execute(pyclipper.CT_XOR,
                          pyclipper.PFT_NONZERO,
                          pyclipper.PFT_NONZERO)
    else:
        raise ValueError('Please specify a clipping method')

    sp = pyclipper.SimplifyPolygons(subj)
#     cp = pyclipper.CleanPolygons(sf(sp, scale))
    return sp


def offset_operation(layer, size):
    """
    Apply polygon offsetting using Angusj.
    Either blow up polygons or blow it down.
    """

    pco = pyclipper.PyclipperOffset()
    pco.AddPath(layer, pyclipper.JT_ROUND, pyclipper.ET_CLOSEDPOLYGON)

    if size == 'down':
        return pco.Execute(-10000)[0]
    elif size == 'up':
        return pco.Execute(10.0)
    else:
        raise ValueError('please select the Offset function to use')


def point_inside(points, position):
    assert position is not None, 'No label position found.'
    if pyclipper.PointInPolygon(position, points) != 0:
        return True
    return False


def labeled_polygon_id(position, polygons):
    for i, spira_polygon in enumerate(polygons):
        for j, points in enumerate(spira_polygon.polygons):
            if point_inside(points, position):
                # return (i, j)
                return spira_polygon.id
    return None


def _grids_per_unit():
    return (utils.unit/utils.grid) * utils.um


def _points_to_float(points):
    layer = np.array(points).tolist()

    polygons = []
    for pl in layer:
        poly = [[float(y) for y in x] for x in pl]
        polygons.append(poly)
    return polygons


def snap_points(points, grids_per_unit=None):
    """ Round a list of points to a grid value. """
    if grids_per_unit is None:
        grids_per_unit = _grids_per_unit()
    else:
        raise ValueError('please define grids per unit')
    points = _points_to_float(points)
    polygons = list()
    for coords in points:
        poly = list()
        for coord in coords:
            p1 = (math.floor(coord[0] * grids_per_unit + 0.5)) / grids_per_unit
            p2 = (math.floor(coord[1] * grids_per_unit + 0.5)) / grids_per_unit
            poly.append([int(p1), int(p2)])
        polygons.append(poly)

    return polygons


def c2d(coord):
    """ Convert coordinate to 2D. """
    pp = [coord[i]*1e+8 for i in range(len(list(coord))-1)]
    return pp


def c3d(coord):
    """ Convert coordinate to 3D. """
    pp = [coord[i]*1e+6 for i in range(len(list(coord)))]
    return pp


def scale_coord_up(coord):
    return [c*SCALE_UP for c in coord]


def scale_coord_down(coord):
    return [c*SCALE_DOWN for c in coord]


def scale_polygon_up(polygons, value=None):
    if value is None:
        value = SCALE_UP
    new_poly = []
    for points in polygons:
        pp = [[float(p[0]*value), float(p[1]*value)] for p in points]
        new_poly.append(pp)
    return new_poly


def scale_polygon_down(polygons, value=None):
    if value is None:
        value = SCALE_DOWN
    new_poly = []
    for points in polygons:
        pp = [[float(p[0]*value), float(p[1]*value)] for p in points]
        new_poly.append(pp)
    return new_poly


def numpy_to_list(points, start_height, unit=None):
    if unit is None:
        raise ValueError('Unit value not implemented!')
    unit = unit * 10
    return [[float(p[0]*unit), float(p[1]*unit), start_height] for p in points]



