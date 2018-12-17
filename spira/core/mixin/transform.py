import numpy as np
from numpy.linalg import norm


class TranformationMixin(object):

    def _rotate_points(self, points, angle = 45, center = (0,0)):
        """
        Rotates points around a centerpoint defined by `center`.
        `points` may be input as either single points [1,2]
        or array-like[N][2], and will return in kind
        """
        angle = angle*np.pi/180
        ca = np.cos(angle)
        sa = np.sin(angle)
        sa = np.array((-sa, sa))
        c0 = np.array(center)
        if np.asarray(points).ndim == 2:
            return (points - c0) * ca + (points - c0)[:,::-1] * sa + c0
        if np.asarray(points).ndim == 1:
            return (points - c0) * ca + (points - c0)[::-1] * sa + c0


    def _reflect_points(self, points, p1=(0,0), p2=(1,0)):
        """
        Reflects points across the line formed by p1 and
        p2. `points` may be input as either single points
        [1,2] or array-like[N][2], and will return in kind
        """
        # From http://math.stackexchange.com/questions/11515/point-reflection-across-a-line
        points = np.array(points); p1 = np.array(p1); p2 = np.array(p2)
        if np.asarray(points).ndim == 1:
            return 2*(p1 + (p2-p1)*np.dot((p2-p1),(points-p1))/norm(p2-p1)**2) - points
        if np.asarray(points).ndim == 2:
            t = np.dot((p2-p1),(p-p1))/norm(p2-p1)**2
            x = np.array([2*(p1 + (p2-p1)*t) - p for p in points])
            return x

