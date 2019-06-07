import gdspy
import math
import pyclipper
import numpy as np
import networkx as nx

from numpy.linalg import norm
from spira.yevon import constants
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


def angle_diff(a1, a2):
    return np.round(np.abs(np.mod(a2-a1, 360)), 3)


def angle_rad(coord, origin=(0.0, 0.0)):
    """ Absolute angle (radians) of coordinate with respect to origin"""
    return math.atan2(coord[1] - origin[1], coord[0] - origin[0])


def angle_deg(coord, origin=(0.0, 0.0)):
    """ Absolute angle (radians) of coordinate with respect to origin"""
    return angle_rad(coord, origin) * constants.RAD2DEG


def distance(coord, origin=(0.0, 0.0)):
    """ Distance of coordinate to origin. """
    return np.sqrt((coord[0] - origin[0])**2 + (coord[1] - origin[1])**2)


def encloses(points, position):
    assert position is not None, 'No label position found.'
    if pyclipper.PointInPolygon(position, points) != 0:
        return True
    return False


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
    # pp = [(coord[i]/(RDD.GDSII.GRID)) for i in range(len(list(coord))-1)]
    pp = [coord[i] for i in range(len(list(coord))-1)]
    return pp


def c3d(coord):
    """ Convert coordinate to 3D. """
    # pp = [coord[i]*RDD.GDSII.GRID for i in range(len(list(coord)))]
    pp = [coord[i] for i in range(len(list(coord)))]
    return pp


def scale_coord_up(coord):
    return [c*constants.SCALE_UP for c in coord]


def scale_coord_down(coord):
    return [c*constants.SCALE_DOWN for c in coord]


def scale_polygon_up(polygons, value=None):
    if value is None:
        value = constants.SCALE_UP
    new_poly = []
    for points in polygons:
        pp = np.array([np.array([np.floor(float(p[0]*value)), np.floor(float(p[1]*value))]) for p in points])
        new_poly.append(pp)
    return new_poly


def scale_polygon_down(polygons, value=None):
    if value is None:
        value = constants.SCALE_DOWN
    new_poly = []
    for points in polygons:
        pp = np.array([np.array([np.floor(np.int32(p[0]*value)), np.floor(np.int32(p[1]*value))]) for p in points])
        new_poly.append(pp)
    return new_poly


def numpy_to_list(points, start_height, unit=None):
    return [[float(p[0]*unit), float(p[1]*unit), start_height] for p in points]


def cut(ply, position, axis):
    import spira.all as spira
    plys = spira.ElementalList()
    gp = ply.commit_to_gdspy()
    pl = gdspy.slice(objects=[gp], position=position, axis=axis)
    for p in pl:
        if len(p.polygons) > 0:
            plys += spira.Polygon(shape=p.polygons[0])
    return plys




