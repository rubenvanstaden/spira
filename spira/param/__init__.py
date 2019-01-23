from .field.typed_string import StringField
# from .field.typed_integer import IntegerField
# from .field.typed_float import FloatField
from .field.typed_bool import BoolField
from .field.typed_list import ListField
from .field.layer_list import LayerListProperty
from .field.typed_color import ColorField
from .field.typed_point import PointField

from spira.core.descriptor import DataField
from spira.core.descriptor import DataFieldDescriptor
from spira.core.descriptor import FunctionField

import numpy as np


class MidPointField(DataFieldDescriptor):
    from .field.point import Point
    __type__ = Point

    def __init__(self, default=Point(0,0), **kwargs):
        if isinstance(default, self.__type__):
            kwargs['default'] = [default.x, default.y]
        elif isinstance(default, (list, set, tuple, np.ndarray)):
            kwargs['default'] = default
        super().__init__(**kwargs)

    def get_stored_value(self, obj):
        value = obj.__store__[self.__name__]
        if not isinstance(value, (list, set, tuple, np.ndarray)):
            raise ValueError('Correct MidPoint type to retreived.')
        return list(value)

    def __set__(self, obj, value):
        if isinstance(value, self.__type__):
            value = self.__type__()
        elif isinstance(value, (list, set, tuple, np.ndarray)):
            value = self.__type__(value[0], value[1])
            # value = self.__type__(value)
        else:
            raise TypeError("Invalid type in setting value " +
                            "of {} (expected {}): {}"
                            .format(self.__class__, type(value)))

        # if (value.x > 0) and (value.y > 0):
        #     if (value.x/100 < 1.0) and (value.y/100 < 1.0):
        #         from spira.gdsii.utils import SCALE_UP
        #         from spira.gdsii.utils import SCALE_DOWN
        #         value.x = SCALE_UP*value.x
        #         value.y = SCALE_UP*value.y

        obj.__store__[self.__name__] = [value.x, value.y]


def PolygonField(shape=[]):
    from spira.gdsii.elemental.polygons import Polygons
    F = Polygons(shape)
    return DataFieldDescriptor(default=F)


def ShapeField(points=[]):
    from spira.lgm.shapes.shape import Shape
    F = Shape(points)
    return DataFieldDescriptor(default=F)


def LayerField(name='', number=0, datatype=0, **kwargs):
    from spira.gdsii.layer import Layer
    F = Layer(name=name, number=number, datatype=datatype, **kwargs)
    return DataFieldDescriptor(default=F, **kwargs)


# def FloatField(default=0.0, **kwargs):
def FloatField(**kwargs):
    from .variables import FLOAT
    return DataFieldDescriptor(constraint=FLOAT, **kwargs)


def IntegerField(**kwargs):
    from .variables import INTEGER
    return DataFieldDescriptor(constraint=INTEGER, **kwargs)

def CellField(name=None, elementals=None, library=None):
    from spira.gdsii.cell import Cell
    F = Cell(name=name, elementals=elementals, library=library)
    return DataFieldDescriptor(default=F)


def PhysicalLayerField(layer=None, purpose=None):
    from spira.rdd.layer import PhysicalLayer
    F = PhysicalLayer(layer=layer, purpose=purpose)
    return DataFieldDescriptor(default=F)


class ElementListField(DataFieldDescriptor):
    from spira.core.lists import ElementList
    __type__ = ElementList

    def __init__(self, default=[], **kwargs):
        kwargs['default'] = self.__type__(default)
        super().__init__(**kwargs)

    def __repr__(self):
        return ''

    def __str__(self):
        return ''

    def call_param_function(self, obj):
        f = self.get_param_function(obj)
        value = f(self.__type__())
        if value is None:
            value = self.__type__()
        obj.__store__[self.__name__] = value
        return value


class PointArrayField(DataFieldDescriptor):
    import numpy as np
    __type__ = np.array([])

    def call_param_function(self, obj):
        f = self.get_param_function(obj)
        value = f([])
        if value is None:
            value = self.__operations__([])
        else:
            value = self.__operations__(value)
        obj.__store__[self.__name__] = value
        return value 
        # if (value is None):
        #     value = self.__process__([])
        # else:
        #     value = self.__process__([c.convert_to_array() if isinstance(c, Coord) else c for c in value])
        # return value 

    def __operations__(self, points):
        # from spira.gdsii.utils import scale_polygon_up as spu
        # return spu(points) 
        return points

    def __set__(self, obj, points):
        # from spira.gdsii.utils import scale_polygon_up as spu
        # pp = spu(self.__operations__(points))
        # obj.__store__[self.__name__] = pp
        obj.__store__[self.__name__] = points
    
    # def __process__(self, points):
    #     if isinstance(points, Shape):
    #         return array(points.points)
    #     elif isinstance(points, (list, ndarray)):
    #         if len(points):
    #             element = points[0]
    #             if isinstance(element, (ndarray, list)):
    #                 points_as_array = array(points, copy=False)
    #             else:
    #                 points_as_array = array([(c[0], c[1]) for c in points])
    #             return points_as_array
    #         else:
    #             return ndarray((0, 2))
    #     elif isinstance(points, Coord2):
    #             return array([[points.x, points.y]])
    #     elif isinstance(points, tuple):
    #             return array([[points[0], points[1]]])
    #     else:
    #             raise TypeError("Invalid type of points in setting value of PointsDefinitionProperty: " + str(type(points)))
    
    # def __set__(self, obj, points):
    #     points = self.__process__(points)
    #     self.__externally_set_property_value_on_object__(obj, points)
            

class PortListField(DataFieldDescriptor):
    pass
    # from spira.gdsii.lists.port_list import PortList
    # __type__ = PortList

    # def __init__(self, default=[], **kwargs):
    #     kwargs['default'] = self.__type__(default)
    #     super().__init__(**kwargs)

    # def call_param_function(self, obj):
    #     f = self.get_param_function(obj)
    #     value = f(self.__type__())
    #     if value is None:
    #         value = self.__type__()
    #     obj.__store__[self.__name__] = value
    #     return value












