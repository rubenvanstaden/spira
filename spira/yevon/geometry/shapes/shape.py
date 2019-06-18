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
from spira.yevon.geometry.coord import CoordField, Coord
from spira.core.parameters.initializer import FieldInitializer
from spira.core.parameters.processors import ProcessorTypeCast
from spira.core.parameters.descriptor import DataFieldDescriptor, DataField
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = ['Shape', 'ShapeField', 'PointArrayField', 'shape_edge_ports']


class PointArrayField(DataFieldDescriptor):
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


class __Shape__(Transformable, FieldInitializer):

    center = CoordField()
    clockwise = BoolField(default=False)
    points = PointArrayField(fdef_name='create_points')

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
        pts = self.points[0]
        T = np.roll(np.roll(pts, 1, 1), 1, 0)
        return sum(abs(np.diff(pts * T, 1, 1))) * 0.5

    @property
    def hash_string(self):
        import hashlib
        pts = np.array([self.points])
        hash_key = np.sort([hashlib.sha1(p).digest() for p in pts])
        return str(hash_key)

    @property
    def count(self):
        """ Number of points in the shape """
        return self.__len__()

    @property
    def bbox_info(self):
        return bbox_info.bbox_info_from_numpy_array(self.points)

    @property
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

    # def transform_copy(self, transformation):
    #     S = deepcopy(self)
    #     S.points = transformation.apply_to_array(self.points)
    #     return S

    def id_string(self):
        return self.__str__()


class Shape(__Shape__):
    """ 
    A shape is a geometrical object that
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
        # return np.prod(sum(self.points == np.array([point[0], point[1]]), 0))
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

    def is_empty(self):
        return self.__len__() <= 1
        

def ShapeField(restriction=None, preprocess=None, **kwargs):
    R = RestrictType(Shape) & restriction
    P = ProcessorTypeCast(Shape) + preprocess
    return DataFieldDescriptor(restrictions=R, preprocess=P, **kwargs)


from spira.yevon.process.gdsii_layer import Layer
from spira.yevon.geometry.ports.port import Port
def shape_edge_ports(shape, layer, local_pid='None'):

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

    edges = PortList()
    for i in range(0, n):
        name = '{}_e{}'.format(layer.name, i)
        x = np.sign(clockwise) * (xpts[i+1] - xpts[i])
        y = np.sign(clockwise) * (ypts[i] - ypts[i+1])
        orientation = (np.arctan2(x, y) * constants.RAD2DEG)
        midpoint = [(xpts[i+1] + xpts[i])/2, (ypts[i+1] + ypts[i])/2]
        width = np.abs(np.sqrt((xpts[i+1] - xpts[i])**2 + (ypts[i+1]-ypts[i])**2))
        layer = RDD.GDSII.IMPORT_LAYER_MAP[layer]
        P = Port(
            name=name,
            bbox=bbox,
            locked=True,
            process=layer.process,
            purpose=RDD.PURPOSE.PORT.EDGE_DISABLED,
            midpoint=midpoint,
            orientation=orientation,
            width=width,
            length=0.2,
            local_pid=local_pid
        )
        edges += P
    return edges
