import spira
import pyclipper
import numpy as np
from spira import param
from spira.gdsii.utils import *
from spira.core.initializer import FieldInitializer


class __Shape__(FieldInitializer):

    center = param.PointField()
    gdslayer = param.LayerField()
    clockwise = param.BoolField(default=False)
    points = param.PointArrayField(fdef_name='create_points')
    apply_merge = param.DataField(fdef_name='create_merged_points')
    simplify = param.DataField(fdef_name='create_simplified_points')
    edges = param.DataField(fdef_name='create_edge_lines')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_points(self, points):
        return points

    def create_merged_points(self):
        pcell = False
        poly_list = []
        polygons = self.points
        self.points = []
        for poly in polygons:
            if pyclipper.Orientation(poly) is False:
                reverse_poly = pyclipper.ReversePath(poly)
                solution = pyclipper.SimplifyPolygon(reverse_poly)
            else:
                solution = pyclipper.SimplifyPolygon(poly)
            for sol in solution:
                self.points.append(sol)
        self.points = bool_operation(subj=self.points, method='union')
        return self

    def create_simplified_points(self):
        from shapely.geometry import Polygon as ShapelyPolygon
        value = 1
        polygons = self.points
        self.points = []
        for points in polygons:
            factor = (len(points)/100) * 1e5 * value
            sp = ShapelyPolygon(points).simplify(factor)
            pp = [[p[0], p[1]] for p in sp.exterior.coords]
            # if len(points) > 10:
            #     factor = (len(points)/100) * 1e5 * value
            #     sp = ShapelyPolygon(points).simplify(factor)
            #     pp = [[int(p[0]), int(p[1])] for p in sp.exterior.coords]
            # else:
            #     pp = points
            self.points.append(pp)
        return self

    def move(self):
        pass

    def transform(self):
        pass

    @property
    def area(self):
        """ Returns the area of the shape. """
        pts = self.points[0]
        T = np.roll(np.roll(pts, 1, 1), 1, 0)
        return sum(abs(np.diff(pts * T, 1, 1))) * 0.5

    @property
    def orientation(self):
        """ Returns the orientation of the 
        shape: +1(counterclock) or -1(clock) """
        # FIXME: Error with multiple shapes: [[[s1], [s2]]]
        pts = self.points[0]
        T = np.roll(np.roll(pts, 1, 1), 1, 0)
        return -np.sign(sum(np.diff(pts * T, 1, 1)))

    def point_inside(self):
        pass

    @property
    def count(self):
        """ number of points in the shape """
        return self.__len__()

    @property
    def reverse(self):
        pass

    def index(self, item):
        pass

    def id_string(self):
        return self.__str__()

    # def __repr__(self):
    #     return 'Shape'

    # def __str__(self):
    #     return self.__repr__()

    def __eq__(self, other):
        if not isinstance(other, Shape):
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __len__(self):
        pass


class Shape(__Shape__):

    def __init__(self, points=None, **kwargs):
        super().__init__(**kwargs)
        if points is not None:
            # from spira.gdsii.utils import scale_polygon_up as spu
            # self.points = spu(points)
            self.points = points

    def __deepcopy__(self, memo):
        from copy import copy, deepcopy
        from spira.gdsii.utils import scale_polygon_down as spd

        shape = self.modified_copy(
            # points = spd(self.points),
            points = deepcopy(self.points),
            gdslayer = deepcopy(self.gdslayer)
        )

        return shape


# TODO: Add boolean operations of shapes.
# An arrow can be a triangle + box>
class Arrow(Shape):

    rotation = param.FloatField()

    wh = param.FloatField(default=0.2)
    wb = param.FloatField(default=0.1)
    hh = param.FloatField(default=0.6)
    hb = param.FloatField(default=1)

    arrow_head = param.PointField()

    endpoints = param.DataField(fdef_name='create_endpoints')

    def create_endpoints(self):
        return (self.arrow_head, [self.wb/2, 0])

    def create_points(self, points):
        self.arrow_head = [self.wb/2, self.hb+self.hh]
        pts = [[0,0], [self.wb,0], [self.wb,self.hb], 
               [self.wh,self.hb], self.arrow_head, 
               [-self.wb,self.hb], [0,self.hb]]
        points += [pts]
        return points

    def __repr__(self):
        return ("[SPiRA: Arrow] points {}").format(len(self.points[0]))

    def __str__(self):
        return self.__repr__()












