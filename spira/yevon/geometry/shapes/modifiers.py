from spira.yevon.structure.edges import EdgeListField
from spira.yevon.geometry.shapes.shape import Shape, ShapeField
from spira.core.parameters.variables import ListField
from spira.yevon.geometry.line import line_from_two_points

from copy import deepcopy
import numpy as np


class __ShapeModifier__(Shape):

    original_shape = ShapeField()

    def __init__(self, original_shape, **kwargs):
        super(__ShapeModifier__, self).__init__(original_shape=original_shape, **kwargs)

    def move(self, position):
        self.original_shape = self.original_shape.move_copy(position)
        return self


class ShapeConnected(__ShapeModifier__):
    """  """

    edges = EdgeListField()
    segment_labels = ListField(fdef_name='create_segment_labels')

    def create_segment_labels(self):

        sl = []
        for edge in self.edges:
            edge = deepcopy(edge)
            edge = edge.outside.transform(edge.transformation)
            for i, s1 in enumerate(self.segments):

                bbox = edge.bbox_info.bounding_box().snap_to_grid()

                print(s1)
                # print(bbox.segments)
                # print('')

                sl.append(str(i))
                # for s2 in edge.shape.segments:
                for s2 in bbox.segments:
                    print(s2)
                    if (np.array(s1) == np.array(s2)).all():
                        sl[i] = edge.shape.hash_string
                print('')

                # segment_line = line_from_two_points(s[0], s[1])
                # count = 0
                # sl.append(str(i))
                # print(s[0], s[1])
                # # for c in edge.outside.bbox_info.bounding_box().snap_to_grid():
                # for c in edge.points:
                #     print(c)
                #     if segment_line.is_on_line(coordinate=c):
                #         count += 1
                #         # NOTE: I believe this is the wrong has string.
                #         # We want to use the hash of the intersected shape.
                #         # sl.append(self.hash_string)
                #     # else:
                # print(count)
                # if count == 2:
                #     # sl[i] = self.hash_string
                #     sl[i] = edge.shape.hash_string
                # print('')
        return sl

    def create_points(self, points):

        for edge in self.edges:
            edge = deepcopy(edge)
            for i, s in enumerate(self.original_shape.segments):
                segment_line = line_from_two_points(s[0], s[1])
                for c in edge.outside.bbox_info.bounding_box().snap_to_grid():
                    if segment_line.is_on_line(coordinate=c):
                        if c not in self.original_shape:
                            self.original_shape.insert(i=i+1, item=c)

        self.original_shape.clockwise()
        points = self.original_shape.points

        return points

