import numpy as np

from .field.layer_list import LayerListProperty
from .field.typed_point import PointField
from .restrictions import RestrictType
from .variables import *

from spira.core.descriptor import DataField
from spira.core.descriptor import FunctionField
from spira.core.descriptor import DataFieldDescriptor


def CoordField(**kwargs):
    from spira.lgm.coord import Coord
    if 'default' not in kwargs:
        kwargs['default'] = Coord(0,0)
    R = RestrictType(Coord)
    return DataFieldDescriptor(restrictions=R, **kwargs)
    

def TransformationField(name='noname', number=0, datatype=0, **kwargs):
    from spira.gdsii.tranformation import Tranform
    # if 'default' not in kwargs:
    #     kwargs['default'] = Layer(name=name, number=number, datatype=datatype, **kwargs)
    R = RestrictType(Tranform)
    return DataFieldDescriptor(restrictions=R, **kwargs)


def LayerField(name='noname', number=0, datatype=0, **kwargs):
    from spira.layer import Layer
    if 'default' not in kwargs:
        kwargs['default'] = Layer(name=name, number=number, datatype=datatype, **kwargs)
    R = RestrictType(Layer)
    return DataFieldDescriptor(restrictions=R, **kwargs)


def ColorField(red=0, green=0, blue=0, **kwargs):
    from spira.visualization.color import Color
    if 'default' not in kwargs:
        kwargs['default'] = Color(red=0, green=0, blue=0, **kwargs)
    R = RestrictType(Color)
    return DataFieldDescriptor(restrictions=R, **kwargs)


def LabelField(position=[[], []], **kwargs):
    from spira.gdsii.elemental.label import Label
    if 'default' not in kwargs:
        kwargs['default'] = Label(position=position)
    R = RestrictType(Label)
    return DataFieldDescriptor(restrictions=R, **kwargs)


def PortField(midpoint=[0, 0], **kwargs):
    from spira.gdsii.elemental.port import Port
    if 'default' not in kwargs:
        kwargs['default'] = Port(midpoint=midpoint)
    R = RestrictType(Port)
    return DataFieldDescriptor(restrictions=R, **kwargs)


def TermField(midpoint=[0, 0], **kwargs):
    from spira.gdsii.elemental.term import Term
    if 'default' not in kwargs:
        kwargs['default'] = Term(midpoint=midpoint)
    R = RestrictType(Term)
    return DataFieldDescriptor(restrictions=R, **kwargs)


def ShapeField(points=[], doc='', **kwargs):
    from spira.lgm.shapes.shape import Shape
    if 'default' not in kwargs:
        kwargs['default'] = Shape(points, doc=doc)
    R = RestrictType(Shape)
    return DataFieldDescriptor(restrictions=R, **kwargs)


def CellField(name=None, elementals=None, ports=None, library=None, **kwargs):
    from spira.gdsii.cell import Cell
    if 'default' not in kwargs:
        kwargs['default'] = Cell(name=name, elementals=elementals, library=library)
    R = RestrictType(Cell)
    return DataFieldDescriptor(restrictions=R, **kwargs)


def PurposeLayerField(name='', datatype=0, symbol='', **kwargs):
    from spira.rdd.layer import PurposeLayer
    if 'default' not in kwargs:
        kwargs['default'] = PurposeLayer(name=name, datatype=datatype, symbol='')
    R = RestrictType(PurposeLayer)
    return DataFieldDescriptor(restrictions=R, **kwargs)


def PhysicalLayerField(layer=None, purpose=None, **kwargs):
    from spira.rdd.layer import PhysicalLayer
    if 'default' not in kwargs:
        kwargs['default'] = PhysicalLayer(layer=layer, purpose=purpose)
    R = RestrictType(PhysicalLayer)
    return DataFieldDescriptor(restrictions=R, **kwargs)


def PolygonField(shape=[[], []], **kwargs):
    from spira.gdsii.elemental.polygons import Polygons
    if 'default' not in kwargs:
        kwargs['default'] = Polygons(shape=shape)
    R = RestrictType(Polygons)
    return DataFieldDescriptor(restrictions=R, **kwargs)
    

def DesignRuleField(shape=[[], []], **kwargs):
    from spira.lrc.rules import __DesignRule__
    R = RestrictType(__DesignRule__)
    return DataFieldDescriptor(restrictions=R, **kwargs)


class ElementalListField(DataFieldDescriptor):
    from spira.core.lists import ElementList
    __type__ = ElementList

    def __init__(self, default=[], **kwargs):
        kwargs['default'] = self.__type__(default)
        kwargs['restrictions'] = RestrictType([self.__type__])
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
        else:
            raise TypeError("Invalid type in setting value " +
                            "of {} (expected {}): {}"
                            .format(self.__class__, type(value)))

        obj.__store__[self.__name__] = [value.x, value.y]


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
        return points

    def __set__(self, obj, points):
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
            










