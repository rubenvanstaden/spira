import spira
import pyclipper
from spira import param
from spira.gdsii.utils import *
from spira.core.initializer import FieldInitializer


class __Shape__(FieldInitializer):

    gdslayer = param.LayerField()
    points = param.PointArrayField(fdef_name='create_points')
    apply_merge = param.DataField(fdef_name='create_merged_points')
    simplify = param.DataField(fdef_name='create_simplified_points')

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

    def area(self):
        pass

    def point_inside(self):
        pass

    @property
    def orientation(self):
        """ The point orientation, either clockwise
        or counterclockwise"""
        print(len(self.points))

    @property
    def count(self):
        """ number of points in the shape """
        return self.__len__()

    @property
    def reverse(self):
        pass

    def index(self, item):
        pass

    def __repr__(self):
        pass

    def __str__(self):
        return self.__repr__()

    def id_string(self):
        return self.__str__()

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
        print(points)
        if points is not None:
            self.points = points

    def __deepcopy__(self, memo):
        return Shape(points = deepcopy(self.points),
                     closed = self.closed,
                     start_face_angle = self.start_face_angle,
                     end_face_angle = self.end_face_angle)















