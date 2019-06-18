import pyclipper
import numpy as np
import spira.all as spira

from copy import deepcopy
from spira.yevon import constants
from spira.yevon.gdsii.elem_list import ElementalList
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


st = pyclipper.scale_to_clipper
sf = pyclipper.scale_from_clipper


def boolean(subj, clip=None, clip_type=None, closed=True, scale=1):
    """ Apply boolean operation of polygons. """
    if clip is None and len(subj) <= 1: return subj
    sc = constants.CLIPPER_SCALE
    pc = pyclipper.Pyclipper()
    if clip is not None:
        pc.AddPaths(st(clip, sc), pyclipper.PT_CLIP, True)
    pc.AddPaths(st(subj, sc), pyclipper.PT_SUBJECT, closed)
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
    return sf(value, sc)


def offset(points, grow=1, accuracy=1.0, jointype='miter'):
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
    pts = sf(pco.Execute(grow*sc), sc)
    return pts


def simplify_points(points, value=100):
    """  """
    from shapely.geometry import Polygon as ShapelyPolygon
    if len(points) > 199:
        factor = len(points) * value * RDD.GDSII.GRID
        sp = ShapelyPolygon(points).simplify(factor)
        points = [[p[0], p[1]] for p in sp.exterior.coords]
        simplify_points(points, value)
    return points


def reverse_points(pts):
    """  """
    polygons = pyclipper.scale_to_clipper(pts, constants.CLIPPER_SCALE)
    points = []
    for poly in polygons:
        if pyclipper.Orientation(poly) is False:
            reverse_poly = pyclipper.ReversePath(poly)
            solution = pyclipper.SimplifyPolygon(reverse_poly)
        else:
            solution = pyclipper.SimplifyPolygon(poly)
        for sol in solution:
            points.append(sol)
    return points


def clean_points(pts):
    """  """
    new_points = []
    mc = pyclipper.scale_from_clipper(pts, constants.CLIPPER_SCALE)
    for ps in pyclipper.SimplifyPolygons(mc):
        new_points.append(np.array(ps))
    cln_pts = pyclipper.CleanPolygons(new_points)
    points = np.array([np.array(p) for p in cln_pts])
    return points




