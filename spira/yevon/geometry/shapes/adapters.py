import numpy as np
from copy import deepcopy

# from spira.yevon.geometry.edges.edge_list import EdgeListParameter
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
        self.original_shape = self.original_shape.movecopy(position)
        return self


class ShapeConnected(__ShapeAdapter__):
    """  """

    # edges = EdgeListParameter()
    edges = DictParameter()
    overlapping_shape = ShapeParameter(doc='Shape containing the edge coordinates of the original shape intersecting with other shapes with equal layer.')

    def create_segment_labels(self):

        labels = []

        for i, s1 in enumerate(self.segments()):
            labels.append(str(i))

        for ply, edges in self.edges.items():
            for edge in edges:
                bbox_shape = edge.bbox_info.bounding_box().snap_to_grid()
                # bbox_shape = e.bbox_info.bounding_box()
                # print(bbox_shape.segments())
                # print(self.segments())
                for i, s1 in enumerate(self.segments()):
                    # print(s1)
                    s1 = Shape(points=s1).snap_to_grid()
                    s1 = s1.points[0]
                    # print(s1)
                    for s2 in bbox_shape.segments():
                        s1 = [tuple(c) for c in s1]
                        s2 = [tuple(c) for c in s2]
                        # if (np.array(s1) == np.array(s2)).all():
                        # if (sorted(s1) == sorted(s2)).all():
                        # print(s1)
                        # print(s2)
                        if set(s1) == set(s2):
                            labels[i] = edge.shape.hash_string
                            # print(labels[i])
                #             print('YES SEGMENT')
                #     print('----')
                # print('')

        return labels

    def create_points(self, points):

        if len(self.overlapping_shape) == 0:
            points = self.original_shape.points
        else:
            new_points = []
            for i, s in enumerate(self.original_shape.segments()):
                s1_inter = []
                new_points += [s[0]]
                for c in self.overlapping_shape.points:
                    if c not in self.original_shape:
                        # print(c)
                        segment_line = line_from_two_points(s[0], s[1])
                        if segment_line.is_on_line(coordinate=c):
                            # print('jkfbjwkebkwefb')
                            s1_inter.append(c)

                if len(s1_inter) > 0:
                    line = np.concatenate((s, s1_inter))
                    pl = sort_points_on_line(line)
                    new_points += pl[0:-1]
                # new_points += [s[1]]

            points = new_points
            points = [Coord(p[0], p[1]) for p in points]
            points = points_unique(points)
            points = [c.to_list() for c in points]

            # if len(points) > 0:
            #     print(points)
            #     print(len(self.overlapping_shape.points), len(points))
            #     print('')

        return points


