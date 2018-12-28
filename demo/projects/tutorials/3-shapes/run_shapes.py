import spira
import numpy as np
from spira import param
from spira import shapes


class BasicTriangle(shapes.Shape):

    a = param.FloatField(default=2)
    b = param.FloatField(default=0.5)
    c = param.FloatField(default=1)

    def create_points(self, points):
        p1 = [0, 0]
        p2 = [p1[0]+self.b, p1[1]]
        p3 = [p1[0], p1[1]+self.a]
        pts = np.array([p1, p2, p3])
        points = [pts]
        return points


class TriangleShape(BasicTriangle):

    def create_points(self, points):
        points = super().create_points(points)
        triangle = BasicTriangle(a=self.a, b=self.b, c=self.c)
        triangle.reflect()
        points.extend(triangle.points)
        return points


class ArrowShape(TriangleShape):

    # TODO: Implement point_list properties.
    def create_points(self, points):
        points = super().create_points(points)
        box = shapes.BoxShape(width=self.b/2, height=3*self.c)
        box.move(pos=(0,-self.c/2))
        points.extend(box.points)
        return points


if __name__ == '__main__':

    cell = spira.Cell(name='TriangleCell')

    s1 = ArrowShape()
    s1.apply_merge
    p1 = spira.Polygons(shape=s1, gdslayer=spira.Layer(number=13))

    s2 = ArrowShape(a=4)
    s2.apply_merge
    s2.rotate(angle=180)
    s2.move(pos=(10,0))
    p2 = spira.Polygons(shape=s2, gdslayer=spira.Layer(number=15))

    cell += p1
    cell += p2

    cell.output()

