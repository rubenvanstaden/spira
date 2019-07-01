import spira.all as spira
from spira.yevon.geometry import shapes

from spira.technologies.mit.process import RDD


el = spira.ElementList()
p1 = spira.Rectangle(p1=(0, 0), p2=(4, 10), layer=RDD.PLAYER.M5.METAL)
# p2 = spira.Rectangle(p1=(3, 4), p2=(8, 6), layer=RDD.PLAYER.M5.METAL)
pts = [(3,4), (3,6), (8,6), (8,15), (10,15), (10,6), (14,6), (14,4)]
s1 = shapes.Shape(points=pts)
s1.move(pos=(-13,0))
p2 = spira.Polygon(shape=s1, layer=RDD.PLAYER.M5.METAL)
el = [p1, p2]


S = p1.shape.intersections(p2.shape)


# if self.original_shape.intersection(ply.shape):
#     for edge in edges:
#         edge = deepcopy(edge)
#         for i, s in enumerate(self.original_shape.segments()):
#             segment_line = line_from_two_points(s[0], s[1])
#             edge_line = []
#             for c in edge.outside.bbox_info.bounding_box().snap_to_grid():
#                 if segment_line.is_on_line(coordinate=c):
#                     if c not in self.original_shape:
#                         edge_line.append(c)
#                         # self.original_shape.insert(i=i+1, item=c)

#             if len(edge_line) > 0:
#                 ll = edge_line
#                 if len(edge_line) > 1:
#                     segment_vector = vector_from_two_points(point1=s[0], point2=s[1])
#                     endpoint_vector = vector_from_two_points(point1=ll[0], point2=ll[1])
#                     if segment_vector.orientation == endpoint_vector.orientation:
#                         corner_points = [ll[0], ll[1]]
#                     else:
#                         corner_points = [ll[1], ll[0]]
#                 else:
#                     corner_points = [ll[0]]
#                 self.original_shape.insert(i=i+1, item=corner_points)



print(p1.points)
print('----------------------------------------')
print(S.points)


D = spira.Cell(name='Device', elements=el)
D.gdsii_output()
