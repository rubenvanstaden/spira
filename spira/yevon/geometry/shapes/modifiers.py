from spira.yevon.geometry.edges.edge_list import EdgeListField
from spira.yevon.geometry.shapes.shape import Shape, ShapeField
from spira.yevon.geometry.line import line_from_two_points
from spira.yevon.geometry.vector import vector_from_two_points
from spira.yevon.geometry.coord import Coord
from spira.yevon.utils.geometry import intersection, lines_cross, lines_coincide, sort_points_on_line, points_unique
from spira.core.parameters.variables import *

from copy import deepcopy
import numpy as np


class __ShapeModifier__(Shape):

    original_shape = ShapeField()

    def __init__(self, original_shape, **kwargs):
        super().__init__(original_shape=original_shape, **kwargs)

    def move(self, position):
        self.original_shape = self.original_shape.move_copy(position)
        return self


class ShapeConnected(__ShapeModifier__):
    """  """

    # edges = EdgeListField()
    edges = DictField()
    overlapping_shape = ShapeField(doc='Shape containing the edge coordinates of the original shape intersecting with other shapes with equal layer.')

    def create_segment_labels(self):

        labels = []

        print('wejfbkjfwbjbwekfbwefjkbekfwk')
        
        for i, s1 in enumerate(self.segments()):
            labels.append(str(i))

        for ply, edges in self.edges.items():
            for edge in edges:
                e = deepcopy(edge).outside.transform(edge.transformation)
                # e = edge.outside
                for i, s1 in enumerate(self.segments()):
                    bbox_shape = e.bbox_info.bounding_box().snap_to_grid()
                    for s2 in bbox_shape.segments():
                        if (np.array(s1) == np.array(s2)).all():
                            labels[i] = e.shape.hash_string

        return labels

    def create_points(self, points):

        print('Points:')
        if len(self.overlapping_shape) == 0:
            points = self.original_shape.points
        else:        
            new_points = []
            for i, s in enumerate(self.original_shape.segments()):
                s1_inter = []
                new_points += [s[0]]
                for c in self.overlapping_shape.points:
                    if c not in self.original_shape:
                        segment_line = line_from_two_points(s[0], s[1])
                        if segment_line.is_on_line(coordinate=c):
                            s1_inter.append(c)
    
                if len(s1_inter) > 0:
                    line = np.concatenate((s, s1_inter))
                    pl = sort_points_on_line(line)
                    new_points += pl[0:-1]
                new_points += [s[1]]
    
            points = new_points
            points = [Coord(p[0], p[1]) for p in points]
            points = points_unique(points)

        return points


