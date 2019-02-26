import math
import spira
import pyclipper
import numpy as np

from spira.settings import SCALE_DOWN, SCALE_UP, OFFSET


st = pyclipper.scale_to_clipper
sf = pyclipper.scale_from_clipper


def bool_operation(subj, clip=None, method=None, closed=True, scale=1):
    from spira.gdsii.elemental.polygons import PolygonAbstract
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
        subj = pc.Execute(
            pyclipper.CT_DIFFERENCE,
            pyclipper.PFT_NONZERO,
            pyclipper.PFT_NONZERO
        )
    elif method == 'union':
        subj = pc.Execute(
            pyclipper.CT_UNION,
            pyclipper.PFT_NONZERO,
            pyclipper.PFT_NONZERO
        )
    elif method == 'intersection':
        subj = pc.Execute(
            pyclipper.CT_INTERSECTION,
            pyclipper.PFT_NONZERO,
            pyclipper.PFT_NONZERO
        )
    elif method == 'exclusive':
        subj = pc.Execute(
            pyclipper.CT_XOR,
            pyclipper.PFT_NONZERO,
            pyclipper.PFT_NONZERO
        )
    else:
        raise ValueError('Please specify a clipping method')
    points = []
    for pts in pyclipper.SimplifyPolygons(subj):
        points.append(np.array(pts))
    return np.array(points)


def offset_operation(points, offset_type=None, scale=OFFSET):
    """ Apply polygon offsetting using Angusj.
    Either blow up polygons or blow it down. """
    pco = pyclipper.PyclipperOffset()
    pco.AddPath(points, pyclipper.JT_MITER, pyclipper.ET_CLOSEDPOLYGON)
    pp = None
    if offset_type == 'down':
        pp = pco.Execute(-10000)[0]
    elif offset_type == 'up':
        pp = pco.Execute(scale * SCALE_UP)
    else:
        raise ValueError('Please select the Offset function to use')
    points = []
    for pts in pp:
        points.append(np.array(pts))
    return np.array(points)


def encloses(points, position):
    assert position is not None, 'No label position found.'
    if pyclipper.PointInPolygon(position, points) != 0:
        return True
    return False


def labeled_polygon_id(position, polygons):
    for i, spira_polygon in enumerate(polygons):
        for j, points in enumerate(spira_polygon.polygons):
            if encloses(points, position):
                return spira_polygon.id
    return None


# def _grids_per_unit():
#     return (utils.unit/utils.grid) * utils.um


# def _points_to_float(points):
#     layer = np.array(points).tolist()

#     polygons = []
#     for pl in layer:
#         poly = [[float(y) for y in x] for x in pl]
#         polygons.append(poly)
#     return polygons


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
    RDD = spira.get_rule_deck()

    """ Convert coordinate to 2D. """
    # pp = [coord[i]*1e+8 for i in range(len(list(coord))-1)]
    pp = [(coord[i]/(RDD.GDSII.GRID)) for i in range(len(list(coord))-1)]
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
        # pp = [[float(p[0]*value), float(p[1]*value)] for p in points]
        # pp = np.array([np.array([float(p[0]*value), float(p[1]*value)]) for p in points])
        pp = np.array([np.array([np.floor(float(p[0]*value)), np.floor(float(p[1]*value))]) for p in points])
        new_poly.append(pp)
    return new_poly


def scale_polygon_down(polygons, value=None):
    if value is None:
        value = SCALE_DOWN
        # value = 1
    # value = 1
    new_poly = []
    for points in polygons:
        # pp = [[float(p[0]*value), float(p[1]*value)] for p in points]
        # pp = np.array([np.array([float(p[0]*value), float(p[1]*value)]) for p in points])
        # pp = np.array([np.array([np.floor(float(p[0]*value)), np.floor(float(p[1]*value))]) for p in points])
        pp = np.array([np.array([np.floor(np.int32(p[0]*value)), np.floor(np.int32(p[1]*value))]) for p in points])
        new_poly.append(pp)
    return new_poly


def numpy_to_list(points, start_height, unit=None):
    if unit is None:
        raise ValueError('Unit value not implemented!')
    # unit = 1
    return [[float(p[0]*unit), float(p[1]*unit), start_height] for p in points]
    # return np.array([[p[0]*unit, p[1]*unit, start_height] for p in points], dtype=np.int64)



