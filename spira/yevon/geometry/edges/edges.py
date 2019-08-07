import gdspy
import numpy as np

from spira.core.transforms import *
from spira.core.parameters.variables import *

from spira.yevon import constants
from spira.core.parameters.restrictions import RestrictValueList
from spira.core.parameters.descriptor import RestrictedParameter
from spira.yevon.process import get_rule_deck


__all__ = ['Edge', 'generate_edges']


RDD = get_rule_deck()


from spira.yevon.gdsii.base import __ShapeElement__
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


from spira.yevon.geometry.shapes import ShapeParameter, Shape
class Edge(Path):
    """ Edge elements are object that represents the edge of a polygonal shape. """

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
        # return "Edge [{}, {}, {}]".format(self.center, self.layer.process.symbol, self.layer.purpose.symbol)
        # NOTE: We want to ignore the purpose for CIRCUIT_METAL ot DEVICE_METAL net connections.
        return "Edge [{}, {}]".format(self.center, self.layer.process.symbol)

    def flat_copy(self, level=-1):
        """ Flatten a copy of the polygon. """
        S = Edge(shape=self.shape, layer=self.layer, transformation=self.transformation)
        S.expand_transform()
        return S


from spira.yevon.gdsii.group import Group
from spira.yevon.gdsii.base import __LayerElement__
from spira.yevon.process.physical_layer import PLayer
class EdgeGenerator(Group, __LayerElement__):
    """ Generates edge objects for each shape segment. """

    shape = ShapeParameter()
    internal_pid = StringParameter(default='no_pid', doc='A unique polygon ID to which the edge connects.')

    def create_elements(self, elems):

        shape = self.shape.remove_straight_angles()
        shape = shape.reverse_points()

        for i, s in enumerate(shape.segments()):

            line_shape = Shape(points=s)

            L = RDD.GDSII.IMPORT_LAYER_MAP[self.layer]
            width = RDD[L.process.symbol].MIN_SIZE

            layer = PLayer(process=L.process, purpose=RDD.PURPOSE.PORT.OUTSIDE_EDGE_DISABLED)

            elems += Edge(
                shape=[],
                line_shape=line_shape,
                layer=layer,
                internal_pid=self.internal_pid,
                width=width,
                transformation=self.transformation
            )
            
        return elems


def generate_edges(shape, layer, internal_pid, transformation):
    """ Method call for edge generator. """
    edge_gen = EdgeGenerator(shape=shape, layer=layer, internal_pid=internal_pid, transformation=transformation)
    return edge_gen.elements


from spira.yevon.aspects.base import __Aspects__
from spira.core.parameters.descriptor import Parameter
class EdgeAspects(__Aspects__):

    edges = Parameter(fdef_name='create_edges')

    def create_edges(self):
        """ Generate default edges for this polygon.
        These edges can be transformed using adapters. """
        from spira.yevon.geometry.edges.edges import generate_edges
        return generate_edges(
            shape=self.shape, layer=self.layer,
            internal_pid=self.id_string(),
            transformation=self.transformation)


from spira.yevon.gdsii.polygon import Polygon
Polygon.mixin(EdgeAspects)

