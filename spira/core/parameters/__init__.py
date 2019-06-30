# import numpy as np

# from .variables import *

# from spira.core.parameters.descriptor import Parameter
# from spira.core.parameters.descriptor import FunctionParameter
# from spira.core.parameters.descriptor import ParameterDescriptor
# from spira.core.parameters.restrictions import RestrictType


# # def CoordParameter(**kwargs):
# #     from spira.yevon.geometry.coord import Coord
# #     if 'default' not in kwargs:
# #         kwargs['default'] = Coord(0,0)
# #     R = RestrictType(Coord)
# #     return ParameterDescriptor(restrictions=R, **kwargs)
    

# # def TransformationParameter(name='noname', number=0, datatype=0, **kwargs):
# #     from spira.core.transformation import Transform
# #     # if 'default' not in kwargs:
# #     #     kwargs['default'] = Layer(name=name, number=number, datatype=datatype, **kwargs)
# #     R = RestrictType(Transform)
# #     return ParameterDescriptor(restrictions=R, **kwargs)


# def LayerParameter(name='noname', number=0, datatype=0, **kwargs):
#     from spira.yevon.layer import Layer
#     if 'default' not in kwargs:
#         kwargs['default'] = Layer(name=name, number=number, datatype=datatype, **kwargs)
#     R = RestrictType(Layer)
#     return ParameterDescriptor(restrictions=R, **kwargs)


# def ColorParameter(red=0, green=0, blue=0, **kwargs):
#     from spira.yevon.visualization.color import Color
#     if 'default' not in kwargs:
#         kwargs['default'] = Color(red=0, green=0, blue=0, **kwargs)
#     R = RestrictType(Color)
#     return ParameterDescriptor(restrictions=R, **kwargs)


# def LabelParameter(position=[[], []], **kwargs):
#     from spira.yevon.gdsii.label import Label
#     if 'default' not in kwargs:
#         kwargs['default'] = Label(position=position)
#     R = RestrictType(Label)
#     return ParameterDescriptor(restrictions=R, **kwargs)


# def PortParameter(midpoint=[0, 0], **kwargs):
#     # from spira.yevon.gdsii.port import Port
#     from spira.yevon.geometry.ports.port import Port
#     if 'default' not in kwargs:
#         kwargs['default'] = Port(midpoint=midpoint)
#     R = RestrictType(Port)
#     return ParameterDescriptor(restrictions=R, **kwargs)


# def TermParameter(midpoint=[0, 0], **kwargs):
#     from spira.yevon.gdsii.term import Term
#     if 'default' not in kwargs:
#         kwargs['default'] = Port(midpoint=midpoint)
#     R = RestrictType(Term)
#     return ParameterDescriptor(restrictions=R, **kwargs)


# def ShapeParameter(points=[], doc='', **kwargs):
#     from spira.yevon.geometry.shapes.shape import Shape
#     if 'default' not in kwargs:
#         kwargs['default'] = Shape(points, doc=doc)
#     R = RestrictType(Shape)
#     return ParameterDescriptor(restrictions=R, **kwargs)


# # def CellParameter(name=None, elements=None, ports=None, library=None, **kwargs):
# #     from spira.yevon.gdsii.cell import Cell
# #     if 'default' not in kwargs:
# #         kwargs['default'] = Cell(name=name, elements=elements, library=library)
# #     R = RestrictType(Cell)
# #     return ParameterDescriptor(restrictions=R, **kwargs)


# def PurposeLayerParameter(name='', datatype=0, symbol='', **kwargs):
#     from spira.yevon.process.layer import PurposeLayer
#     if 'default' not in kwargs:
#         kwargs['default'] = PurposeLayer(name=name, datatype=datatype, symbol='')
#     R = RestrictType(PurposeLayer)
#     return ParameterDescriptor(restrictions=R, **kwargs)


# def PhysicalLayerParameter(layer=None, purpose=None, **kwargs):
#     from spira.yevon.process.layer import PhysicalLayer
#     if 'default' not in kwargs:
#         kwargs['default'] = PhysicalLayer(layer=layer, purpose=purpose)
#     R = RestrictType(PhysicalLayer)
#     return ParameterDescriptor(restrictions=R, **kwargs)


# def PolygonParameter(shape=[[], []], **kwargs):
#     from spira.yevon.gdsii.polygon import Polygon
#     if 'default' not in kwargs:
#         kwargs['default'] = Polygon(shape=shape)
#     R = RestrictType(Polygon)
#     return ParameterDescriptor(restrictions=R, **kwargs)
    

# def DesignRuleParameter(shape=[[], []], **kwargs):
#     from spira.lrc.rules import __DesignRule__
#     R = RestrictType(__DesignRule__)
#     return ParameterDescriptor(restrictions=R, **kwargs)


# class ElementListParameter(ParameterDescriptor):
#     from spira.yevon.gdsii.elem_list import ElementList
#     __type__ = ElementList

#     def __init__(self, default=[], **kwargs):
#         kwargs['default'] = self.__type__(default)
#         kwargs['restrictions'] = RestrictType([self.__type__])
#         super().__init__(**kwargs)

#     def __repr__(self):
#         return ''

#     def __str__(self):
#         return ''

#     def call_param_function(self, obj):
#         f = self.get_param_function(obj)
#         value = f(self.__type__())
#         if value is None:
#             value = self.__type__()
#         obj.__store__[self.__name__] = value
#         return value


# # class MidPointParameter(ParameterDescriptor):
# #     from spira.yevon.geometry.coord import Coord
# #     __type__ = Coord

# #     def __init__(self, default=Coord(0,0), **kwargs):
# #         if isinstance(default, self.__type__):
# #             kwargs['default'] = [default.x, default.y]
# #         elif isinstance(default, (list, set, tuple, np.ndarray)):
# #             kwargs['default'] = default
# #         super().__init__(**kwargs)

# #     def __get_parameter_value__(self, obj):
# #         value = obj.__store__[self.__name__]
# #         if not isinstance(value, (list, set, tuple, np.ndarray)):
# #             raise ValueError('Correct MidPoint type to retreived.')
# #         return list(value)

# #     def __set__(self, obj, value):
# #         if isinstance(value, self.__type__):
# #             value = self.__type__()
# #         elif isinstance(value, (list, set, tuple, np.ndarray)):
# #             value = self.__type__(value[0], value[1])
# #         else:
# #             raise TypeError("Invalid type value of {} (expected {}), but received {}".format(self.__class__, self.__type__,  type(value)))

# #         obj.__store__[self.__name__] = [value.x, value.y]


# class PointArrayParameter(ParameterDescriptor):
#     import numpy as np
#     __type__ = np.array([])

#     def call_param_function(self, obj):
#         f = self.get_param_function(obj)
#         value = f([])
#         if value is None:
#             value = self.__operations__([])
#         else:
#             value = self.__operations__(value)
#         obj.__store__[self.__name__] = value
#         return value 
#         # if (value is None):
#         #     value = self.__process__([])
#         # else:
#         #     value = self.__process__([c.to_numpy_array() if isinstance(c, Coord) else c for c in value])
#         # return value 

#     def __operations__(self, points):
#         return points

#     # def __process__(self, points):
#     def __operations__(self, points):
#         from spira.yevon.geometry.shapes.shape import Shape
#         if isinstance(points, Shape):
#             return array(points.points)
#         elif isinstance(points, (list, np.ndarray)):
#             if len(points):
#                 element = points[0]
#                 if isinstance(element, (np.ndarray, list)):
#                     points_as_array = np.array(points, copy=False)
#                 else:
#                     points_as_array = np.array([(c[0], c[1]) for c in points])
#                 return points_as_array
#             else:
#                 return np.ndarray((0, 2))
#         # elif isinstance(points, Coord2):
#         #     return array([[points.x, points.y]])
#         # elif isinstance(points, tuple):
#         #     return array([[points[0], points[1]]])
#         else:
#             raise TypeError("Invalid type of points in setting value of PointsDefinitionProperty: " + str(type(points))) 

#     def __set__(self, obj, points):
#         obj.__store__[self.__name__] = points
        
#     # def __deepcopy__(self, memo):
#     #     from copy import deepcopy
#     #     return deepcopy(obj)
    

# # class PortListParameter(ParameterDescriptor):
# #     from spira.yevon.geometry.ports.port_list import PortList
# #     __type__ = PortList

# #     def __init__(self, default=[], **kwargs):
# #         kwargs['default'] = self.__type__(default)
# #         kwargs['restrictions'] = RestrictType([self.__type__])
# #         super().__init__(**kwargs)

# #     def __repr__(self):
# #         return ''

# #     def __str__(self):
# #         return ''

# #     def call_param_function(self, obj):
# #         f = self.get_param_function(obj)
# #         value = f(self.__type__())
# #         if value is None:
# #             value = self.__type__()
# #         obj.__store__[self.__name__] = value
# #         return value
