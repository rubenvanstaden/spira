import pyclipper
import gdspy
import numpy as np
from spira.core import param
from spira.yevon.utils import *
from copy import copy, deepcopy
from spira.core.initializer import FieldInitializer
from numpy.linalg import norm

from spira.yevon.geometry.coord import CoordField
from spira.core.param.variables import *
from spira.core.descriptor import DataFieldDescriptor, DataField


# __all__ = ['Shape', 'ShapeField']


class PointArrayField(DataFieldDescriptor):

    __type__ = np.array([])

    def call_param_function(self, obj):
        f = self.get_param_function(obj)
        value = f([])
        if value is None:
            value = self.__operations__([])
        else:
            value = self.__operations__(value)
        obj.__store__[self.__name__] = value
        return value 
        # if (value is None):
        #     value = self.__process__([])
        # else:
        #     value = self.__process__([c.convert_to_array() if isinstance(c, Coord) else c for c in value])
        # return value 

    def __operations__(self, points):
        return points

    # def __process__(self, points):
    def __operations__(self, points):
        from spira.yevon.geometry.shapes.shape import Shape
        if isinstance(points, Shape):
            return array(points.points)
        elif isinstance(points, (list, np.ndarray)):
            if len(points):
                element = points[0]
                if isinstance(element, (np.ndarray, list)):
                    points_as_array = np.array(points, copy=False)
                else:
                    points_as_array = np.array([(c[0], c[1]) for c in points])
                return points_as_array
            else:
                return np.ndarray((0, 2))
        # elif isinstance(points, Coord2):
        #     return array([[points.x, points.y]])
        # elif isinstance(points, tuple):
        #     return array([[points[0], points[1]]])
        else:
            raise TypeError("Invalid type of points in setting value of PointsDefinitionProperty: " + str(type(points))) 

    def __set__(self, obj, points):
        obj.__store__[self.__name__] = points
        
    # def __deepcopy__(self, memo):
    #     from copy import deepcopy
    #     return deepcopy(obj)


class __Shape__(FieldInitializer):

    # center = param.CoordField()
    # clockwise = param.BoolField(default=False)
    # points = param.PointArrayField(fdef_name='create_points')
    # apply_merge = param.DataField(fdef_name='create_merged_points')
    # simplify = param.DataField(fdef_name='create_simplified_points')
    # edges = param.DataField(fdef_name='create_edge_lines')
    
    center = CoordField()
    clockwise = BoolField(default=False)
    points = PointArrayField(fdef_name='create_points')
    apply_merge = DataField(fdef_name='create_merged_points')
    simplify = DataField(fdef_name='create_simplified_points')
    edges = DataField(fdef_name='create_edge_lines')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_points(self, points):
        return points

    # def create_merged_points(self):
    #     """  """
    #     from spira.yevon.utils import scale_polygon_up as spu
    #     from spira.yevon.utils import scale_polygon_down as spd
    #     polygons = spd(self.points, value=1e-0)
    #     points = []
    #     for poly in polygons:
    #         if pyclipper.Orientation(poly) is False:
    #             reverse_poly = pyclipper.ReversePath(poly)
    #             solution = pyclipper.SimplifyPolygon(reverse_poly)
    #         else:
    #             solution = pyclipper.SimplifyPolygon(poly)
    #         for sol in solution:
    #             points.append(sol)
    #     self.points = boolean(subj=points, method='or')
    #     self.points = spu(self.points, value=1e0)
    #     return self

    def create_merged_points(self):
        """  """
        from spira.yevon.utils import scale_polygon_up as spu
        from spira.yevon.utils import scale_polygon_down as spd
        # polygons = spd(self.points, value=1e-0)
        # polygons = spd(self.points, value=1e-4)
        # accuracy = 1e-5
        # sc = 1/accuracy
        sc = 2**30
        polygons = pyclipper.scale_to_clipper(self.points, sc)
        points = []
        for poly in polygons:
            # print(poly)
            if pyclipper.Orientation(poly) is False:
                reverse_poly = pyclipper.ReversePath(poly)
                solution = pyclipper.SimplifyPolygon(reverse_poly)
            else:
                solution = pyclipper.SimplifyPolygon(poly)
            for sol in solution:
                points.append(sol)
        value = boolean(subj=points, method='or')
        # self.points = spu(self.points, value=1e0)
        # print(self.points)
        
        PTS = []
        mc = pyclipper.scale_from_clipper(value, sc)
        for pts in pyclipper.SimplifyPolygons(mc):
            PTS.append(np.array(pts))
        self.points = np.array(pyclipper.CleanPolygons(PTS))
        # print(self.points)

        # self.points = spu(self.points, value=1e4)
        return self

    def create_simplified_points(self):
        """  """
        from shapely.geometry import Polygon as ShapelyPolygon
        value = 1
        polygons = self.points
        self.points = []
        for points in polygons:
            factor = (len(points)/100) * 1e5 * value
            sp = ShapelyPolygon(points).simplify(factor)
            pp = [[p[0], p[1]] for p in sp.exterior.coords]
            self.points.append(pp)
        return self

    def reflect(self, p1=(0,1), p2=(0,0)):
        """ Reflect across a line. """
        points = np.array(self.points[0])
        p1 = np.array(p1)
        p2 = np.array(p2)
        if np.asarray(points).ndim == 1:
            t = np.dot((p2-p1), (points-p1))/norm(p2-p1)**2
            pts = 2*(p1 + (p2-p1)*t) - points
        if np.asarray(points).ndim == 2:
            pts = np.array([0, 0])
            for p in points:
                t = np.dot((p2-p1), (p-p1))/norm(p2-p1)**2
                r = np.array(2*(p1 + (p2-p1)*t) - p)
                pts = np.vstack((pts, r))
        self.points = [pts]
        return self

    def rotate(self, angle=45, center=(0,0)):
        """ Rotate points with an angle around a center. """
        points = np.array(self.points[0])
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
        self.points = [pts]
        return self

    @property
    def orientation(self):
        """ Returns the orientation of the shape: 
        +1(counterclock) or -1(clock) """
        # FIXME: Error with multiple shapes: [[[s1], [s2]]]
        pts = self.points[0]
        T = np.roll(np.roll(pts, 1, 1), 1, 0)
        return -np.sign(sum(np.diff(pts * T, 1, 1)))

    @property
    def area(self):
        """ Returns the area of the shape. """
        pts = self.points[0]
        T = np.roll(np.roll(pts, 1, 1), 1, 0)
        return sum(abs(np.diff(pts * T, 1, 1))) * 0.5

    @property
    def count(self):
        """ number of points in the shape """
        return self.__len__()

    def center_of_mass(self):
        c = np.mean(self.points[0], 0)
        return [c[0], c[1]]
        # return Coord2(COM[0], COM[1]) 

    def move(self, pos):
        p = np.array([pos[0], pos[1]])
        self.points += p
        return self

    @property
    def reverse(self):
        pass

    def transform(self):
        pass

    def encloses(self):
        pass

    def index(self, item):
        pass


class Shape(__Shape__):
    """ A shape is a geometrical object that 
    calculates the points that will be used 
    to generate a polygon object.
    
    Examples
    --------
    >>> shape = shapes.Shape(points=[])
    """
    
    doc = StringField()

    def __init__(self, points=None, **kwargs):
        super().__init__(**kwargs)
        if points is not None:
            self.points = points

    def __deepcopy__(self, memo):
        shape = self.modified_copy(
            points = deepcopy(self.points)
        )
        return shape

    def __contains__(self, point):
        """ Checks if point is on the shape. """
        return np.prod(sum(self.points == np.array(point[0], point[1]), 0))

    def __eq__(self, other):
        if not isinstance(other, Shape):
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __len__(self):
        pass


def ShapeField(points=[], doc='', **kwargs):
    from spira.yevon.geometry.shapes.shape import Shape
    if 'default' not in kwargs:
        kwargs['default'] = Shape(points, doc=doc)
    R = RestrictType(Shape)
    return DataFieldDescriptor(restrictions=R, **kwargs)








