import gdspy
import spira

from spira.kernel.elemental.polygons import PolygonAbstract
from spira.kernel.elemental.polygons import Polygons
from spira.kernel.elemental.polygons import UnionPolygons
from spira.kernel.utils import scale_polygon_up as spu
from spira.kernel.utils import scale_coord_down as scd


def Rectangle(point1, point2, **kwargs):
    rectangle = gdspy.Rectangle(point1, point2)

    ply = Polygons(polygons=spu(rectangle.polygons),
                   gdslayer=kwargs['layer'])

    return ply


def Circle(center, radius):
    circle = gdspy.Round(scd(center), radius,
                         inner_radius=0, initial_angle=0,
                         final_angle=0, number_of_points=6,
                         max_points=6, layer=100, datatype=0)

    layer = spira.Layer(name='Circle', number=circle.layers[0])
    ply = Polygons(polygons=spu(circle.polygons), gdslayer=layer)

    return ply


class Arc(PolygonAbstract):
    pass


class Cone(PolygonAbstract):
    pass


class CurveCone(PolygonAbstract):
    pass
