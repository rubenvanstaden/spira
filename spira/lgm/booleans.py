import pyclipper
from spira.kernel.utils import bool_operation


def merge(points):
    pcell = False
    poly_list = []
    pts = []
    for poly in points:
        if pyclipper.Orientation(poly) is False:
            reverse_poly = pyclipper.ReversePath(poly)
            solution = pyclipper.SimplifyPolygon(reverse_poly)
        else:
            solution = pyclipper.SimplifyPolygon(poly)
        for sol in solution:
            pts.append(sol)
    return bool_operation(subj=pts, method='union')