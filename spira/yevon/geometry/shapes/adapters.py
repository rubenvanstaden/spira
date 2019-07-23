import numpy as np
from copy import deepcopy

from spira.yevon.geometry.shapes.shape import Shape, ShapeParameter
from spira.yevon.geometry.line import line_from_two_points
from spira.yevon.geometry.vector import vector_from_two_points
from spira.yevon.geometry.coord import Coord
from spira.yevon.utils.geometry import intersection, lines_cross, lines_coincide, sort_points_on_line, points_unique
from spira.core.parameters.variables import *


class __ShapeAdapter__(Shape):

    original_shape = ShapeParameter()

    def __init__(self, original_shape, **kwargs):
        super().__init__(original_shape=original_shape, **kwargs)

    def move(self, position):
        self.original_shape = self.original_shape.move_copy(position)
        return self


class ShapeConnected(__ShapeAdapter__):
    """  """

    edges = DictParameter()
    clip_shape = ShapeParameter(doc='Edge shape that clipes the original shape for electrical connection.')

    def create_segment_labels(self):
        labels = []
        for i, s1 in enumerate(self.segments()):
            labels.append(str(i))
        for ply, edges in self.edges.items():
            for edge in edges:
                bbox_shape = edge.shape.transform(edge.transformation).snap_to_grid()
                for i, s1 in enumerate(self.segments()):
                    s1 = Shape(points=s1).snap_to_grid()
                    s1 = s1.points[0]
                    s1 = [tuple(c) for c in s1]
                    for s2 in bbox_shape.segments():
                        s2 = [tuple(c) for c in s2]
                        if set(s1) == set(s2):
                            labels[i] = edge.external_pid
        return labels

    def create_points(self, points):

        if self.clip_shape.is_empty() is False:
            new_points = []
            for i, s in enumerate(self.original_shape.segments()):
                s1_inter = []
                new_points += [s[0]]
                for c in self.clip_shape.points:
                    if c not in self.original_shape:
                        segment_line = line_from_two_points(s[0], s[1])
                        if segment_line.is_on_line(coordinate=c):
                            s1_inter.append(c)

                if len(s1_inter) > 0:
                    line = np.concatenate((s, s1_inter))
                    pl = sort_points_on_line(line)
                    new_points += pl[0:-1]

            points = [Coord(p[0], p[1]) for p in new_points]
            points = points_unique(points)
            points = [c.to_list() for c in points]
        else:
            points = self.original_shape.points

        return points


