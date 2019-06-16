import pyclipper
import numpy as np
import spira.all as spira
from spira.yevon import constants
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


st = pyclipper.scale_to_clipper
sf = pyclipper.scale_from_clipper


def simplify_points(points, value=100):
    """

    """
    from shapely.geometry import Polygon as ShapelyPolygon
    if len(points) > 199:
        factor = len(points) * value
        sp = ShapelyPolygon(points).simplify(factor)
        points = [[p[0], p[1]] for p in sp.exterior.coords]
        simplify_points(points, value)
    return points


def union_points(pts):
    """
    
    """
    points = convert_to_pyclipper_array(pts)
    points = boolean(subj=points, method='or')
    points = convert_to_numpy_array(points)
    return points


    # FIXME: Required for .merge in PolygonGroup
def union_polygons(elems):
    """
    
    """
    el = spira.ElementalList()
    for i, e1 in enumerate(elems):
        for j, e2 in enumerate(elems):
            if i != j:
                polygons = e1 | e2
                # for p in polygons:
                #     p.layer.purpose = RDD.PURPOSE.UNION
                el += polygons
    return el


def intersection_polygons(elems):
    """
    
    """
    from copy import deepcopy
    el = spira.ElementalList()
    for i, e1 in enumerate(elems):
        for j, e2 in enumerate(elems):
            if i != j:
                e1 = deepcopy(e1)
                e2 = deepcopy(e2)
                polygons = e1 & e2
                for p in polygons:
                    p.layer.purpose = RDD.PURPOSE.INTERSECTED
                for p in polygons:
                    el += p
    return el


# FIXME: Required for .merge in PolygonGroup
def convert_to_pyclipper_array(pts):
    """
    
    """
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


# FIXME: Required for .merge in PolygonGroup
def convert_to_numpy_array(pts):
    """
    
    """
    print(pts)
    new_points = []
    mc = pyclipper.scale_from_clipper(pts, constants.CLIPPER_SCALE)
    for ps in pyclipper.SimplifyPolygons(mc):
        new_points.append(np.array(ps))
    cln_pts = pyclipper.CleanPolygons(new_points)
    points = np.array([np.array(p) for p in cln_pts])
    print(points)
    return points


def boolean(subj, clip=None, method=None, closed=True, scale=1):
    """
    
    """

    if clip is None and len(subj) <= 1:
        return subj

    # # FIXME: Required for .merge in PolygonGroup
    # pc = pyclipper.Pyclipper()
    # if clip is not None:
    #     # pc.AddPaths(st(clip, sc), pyclipper.PT_CLIP, True)
    #     pc.AddPaths(clip, pyclipper.PT_CLIP, True)
    # pc.AddPaths(subj, pyclipper.PT_SUBJECT, closed)
    # # pc.AddPaths(st(subj, sc), pyclipper.PT_SUBJECT, closed)

    pc = pyclipper.Pyclipper()
    if clip is not None:
        pc.AddPaths(st(clip, constants.CLIPPER_SCALE), pyclipper.PT_CLIP, True)
    pc.AddPaths(st(subj, constants.CLIPPER_SCALE), pyclipper.PT_SUBJECT, closed)

    if method == 'not':
        value = pc.Execute(pyclipper.CT_DIFFERENCE, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)
    elif method == 'or':
        value = pc.Execute(pyclipper.CT_UNION, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)
    elif method == 'and':
        value = pc.Execute(pyclipper.CT_INTERSECTION, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)
    elif method == 'xor':
        value = pc.Execute(pyclipper.CT_XOR, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)
    else:
        raise ValueError('Please specify a clipping method')

    value = sf(value, constants.CLIPPER_SCALE)

    return value


# def offset(pts, value, scale=constants.OFFSET):
#     """

#     """
#     pco = pyclipper.PyclipperOffset()
#     pco.AddPaths([pts], pyclipper.JT_MITER, pyclipper.ET_CLOSEDPOLYGON)
#     points = pco.Execute(value)
#     print(points)
#     return points[0]


def offset(points, grow=1, accuracy=1.0, jointype='miter'):
    """
    Grow polygons and return the grown structures.

    Args:
        paths (list): list of polygons that each have a list of (x,y) coordinates.
        accuracy (float): accuracy [µm] of the location of the intermediate points.
        The accuracy determines the grid on which the grown path is drawn.
        jointype: specifies the type of growing that is used.
        The jointype is one of 'round' (default), 'square' or 'miter'.

    Returns:
        list: list of points [(x1, y1), (x2, y2), ...]
    """
    if grow == 0:
        return points
    sc = constants.CLIPPER_SCALE
    pco = pyclipper.PyclipperOffset()
    jt = {'round': pyclipper.JT_ROUND, 'square': pyclipper.JT_SQUARE, 'miter': pyclipper.JT_MITER}
    if jointype not in jt:
        print("jointype '{}' unknown.".format(jointype))
        print("jointype should be one of 'round', 'square', 'miter'.")
        print("Using default ('round')")
        jointype = 'round'
    pco.AddPaths(st([points], sc), jt[jointype], pyclipper.ET_CLOSEDPOLYGON)
    pts = sf(pco.Execute(grow*sc), sc)
    print(pts[0])
    return pts


# def offset(pts, value, scale=constants.OFFSET):
#     """

#     """
#     print(pts)
#     points = convert_to_pyclipper_array(pts)
#     print(points)
#     pco = pyclipper.PyclipperOffset()
#     pco.AddPath(points, pyclipper.JT_MITER, pyclipper.ET_CLOSEDPOLYGON)
#     points = pco.Execute(value)
#     points = convert_to_numpy_array(points)
#     # print(points)
#     return points
#     # points = []
#     # for pts in pp:
#     #     points.append(np.array(pts))
#     # return np.array(points)


# # # def offset(points, offset_type=None, scale=constants.OFFSET):
# # #     """

# # #     """
# # #     pco = pyclipper.PyclipperOffset()
# # #     pco.AddPath(points, pyclipper.JT_MITER, pyclipper.ET_CLOSEDPOLYGON)
# # #     pp = None
# # #     if offset_type == 'down':
# # #         pp = pco.Execute(-10000)[0]
# # #     elif offset_type == 'up':
# # #         pp = pco.Execute(scale * constants.SCALE_UP)
# # #     else:
# # #         raise ValueError('Please select the Offset function to use')
# # #     points = []
# # #     for pts in pp:
# # #         points.append(np.array(pts))
# # #     return np.array(points)


