import math
import gdspy
import pyclipper
import numpy as np

from numpy.linalg import norm
from copy import copy, deepcopy

from spira.yevon.utils import *
from spira.yevon import constants
from spira.yevon.geometry import bbox_info
from spira.core.parameters.variables import *
from spira.core.transformable import Transformable
from spira.yevon.geometry.ports.port_list import PortList
from spira.core.parameters.variables import ListParameter
from spira.yevon.geometry.coord import CoordParameter, Coord
from spira.core.parameters.initializer import ParameterInitializer
from spira.core.parameters.processors import ProcessorTypeCast
from spira.core.parameters.descriptor import ParameterDescriptor, Parameter
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = ['Shape', 'ShapeParameter', 'PointArrayParameter', 'shape_edge_ports']


st = pyclipper.scale_to_clipper
sf = pyclipper.scale_from_clipper


class PointArrayParameter(ParameterDescriptor):
    """  """

    def call_param_function(self, obj):
        f = self.get_param_function(obj)
        value = f([])
        if value is None:
            value = self.__process__([])
        else:
            value = self.__process__([c.to_numpy_array() if isinstance(c, Coord) else c for c in value])
        self.__cache_parameter_value__(obj, value)
        return value

    def __process__(self, points):
        if isinstance(points, Shape):
            return np.array(points.points)
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
        elif isinstance(points, Coord):
            return np.array([[points.x, points.y]])
        elif isinstance(points, tuple):
            return np.array([[points[0], points[1]]])
        else:
            raise TypeError("Invalid type of points in setting " +
                "value of PointsDefinitionProperty: " + str(type(points)))

    def __set__(self, obj, points):
        points = self.__process__(points)
        self.__externally_set_parameter_value__(obj, points)


class __Shape__(Transformable, ParameterInitializer):

    center = CoordParameter()
    clockwise = BoolParameter(default=False)
    points = PointArrayParameter(fdef_name='create_points')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_points(self, points):
        return points

    @property
    def x_coords(self):
        """ Returns the x coordinates """
        return self.points[:, 0]

    @property
    def y_coords(self):
        """ Returns the y coordinates """
        return self.points[:, 1]

    @property
    def is_closed(self):
        return True

    @property
    def center_of_mass(self):
        """ Get the center of mass of the shape.
        Note: This is not the same as the bounding box center."""
        c = np.mean(self.points, 0)
        return [c[0], c[1]]

    @property
    def orientation(self):
        """ Returns the orientation of the shape.
        Counterclockwise returns +1 and clockwise returns -1. """
        pts = self.points
        T = np.roll(np.roll(pts, 1, 1), 1, 0)
        return -np.sign(sum(np.diff(pts * T, 1, 1)))

    @property
    def area(self):
        """ Returns the area of the shape. """
        pts = self.points
        T = np.roll(np.roll(pts, 1, 1), 1, 0)
        return sum(abs(np.diff(pts * T, 1, 1))) * 0.5

    @property
    def hash_string(self):
        import hashlib
        pts = np.array([self.points])
        hash_key = np.sort([hashlib.sha1(p).hexdigest() for p in pts])
        return str(hash_key[0])

    @property
    def count(self):
        """ Number of points in the shape """
        return self.__len__()

    @property
    def bbox_info(self):
        return bbox_info.bbox_info_from_numpy_array(self.points)

    def reverse_points(self):
        """ If orientation is clockwise, convert to counter-clockwise. """
        sc = constants.CLIPPER_SCALE
        pts = st(self.points, sc)
        if pyclipper.Orientation(pts) is False:
            reverse_poly = pyclipper.ReversePath(pts)
            solution = pyclipper.SimplifyPolygon(reverse_poly)
        else:
            solution = pyclipper.SimplifyPolygon(pts)
        self.points = sf(solution, sc)[0]
        return self
    
    def segments(self):
        """ Returns a list of point pairs 
        with the segments of the shape. """
        p = self.points
        if len(p) < 2:
            return []
        if self.is_closed:
            segments = list(zip(p, np.roll(p, shift=-1, axis=0)))
        else:
            segments = list(zip(p[:-1], p[1:]))
        return segments

    def snap_to_grid(self, grids_per_unit=None):
        """ Snaps all shape points to grid. """
        from spira.settings import get_grids_per_unit
        if grids_per_unit is None:
            grids_per_unit = get_grids_per_unit()
        self.points = (np.floor(self.points * grids_per_unit + 0.5)) / grids_per_unit 
        return self

    def move(self, pos):
        p = np.array([pos[0], pos[1]])
        self.points += p
        return self

    def transform(self, transformation):
        self.points = transformation.apply_to_array(self.points)
        return self

    def make_clockwise(self):
        """ Make sure all points are clockwise ordered. """
        x, y = self.x_coords, self.y_coords
        cx, cy = np.mean(x), np.mean(y)
        a = np.arctan2(y - cy, x - cx)
        order = a.ravel().argsort()
        self.points = np.column_stack((x[order], y[order]))
        return self

    def remove_identicals(self):
        """ Removes consecutive identical points """
        from spira import settings
        pts = self.points
        if len(pts) > 1:
            identicals = np.prod(abs(pts - np.roll(self.points, -1, 0)) < 0.5 / settings.get_grids_per_unit(), 1)
            if not self.is_closed:
                identicals[-1] = False
            self.points = np.delete(pts, identicals.nonzero()[0], 0)
        return self

    def remove_straight_angles(self):
        """ removes points with turn zero or 180 degrees """
        Shape.remove_identicals(self)
        pts = self.points
        if len(pts) > 1:
            straight = (abs(abs((self.turns_rad() + (0.5 * np.pi)) % np.pi) - 0.5 * np.pi) < 0.00001)
            if not self.is_closed:
                straight[0] = False
                straight[-1] = False
            self.points = np.delete(pts, straight.nonzero()[0], 0)
        return self

    def angles_rad(self):
        """ returns the angles (radians) of the connection between each point and the next """
        pts = self.points
        R = np.roll(pts, -1, 0)
        radians = np.arctan2(R[:, 1] - pts[:, 1], R[:, 0] - pts[:, 0])
        return radians

    def turns_rad(self):
        """ returns the angles (radians) of the turn in each point """
        a = self.angles_rad()
        return (a - np.roll(a, 1, 0) + np.pi) % (2 * np.pi) - np.pi

    def intersections(self, other_shape):
        """ the intersections with this shape and the other shape """
        from spira.yevon.utils import geometry as gm

        s = Shape(self.points)
        s.remove_straight_angles()
        segments1 = s.segments()
        if len(segments1) < 1:
            return []

        s = Shape(other_shape)
        s.remove_straight_angles()
        segments2 = s.segments()
        if len(segments2) < 1:
            return []

        intersections = []
        for s1 in segments1:
            intersected_points = []
            for s2 in segments2:
                if gm.lines_cross(s1[0], s1[1], s2[0], s2[1], inclusive=True):
                    c = [gm.intersection(s1[0], s1[1], s2[0], s2[1])]
                    intersected_points += c
            if len(intersected_points) > 0:
                pl = gm.sort_points_on_line([*s1, *intersected_points])
                intersections += [pl[1], pl[2]]

        intersections = gm.points_unique(intersections)
        return Shape(intersections)


class Shape(__Shape__):
    """ 
    A shape is a geometrical object that
    calculates the points that will be used
    to generate a polygon object.

    Examples
    --------
    >>> shape = shapes.Shape(points=[])
    """

    doc = StringParameter()
    segment_labels = ListParameter(fdef_name='create_segment_labels')

    def __init__(self, points=None, **kwargs):
        super().__init__(**kwargs)
        if points is not None:
            self.points = points

    def __repr__(self):
        return "[SPiRA: Shape] (points {})".format(self.center_of_mass)

    def __str__(self):
        return self.__repr__()

    # # NOTE: For some reason is required for deepcopy in `create_edge_ports`.
    # def __deepcopy__(self, memo):
    #     return Shape(points=deepcopy(self.points), transformation=deepcopy(self.transformation))

    def __getitem__(self, index):
        """ Access a point. """
        p = self.points[index]
        return Coord(p[0], p[1])

    def __contains__(self, point):
        """ Checks if point is in the shape. """
        return any((self.points[:] == np.array([point[0], point[1]])).all(1))

    def __eq__(self, other):
        if not isinstance(other, Shape):
            return False
        if np.array([p1 == p2 for p1, p2 in zip(self.points, other.points)]).all():
            return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __len__(self):
        """ Number of points in the shape """
        return np.size(self.points, 0)

    def append(self, point):
        if isinstance(point, (Coord, tuple)):
            point_arr = [(point[0], point[1])]
            if len(self.points) > 0:
                self.points = np.vstack((self.points, point_arr))
            else:
                self.points = np.array(point_arr)
        else:
            raise TypeError("Wrong type " + str(type(point)) + " to append to Shape")
        return self

    def extend(self, points):
        if (len(self.points) == 0):
            self.points = points
        else:
            if isinstance(points, Shape):            
                self.points = np.vstack((self.points, points.points))
            elif isinstance(points, (list, np.ndarray)):
                self.points = np.vstack((self.points, points))
            else:
                raise TypeError("Wrong type " + str(type(points)) + " to extend Shape with")
        return self

    def insert(self, i, item):
        """ Inserts a list of points. """
        if isinstance(item, Shape):
            self.points = np.insert(self.points, i, item.points, axis=0)
        elif isinstance(item, (list, np.ndarray)):
            if isinstance(item[0], Coord):
                item[0] = item[0].to_numpy_array()
            if len(item) > 1:
                if isinstance(item[1], Coord):
                    item[1] = item[1].to_numpy_array()
            self.points = np.insert(self.points, i, item, axis=0)
        elif isinstance(item, (Coord, tuple)):
            self.points = np.insert(self.points, i, [(item[0], item[1])], axis=0)
        else:
            raise TypeError("Wrong type " + str(type(item)) + " to extend Shape with")
        return self

    def is_empty(self):
        return self.__len__() <= 1

    def id_string(self):
        return '{} - hash {}'.format(self.__repr__(), self.hash_string)

    def create_segment_labels(self):
        labels = []
        for i, s1 in enumerate(self.segments()):
            labels.append(str(i))
        return labels


def ShapeParameter(restriction=None, preprocess=None, **kwargs):
    R = RestrictType(Shape) & restriction
    P = ProcessorTypeCast(Shape) + preprocess
    return ParameterDescriptor(restriction=R, preprocess=P, **kwargs)


# from spira.yevon.gdsii.group import Group
# from spira.yevon.gdsii.base import __LayerElement__
# from spira.yevon.process.physical_layer import PLayer
# class EdgeGenerator(Group, __LayerElement__):
#     """ Generates edge objects for each shape segment. """

#     shape = ShapeParameter()
#     internal_pid = StringParameter(default='no_pid', doc='A unique polygon ID to which the edge connects.')

#     def create_elements(self, elems):

#         for i, s in enumerate(self.shape.segments()):

#             shape = Shape(points=s)

#             L = RDD.GDSII.IMPORT_LAYER_MAP[self.layer]
#             width = RDD[L.process.symbol].MIN_SIZE

#             layer = PLayer(process=L.process, purpose=RDD.PURPOSE.PORT.OUTSIDE_EDGE_DISABLED)

#             elems += Edge(
#                 shape=[],
#                 line_shape=shape,
#                 layer=layer,
#                 internal_pid=self.internal_pid,
#                 width=width,
#                 transformation=self.transformation
#             )
            
#         return elems


def shape_edge_ports(shape, layer, local_pid='None', center=(0,0), loc_name=''):

    # FIXME: Integrate with edges.
    from spira.yevon.geometry.ports.port import Port
    from spira.yevon.process.gdsii_layer import Layer
    
    shape = shape.remove_straight_angles()
    # shape = shape.reverse_points()

    edges = PortList()

    xpts = list(shape.x_coords)
    ypts = list(shape.y_coords)

    n = len(xpts)

    xpts.append(xpts[0])
    ypts.append(ypts[0])

    clockwise = 0
    for i in range(0, n):
        clockwise += ((xpts[i+1] - xpts[i]) * (ypts[i+1] + ypts[i]))

    if layer.name == 'BBOX': bbox = True
    else: bbox = False

    layer = RDD.GDSII.IMPORT_LAYER_MAP[layer]

    for i in range(0, n):
        # name = 'E{}_{}'.format(i, layer.process.symbol)
        # name = 'E{}_{}_{}'.format(i, layer.process.symbol, shape.bbox_info.center)
        # print(loc_name)
        name = '{}E{}'.format(loc_name, i)
        # print(name)
        x = np.sign(clockwise) * (xpts[i+1] - xpts[i])
        y = np.sign(clockwise) * (ypts[i] - ypts[i+1])
        orientation = (np.arctan2(x, y) * constants.RAD2DEG)
        midpoint = [(xpts[i+1] + xpts[i])/2, (ypts[i+1] + ypts[i])/2]
        width = np.abs(np.sqrt((xpts[i+1] - xpts[i])**2 + (ypts[i+1]-ypts[i])**2))
        P = Port(
            name=name,
            process=layer.process,
            purpose=RDD.PURPOSE.PORT.OUTSIDE_EDGE_DISABLED,
            midpoint=midpoint,
            orientation=orientation,
            width=width,
            length=0.2,
            local_pid=local_pid
        )
        edges += P
    return edges
