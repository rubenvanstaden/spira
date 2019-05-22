import numpy as np


def reflect_algorithm(points, p1=(0,0), p2=(1,0)):
    points = np.array(points); p1 = np.array(p1); p2 = np.array(p2)
    if np.asarray(points).ndim == 1:
        t = np.dot((p2-p1), (points-p1))/norm(p2-p1)**2
        pts = 2*(p1 + (p2-p1)*t) - points
    if np.asarray(points).ndim == 2:
        t = np.dot((p2-p1), (p2-p1))/norm(p2-p1)**2
        pts = np.array([2*(p1 + (p2-p1)*t) - p for p in points])
    return pts


def rotate_algorithm(points, angle=45, center=(0,0)):
    if isinstance(points, Coord):
        points = points.to_ndarray()
    if isinstance(center, Coord):
        center = center.to_ndarray()
    angle = angle*np.pi/180
    ca = np.cos(angle)
    sa = np.sin(angle)
    sa = np.array((-sa, sa))
    c0 = np.array(center)
    if np.asarray(points).ndim == 2:
        pts = (points - c0) * ca + (points - c0)[:,::-1] * sa + c0
        pts = np.round(pts, 6)
    if np.asarray(points).ndim == 1:
        pts = (points - c0) * ca + (points - c0)[::-1] * sa + c0
        pts = np.round(pts, 6)
    return pts
