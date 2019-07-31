import gdspy
import math
import pyclipper
import numpy as np
import networkx as nx

from spira.log import SPIRA_LOG as LOG
from numpy.linalg import norm
from spira.yevon import constants
from spira.yevon.geometry.coord import Coord
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


def angle_diff(a1, a2):
    """ The angle difference between two orientations. """
    return np.round(np.abs(np.mod(a2-a1, 360)), 3)


def angle_rad(coord, origin=(0.0, 0.0)):
    """ Absolute angle (radians) of coordinate with respect to origin"""
    return math.atan2(coord[1] - origin[1], coord[0] - origin[0])


def orientation(coord, origin=(0.0, 0.0)):
    """ Absolute angle (radians) of coordinate with respect to origin"""
    return angle_rad(coord, origin) * constants.RAD2DEG


def distance(coord, origin=(0,0)):
    """ Distance of coordinate to origin. """
    return np.sqrt((coord[0] - origin[0])**2 + (coord[1] - origin[1])**2)


def midpoint(p1, p2, ratio=0.5):
    """ Determine the midpoint between two points. """
    return ratio * Coord(p1[0], p1[1]) + (1 - ratio) * Coord(p2[0], p2[1])


def c2d(coord):
    """ Convert coordinate to 2D. """
    from spira import settings
    grids_per_unit = settings.get_grids_per_unit()
    points = [coord[i]*grids_per_unit for i in range(len(list(coord))-1)]
    return points


def lines_cross(begin1, end1, begin2, end2, inclusive=False):
    """ Returns true if the line segments intersect """
    A1 = end1[1] - begin1[1]
    B1 = -end1[0] + begin1[0]
    C1 = - (begin1[1] * B1 + begin1[0] * A1)
    A2 = end2[1] - begin2[1]
    B2 = -end2[0] + begin2[0]
    C2 = - (begin2[1] * B2 + begin2[0] * A2)
    if A1 * B2 == A2 * B1:
        return False
    if inclusive:
        return ((A1 * begin2[0] + B1 * begin2[1] + C1) * (A1 * end2[0] + B1 * end2[1] + C1) <= 0 and
                (A2 * begin1[0] + B2 * begin1[1] + C2) * (A2 * end1[0] + B2 * end1[1] + C2) <= 0)
    else:
        return ((A1 * begin2[0] + B1 * begin2[1] + C1) * (A1 * end2[0] + B1 * end2[1] + C1) < 0 and
                (A2 * begin1[0] + B2 * begin1[1] + C2) * (A2 * end1[0] + B2 * end1[1] + C2) < 0)


def lines_coincide(begin1, end1, begin2, end2):
    """ Returns true if the line segments intersect. """
    A1 = end1[1] - begin1[1]
    B1 = -end1[0] + begin1[0]
    C1 = - (begin1[1] * B1 + begin1[0] * A1)
    A2 = end2[1] - begin2[1]
    B2 = -end2[0] + begin2[0]
    C2 = - (begin2[1] * B2 + begin2[0] * A2)
    if (not(A1 or B1)) or (not(A2 or B2)):
        return False
    return abs(A1 * B2 - A2 * B1) < 1E-10 and abs(C1 * A2 - C2 * A1) < 1E-10 and abs(C1 * B2 - C2 * B1) < 1E-10


def intersection(begin1, end1, begin2, end2):
    """ Gives the intersection between two lines (not sections). """
    A1 = end1[1] - begin1[1]
    B1 = -end1[0] + begin1[0]
    C1 = begin1[1] * B1 + begin1[0] * A1
    A2 = end2[1] - begin2[1]
    B2 = -end2[0] + begin2[0]
    C2 = begin2[1] * B2 + begin2[0] * A2
    if A1 * B2 == A2 * B1:
        LOG.error("Can't intersect parallel lines")
        raise ValueError('Cannot be parallel.')
    x = (C1 * B2 - C2 * B1) / (A1 * B2 - A2 * B1)
    y = (C1 * A2 - C2 * A1) / (B1 * A2 - B2 * A1)
    return Coord(x, y)


def sort_points_on_line(point_list):
    """ Sorts points by distance on a line, taking the
    two first points as the reference direction. """
    point_list = [Coord(p[0], p[1]) for p in point_list]
    p0 = point_list[0]
    dx = point_list[1][0] - point_list[0][0]
    dy = point_list[1][1] - point_list[0][1]
    point_list.sort(key=lambda p: distance(p, p0))
    return point_list


def points_unique(coordinates):
    """ Remove duplicate points from point list. """
    unique_coordinates = []
    for c in coordinates:
        already_in_list = False
        for uc in unique_coordinates:
            if c == uc:
                already_in_list = True
        if not already_in_list:
            unique_coordinates.append(c)
    return unique_coordinates

                                
