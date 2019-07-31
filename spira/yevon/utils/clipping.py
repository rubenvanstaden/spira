import pyclipper
import numpy as np
import spira.all as spira

from copy import deepcopy
from spira.yevon import constants
from spira.yevon.gdsii.elem_list import ElementList
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


st = pyclipper.scale_to_clipper
sf = pyclipper.scale_from_clipper


def boolean(subj, clip=None, clip_type=None, closed=True):
    """ Apply boolean operation of polygons. """
    if clip is None and len(subj) <= 1: return subj
    pc = pyclipper.Pyclipper()
    sc = constants.CLIPPER_SCALE
    if clip is not None:
        clip_pts = reverse_points(clip)
        pc.AddPaths(clip_pts, pyclipper.PT_CLIP, True)
    subj_pts = reverse_points(subj)
    pc.AddPaths(subj_pts, pyclipper.PT_SUBJECT, closed)
    ct = {
        'or' : pyclipper.CT_UNION,
        'and': pyclipper.CT_INTERSECTION,
        'not': pyclipper.CT_DIFFERENCE,
        'xor': pyclipper.CT_XOR
    }
    if clip_type not in ct:
        print("jointype '{}' unknown.".format(jointype))
        print("jointype should be one of 'or', 'and', 'not', 'xor'.")
        print("Using default ('or')")
        clip_type = 'or'
    value = pc.Execute(ct[clip_type], pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)
    value = clean_points(pts=value)
    return value


def offset(points, grow=1, jointype='miter'):
    """ Grow polygons and return the grown structures. """
    if grow == 0: return points
    sc = constants.CLIPPER_SCALE
    pco = pyclipper.PyclipperOffset()
    jt = {
        'round' : pyclipper.JT_ROUND,
        'square': pyclipper.JT_SQUARE,
        'miter' : pyclipper.JT_MITER
    }
    if jointype not in jt:
        print("jointype '{}' unknown.".format(jointype))
        print("jointype should be one of 'round', 'square', 'miter'.")
        print("Using default ('round')")
        jointype = 'round'
    pco.AddPaths(st([points], sc), jt[jointype], pyclipper.ET_CLOSEDPOLYGON)
    return sf(pco.Execute(grow*sc), sc)


def reverse_points(pts):
    """ If orientation is clockwise, convert to counter-clockwise. """
    points = []
    sc = constants.CLIPPER_SCALE
    for poly in st(pts, sc):
        if pyclipper.Orientation(poly) is False:
            reverse_poly = pyclipper.ReversePath(poly)
            solution = pyclipper.SimplifyPolygon(reverse_poly)
        else:
            solution = pyclipper.SimplifyPolygon(poly)
        points.extend(solution)
    return points


def simplify_points(points, value=100):
    """ Simplify curved shapes with more than 199 points. """
    from shapely.geometry import Polygon as ShapelyPolygon
    if len(points) > 199:
        factor = len(points) * value * RDD.GDSII.GRID
        sp = ShapelyPolygon(points).simplify(factor)
        points = [[p[0], p[1]] for p in sp.exterior.coords]
    return points


def clean_points(pts):
    """ Clean the polygon by getting rid of numerical artifacts. 
    This is required to overcome Gmsh parsing errors. """
    sc = constants.CLIPPER_SCALE
    spl_pts = pyclipper.SimplifyPolygons(pts)
    cln_pts = pyclipper.CleanPolygons(spl_pts)
    pts = sf(cln_pts, sc)
    return np.array(pts)


def encloses(coord, points):
    """  """
    sc = constants.CLIPPER_SCALE
    coord = st(coord.to_list(), sc)
    points = st(points, sc)
    return pyclipper.PointInPolygon(coord, points) != 0


