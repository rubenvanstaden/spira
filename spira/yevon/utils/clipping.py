import pyclipper
import numpy as np
import spira.all as spira
from spira.yevon import constants
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


st = pyclipper.scale_to_clipper
sf = pyclipper.scale_from_clipper


def simplify_points(points):
    """

    """
    from shapely.geometry import Polygon as ShapelyPolygon
    value = 1
    polygons = points
    points = []
    for points in polygons:
        factor = (len(points)/100) * 1e5 * value
        sp = ShapelyPolygon(points).simplify(factor)
        pp = [[p[0], p[1]] for p in sp.exterior.coords]
        self.points.append(pp)
    return self


# def union_polygons(poly_elems):
#     """
    
#     """
#     mapping = {}
#     elems = spira.ElementalList()
#     for e in poly_elems:
#         if isinstance(e, spira.Polygon):
#             if e.layer not in mapping.keys():
#                 mapping[e.layer] = list(np.array([e.shape.points]))
#             else:
#                 mapping[e.layer].append(e.shape.points)
#     # print(mapping)
#     for layer, points in mapping.items():
#         pts_group = union_points(points)
#         for uid, pts in enumerate(pts_group):
#             elems += spira.Polygon(shape=pts, layer=layer)
#             # name = 'metal_{}_{}_{}'.format('NAME', layer.layer.number, uid)
#             # shape = shapes.Shape(points=pts)
#             # ply = spira.Polygon(shape=pts, layer=layer)
#             # elems += ply
#     return elems
        

def union_points(pts):
    """
    
    """
    points = convert_to_pyclipper_array(pts)
    points = boolean(subj=points, method='or')
    points = convert_to_numpy_array(points)
    return points


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
    el = spira.ElementalList()
    for i, e1 in enumerate(elems):
        for j, e2 in enumerate(elems):
            if i != j:
                polygons = e1 & e2
                for p in polygons:
                    p.layer.purpose = RDD.PURPOSE.INTERSECTED
                el += polygons
    return el


# def merge_points(pts):
#     """  """
#     # TODO: Check that points are a 3D ndarray.
#     sc = 2**30
#     polygons = pyclipper.scale_to_clipper(pts, sc)
#     points = []
#     for poly in polygons:
#         if pyclipper.Orientation(poly) is False:
#             reverse_poly = pyclipper.ReversePath(poly)
#             solution = pyclipper.SimplifyPolygon(reverse_poly)
#         else:
#             solution = pyclipper.SimplifyPolygon(poly)
#         for sol in solution:
#             points.append(sol)
#     value = apply_boolean(subj=points, method='or')
#     PTS = []
#     mc = pyclipper.scale_from_clipper(value, sc)
#     for pts in pyclipper.SimplifyPolygons(mc):
#         PTS.append(np.array(pts))
#     cln_pts = pyclipper.CleanPolygons(PTS)
#     points = np.array([np.array(p) for p in cln_pts])
#     return points


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


def convert_to_numpy_array(pts):
    """
    
    """
    new_points = []
    mc = pyclipper.scale_from_clipper(pts, constants.CLIPPER_SCALE)
    for ps in pyclipper.SimplifyPolygons(mc):
        new_points.append(np.array(ps))
    cln_pts = pyclipper.CleanPolygons(new_points)
    points = np.array([np.array(p) for p in cln_pts])
    return points


def boolean(subj, clip=None, method=None, closed=True, scale=1):
    """
    
    """
    from spira.yevon.gdsii.polygon import Polygon

    if clip is None and len(subj) <= 1:
        return subj

    sc = 1/scale

    pc = pyclipper.Pyclipper()
    if isinstance(subj, Polygon):
        subj = subj.polygons
    if isinstance(clip, Polygon):
        clip = clip.polygons
    if clip is not None:
        # pc.AddPaths(st(clip, sc), pyclipper.PT_CLIP, True)
        pc.AddPaths(clip, pyclipper.PT_CLIP, True)
        # pc.AddPath(clip, pyclipper.PT_CLIP, True)
    # pc.AddPaths(st(subj, sc), pyclipper.PT_SUBJECT, closed)
    pc.AddPaths(subj, pyclipper.PT_SUBJECT, closed)
    # pc.AddPath(subj, pyclipper.PT_SUBJECT, closed)

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

    return value


def offset(points, offset_type=None, scale=constants.OFFSET):
    """ 
    Apply polygon offsetting using Angusj.
    Either blow up polygons or blow it down. 
    """
    pco = pyclipper.PyclipperOffset()
    pco.AddPath(points, pyclipper.JT_MITER, pyclipper.ET_CLOSEDPOLYGON)
    pp = None
    if offset_type == 'down':
        pp = pco.Execute(-10000)[0]
    elif offset_type == 'up':
        pp = pco.Execute(scale * constants.SCALE_UP)
    else:
        raise ValueError('Please select the Offset function to use')
    points = []
    for pts in pp:
        points.append(np.array(pts))
    return np.array(points)


