import gdspy
import numpy as np

from copy import deepcopy
from spira.core.transforms import *
from spira.yevon import constants
from spira.yevon.gdsii.elem_list import ElementList
from spira.yevon.gdsii.group import Group
from spira.yevon.gdsii.polygon import __ShapeElement__, Polygon
from spira.yevon.geometry import shapes
from spira.yevon.geometry.shapes import ShapeParameter
from spira.yevon.geometry.line import line_from_two_points, LineParameter
from spira.yevon.geometry.coord import Coord
import spira.yevon.utils.geometry as ug
from spira.yevon.gdsii.base import __LayerElement__
from spira.yevon.process.physical_layer import PLayer
from spira.core.parameters.descriptor import Parameter
from spira.yevon.process.process_layer import ProcessParameter
from spira.core.parameters.variables import *
from spira.core.parameters.restrictions import RestrictValueList
from spira.core.transforms import Stretch
from spira.yevon.process.physical_layer import PLayer
from spira.core.parameters.descriptor import FunctionParameter, RestrictedParameter
from spira.core.parameters.initializer import ParameterInitializer
from spira.core.transformable import Transformable
from spira.yevon.process import get_rule_deck


__all__ = ['Edge', 'generate_edges']


RDD = get_rule_deck()


# class Edge(__ShapeElement__):
#     """ Edge elements are object that represents the edge of a polygonal shape. """

#     line = LineParameter()
#     internal_pid = StringParameter(default='no_pid', doc='A unique polygon ID to which the edge connects.')
#     external_pid = StringParameter(default='no_pid', doc='A unique polygon ID to which the edge connects.')

#     inside_edge = spira.Parameter(fdef_name='create_inside_edge')
#     outside_edge = spira.Parameter(fdef_name='create_outside_edge')
#     square_edge = spira.Parameter(fdef_name='create_square_edge')
#     side_extend_edge = spira.Parameter(fdef_name='create_side_extend_edge')
#     euclidean_edge = spira.Parameter(fdef_name='create_euclidean_edge')
    
#     def __init__(self, shape, line, transformation=None, **kwargs):
#         super().__init__(shape=shape, line=line, transformation=transformation, **kwargs)
    
#     def __repr__(self):
#         if self is None:
#             return 'Edge is None!'
#         layer = RDD.GDSII.IMPORT_LAYER_MAP[self.layer]
#         class_string = "[SPiRA: Edge] (center {}, width {}, extend {}, process {}, purpose {})"
#         return class_string.format(self.center, self.width, self.extend,
#             self.layer.process.symbol, self.layer.purpose.symbol)

#     def __str__(self):
#         return self.__repr__()

#     def short_string(self):
#         return "Edge [{}, {}, {}]".format(self.center, self.layer.process.symbol, self.layer.purpose.symbol)

#     def create_inside_edge(self):
#         shape = self.shape.move((0, extend/2.0))
#         return spira.Polygon(shape=shape, layer=self.layer)

#     def create_outside_edge(self):
#         shape = self.shape.move((0, -extend/2.0))
#         return spira.Polygon(shape=shape, layer=self.layer)

#     def create_square_edge(self):
#         sf = 1 + 2*extend/width
#         shape = Stretch(stretch_factor=(sf,1), stretch_center=self.shape.center_of_mass)(self.shape)
#         return spira.Polygon(shape=shape, layer=self.layer)

#     def create_side_extend_edge(self):
#         if 'side_extend' not in kwargs:
#             raise ValueError('No `side_extend` parameter given.')
#         side_extend = kwargs['side_extend']
#         sf = 1 + 2*side_extend/width
#         shape = Stretch(stretch_factor=(sf,1), stretch_center=self.shape.center_of_mass)(self.shape)
#         return spira.Polygon(shape=shape, layer=self.layer)

#     def create_euclidean_edge(self):
#         pass


class Path(__ShapeElement__):
    """  """

    width = NumberParameter(default=1, doc='The distance the edge extends from the shape.')
    path_type = RestrictedParameter(
        default=constants.PATH_TYPE_NORMAL,
        restriction=RestrictValueList(constants.PATH_TYPES))
    
    def __init__(self, shape, layer, transformation=None, **kwargs):
        super().__init__(shape=shape, layer=layer, transformation=transformation, **kwargs)

    def __repr__(self):
        if self is None:
            return 'Path is None!'
        layer = RDD.GDSII.IMPORT_LAYER_MAP[self.layer]
        class_string = "[SPiRA: Path \'{}\'] (center {}, width {}, extend {}, process {}, purpose {})"
        return class_string.format(self.alias, self.center, self.shape.width,
            self.extend, self.layer.process.symbol, self.layer.purpose.symbol)

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return hash(self.__repr__())

    def short_string(self):
        return "Path [{}, {}, {}]".format(self.center, self.layer.process.symbol, self.layer.purpose.symbol)

    def flat_copy(self, level=-1):
        """ Flatten a copy of the polygon. """
        S = Path(shape=self.shape, layer=self.layer, transformation=self.transformation)
        S.expand_transform()
        return S


class Edge(Path):
    """ Edge elements are object that represents the edge of a polygonal shape. """

    # def get_alias(self):
    #     if not hasattr(self, '__alias__'):
    #         self.__alias__ = self.layer.purpose.symbol
    #     return self.__alias__

    # def set_alias(self, value):
    #     if value is not None:
    #         self.__alias__ = value

    # alias = FunctionParameter(get_alias, set_alias, doc='Functions to generate an alias for cell name.')

    line_shape = ShapeParameter(default=[])

    edge_type = RestrictedParameter(
        default=constants.EDGE_TYPE_NORMAL, 
        restriction=RestrictValueList(constants.EDGE_TYPES))

    internal_pid = StringParameter(default='no_pid', doc='A unique polygon ID to which the edge connects.')
    external_pid = StringParameter(default='no_pid', doc='A unique polygon ID to which the edge connects.')

    def __init__(self, shape, layer, transformation=None, **kwargs):
        super().__init__(shape=shape, layer=layer, transformation=transformation, **kwargs)

    def __repr__(self):
        if self is None:
            return 'Edge is None!'
        layer = RDD.GDSII.IMPORT_LAYER_MAP[self.layer]
        class_string = "[SPiRA: Edge] (center {}, width {}, process {}, purpose {})"
        return class_string.format(self.center, self.width, self.layer.process.symbol, self.layer.purpose.symbol)

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return hash(self.__repr__())

    def short_string(self):
        return "Edge [{}, {}, {}]".format(self.center, self.layer.process.symbol, self.layer.purpose.symbol)

    def flat_copy(self, level=-1):
        """ Flatten a copy of the polygon. """
        S = Edge(shape=self.shape, layer=self.layer, transformation=self.transformation)
        S.expand_transform()
        return S


class EdgeGenerator(Group, __LayerElement__):
    """ Generates edge objects for each shape segment. """

    shape = ShapeParameter()
    internal_pid = StringParameter(default='no_pid', doc='A unique polygon ID to which the edge connects.')

    def create_elements(self, elems):

        for i, s in enumerate(self.shape.segments()):

            shape = shapes.Shape(points=s)

            L = RDD.GDSII.IMPORT_LAYER_MAP[self.layer]
            width = RDD[L.process.symbol].MIN_SIZE

            layer = PLayer(process=L.process, purpose=RDD.PURPOSE.PORT.OUTSIDE_EDGE_DISABLED)

            elems += Edge(
                shape=[],
                line_shape=shape,
                layer=layer,
                internal_pid=self.internal_pid,
                width=width,
                transformation=self.transformation
            )
            
        return elems


# class EdgeGenerator(Group, __LayerElement__):
#     """ Generates edge objects for each shape segment. """

#     shape = ShapeParameter()
#     internal_pid = StringParameter(default='no_pid', doc='A unique polygon ID to which the edge connects.')

#     def create_elements(self, elems):

#         for i, s in enumerate(self.shape.segments()):

#             width = ug.distance(s[0], s[1])
#             midpoint = ug.midpoint(s[0], s[1])
#             orientation = ug.orientation(s[0], s[1])

#             L = RDD.GDSII.IMPORT_LAYER_MAP[self.layer]
#             extend = RDD[L.process.symbol].MIN_SIZE

#             T = Rotation(orientation) + Translation(midpoint) + self.transformation
#             layer = PLayer(process=L.process, purpose=RDD.PURPOSE.PORT.OUTSIDE_EDGE_DISABLED)

#             elems += Edge(
#                 alias='{}_e{}'.format(self.layer.name, i),
#                 shape=shapes.BoxShape(width=width, height=extend),
#                 layer=layer,
#                 internal_pid=self.internal_pid,
#                 extend=extend,
#                 transformation=T
#             )
            
#         return elems


# class EdgeGenerator(Group, __LayerElement__):
#     """ Generates edge objects for each shape segment. """

#     shape = ShapeParameter()
#     internal_pid = StringParameter(default='no_pid', doc='A unique polygon ID to which the edge connects.')

#     def create_elements(self, elems):

#         xpts = list(self.shape.x_coords)
#         ypts = list(self.shape.y_coords)

#         n = len(xpts)
#         xpts.append(xpts[0])
#         ypts.append(ypts[0])

#         clockwise = 0
#         for i in range(0, n):
#             clockwise += ((xpts[i+1] - xpts[i]) * (ypts[i+1] + ypts[i]))

#         if self.layer.name == 'BBOX': bbox = True
#         else: bbox = False

#         for i in range(0, n):

#             x = np.sign(clockwise) * (xpts[i+1] - xpts[i])
#             y = np.sign(clockwise) * (ypts[i] - ypts[i+1])
#             orientation = (np.arctan2(x, y) * constants.RAD2DEG) + 90
#             midpoint = [(xpts[i+1] + xpts[i])/2, (ypts[i+1] + ypts[i])/2]
#             width = np.abs(np.sqrt((xpts[i+1] - xpts[i])**2 + (ypts[i+1]-ypts[i])**2))

#             L = RDD.GDSII.IMPORT_LAYER_MAP[self.layer]
#             extend = RDD[L.process.symbol].MIN_SIZE

#             elems += Edge(
#                 alias='{}_e{}'.format(self.layer.name, i),
#                 shape=shapes.BoxShape(width=width, height=extend),
#                 layer=PLayer(process=L.process, purpose=RDD.PURPOSE.PORT.OUTSIDE_EDGE_DISABLED),
#                 internal_pid=self.internal_pid,
#                 width=width,
#                 extend=extend,
#                 transformation=Rotation(orientation) + Translation(midpoint) + self.transformation
#             )
            
#             # T = Rotation(orientation) + Translation(midpoint) + self.transformation
#             # layer = PLayer(process=L.process, purpose=RDD.PURPOSE.PORT.OUTSIDE_EDGE_DISABLED),

#             # p1 = Coord(xpts[i], ypts[i])
#             # p2 = Coord(xpts[i+1], ypts[i+1])

#             # edge = Edge(
#             #     # alias='{}_e{}'.format(self.layer.name, i),
#             #     shape=shapes.BoxShape(width=width, height=extend),
#             #     line=line_from_two_points(p1, p2),
#             #     layer=layer,
#             #     internal_pid=self.internal_pid,
#             #     transformation=T
#             # )

#             # elems += edge

#         return elems


def generate_edges(shape, layer, internal_pid, transformation):
    """ Method call for edge generator. """
    edge_gen = EdgeGenerator(shape=shape, layer=layer, internal_pid=internal_pid, transformation=transformation)
    return edge_gen.elements


