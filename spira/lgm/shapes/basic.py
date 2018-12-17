import gdspy
import spira
from spira import param
from spira.lgm.shapes.shape import __Shape__

from spira.gdsii.elemental.polygons import PolygonAbstract
from spira.gdsii.elemental.polygons import Polygons
from spira.gdsii.utils import scale_polygon_up as spu
from spira.gdsii.utils import scale_coord_down as scd
from spira.core.initializer import FieldInitializer


class __Rectangle__(gdspy.Rectangle, __Shape__):

    p1 = param.PointField()
    p2 = param.PointField()

    def __init__(self, **kwargs):

        __Shape__.__init__(self, **kwargs)
        gdspy.Rectangle.__init__(self,
            point1=self.p1,
            point2=self.p2,
            layer=self.gdslayer
        )

    def __repr__(self):
        return None

    def __str__(self):
        return self.__repr__()


class __Box__(gdspy.Rectangle, __Shape__):

    width = param.FloatField()
    height = param.FloatField()
    center = param.PointField()

    # TODO: Create a setter and getter for these parameters.
    p1 = param.DataField(fdef_name='create_point1')
    p2 = param.DataField(fdef_name='create_point2')

    def create_point1(self):
        x = self.center[0] - self.width/2
        y = self.center[1] - self.height/2
        return [x, y]

    def create_point2(self):
        x = self.center[0] + self.width/2
        y = self.center[1] + self.height/2
        return [x, y]

    def __init__(self, **kwargs):

        __Shape__.__init__(self, **kwargs)
        gdspy.Rectangle.__init__(self,
            point1=self.p1,
            point2=self.p2,
            layer=self.gdslayer
        )

    def __repr__(self):
        return None

    def __str__(self):
        return self.__repr__()


class __Circle__(gdspy.Round, __Shape__):

    center = param.PointField()
    radius = param.FloatField()

    def __init__(self, **kwargs):

        __Shape__.__init__(self, **kwargs)
        gdspy.Round.__init__(self, self.center, self.radius,
                             inner_radius=0, initial_angle=0,
                             final_angle=0, number_of_points=6,
                             max_points=6)

    def __repr__(self):
        return None

    def __str__(self):
        return self.__repr__()


class RectangleShape(__Rectangle__):

    def create_points(self, points):
        return self.polygons


class BoxShape(__Box__):

    def create_points(self, points):
        return self.polygons


class CircleShape(__Circle__):

    def create_points(self, points):
        return self.polygons


def Rectangle(shape):
    return spira.Polygons(polygons=shape.points, gdslayer=shape.gdslayer)


def Box(shape):
    return spira.Polygons(polygons=shape.points, gdslayer=shape.gdslayer)


def Circle(shape):
    return spira.Polygons(polygons=shape.points)


# def Box( width, height, center=(0,0), **kwargs):
#     pass
#     p1 = [center[0]-width/2, center[1]-height/2]
#     p2 = [center[0]+width/2, center[1]+height/2]
#     rectangle = gdspy.Rectangle(p1, p2)
#
#     if 'gdslayer' in kwargs:
#         layer = kwargs['gdslayer']
#     else:
#         layer = spira.Layer(name='Box', number=99)
#
#     ply = Polygons(polygons=rectangle.polygons, gdslayer=layer)
# #     ply = Polygons(polygons=spu(rectangle.polygons), gdslayer=layer)
#
#     return ply


# def Rectangle(point1, point2, **kwargs):
#     rectangle = gdspy.Rectangle(point1, point2)

#     if 'gdslayer' in kwargs:
#         layer = kwargs['gdslayer']
#     else:
#         layer = spira.Layer(name='Box', number=99)

#     # ply = Polygons(polygons=spu(rectangle.polygons), gdslayer=layer)
#     ply = Polygons(polygons=rectangle.polygons, gdslayer=layer)

#     return ply


# def Circle(center, radius, layer):
#     circle = gdspy.Round(center, radius,
#     # circle = gdspy.Round(scd(center), radius,
#                          inner_radius=0, initial_angle=0,
#                          final_angle=0, number_of_points=6,
#                          max_points=6)
#                         #  layer=layer.number,
#                         #  datatype=65)

#     ll = spira.Layer(name='Circle', number=layer.number, datatype=65)
#     # ll = spira.Layer(name='Circle', number=layer.number)
#     ply = Polygons(polygons=circle.polygons, gdslayer=ll)
#     # ply = Polygons(polygons=spu(circle.polygons), gdslayer=ll)

#     return ply


if __name__ == '__main__':

    box = Box(p1=[0,0], p2=[1,1])
    print(box.points)






