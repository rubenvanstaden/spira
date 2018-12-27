import pytest
import spira
from spira import param
from spira import shapes


UM = 1e12


def test_shapes_basic():

    rect_shape = shapes.RectangleShape(p1=[0,0], p2=[2,2])
    assert all([a == b for a, b in zip(rect_shape.p1, [0,0])])
    assert all([a == b for a, b in zip(rect_shape.p2, [2,2])])
    assert rect_shape.area == 4*UM
    assert rect_shape.orientation == 1

    box_shape = shapes.BoxShape(center=(0,0), width=2, height=2)
    assert box_shape.area == 4*UM
    assert box_shape.orientation == -1
    assert box_shape.width == 2
    assert box_shape.height == 2

    circle_shape = shapes.CircleShape(center=(0,0), box_size=(4,4))
    # circle_shape = shapes.CircleShape(center=(0,0), radius=2)
    assert all([a == b for a, b in zip(circle_shape.center, [0,0])])
    assert int(circle_shape.area/UM) == 12
    # assert circle_shape.radius == 2


def test_shape_triangle():

    class Triangle(shapes.Shape):
        """ Right triangle """

        a = param.FloatField(default=1)
        b = param.FloatField(default=1)
        c = param.FloatField(default=1)

        def create_points(self, points):

            p1 = [0, 0]
            p2 = [p1[0]+self.b, p1[1]]
            p3 = [p1[0], p1[1]+self.a]

            points = [[p1, p2, p3]]

            return points

    t1 = Triangle()
    assert t1.area == 0.5*UM

    t2 = Triangle(a=2)
    assert t2.area == 1*UM
  
    t3 = Triangle(a=2, b=2)
    assert t3.area == 2*UM

    t4 = Triangle(a=2, b=2, c=2)
    assert t4.area == 2*UM
