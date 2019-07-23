import gdspy
import numpy as np

from copy import deepcopy
from spira.core.transforms import *
from spira.yevon import constants
from spira.yevon.gdsii.elem_list import ElementList
from spira.yevon.gdsii.group import Group
from spira.yevon.gdsii.polygon import __ShapeElement__
from spira.yevon.geometry import shapes
from spira.yevon.geometry.shapes import ShapeParameter
from spira.yevon.geometry.coord import Coord
from spira.yevon.gdsii.base import __LayerElement__
from spira.core.parameters.descriptor import Parameter
from spira.yevon.process.process_layer import ProcessParameter
from spira.core.parameters.variables import *
from spira.core.transforms import Stretch
from spira.yevon.process.physical_layer import PLayer
from spira.core.parameters.descriptor import FunctionParameter
from spira.yevon.process import get_rule_deck


__all__ = [
    'Edge',
    'EdgeAdapter',
    'generate_edges',
]


RDD = get_rule_deck()


class Edge(__ShapeElement__):
    """ Edge elements are object that represents the edge of a polygonal shape.

    Example
    -------
    >>> edge Edge()
    """

    def get_alias(self):
        if not hasattr(self, '__alias__'):
            self.__alias__ = self.layer.purpose.symbol
        return self.__alias__

    def set_alias(self, value):
        if value is not None:
            self.__alias__ = value

    alias = FunctionParameter(get_alias, set_alias, doc='Functions to generate an alias for cell name.')

    width = NumberParameter(default=1, doc='The width of the edge.')
    extend = NumberParameter(default=1, doc='The distance the edge extends from the shape.')
    internal_pid = StringParameter(default='no_pid', doc='A unique polygon ID to which the edge connects.')
    external_pid = StringParameter(default='no_pid', doc='A unique polygon ID to which the edge connects.')
    edge_type = IntegerParameter(default=constants.EDGE_TYPE_NORMAL)

    def __init__(self, shape, layer, transformation=None, **kwargs):
        super().__init__(shape=shape, layer=layer, transformation=transformation, **kwargs)

    def __repr__(self):
        if self is None:
            return 'Edge is None!'
        layer = RDD.GDSII.IMPORT_LAYER_MAP[self.layer]
        class_string = "[SPiRA: Edge \'{}\'] (center {}, width {}, extend {}, process {}, purpose {})"
        return class_string.format(self.alias, self.center, self.width,
            self.extend, self.layer.process.symbol, self.layer.purpose.symbol)

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


def EdgeAdapter(original_edge, edge_type, **kwargs):
    """ Adapter class to modify the edge shape. """

    shape = original_edge.shape
    extend = original_edge.extend
    width = original_edge.width

    if edge_type == constants.EDGE_TYPE_INSIDE:
        shp = shape.move((0, extend/2.0))
    elif edge_type == constants.EDGE_TYPE_OUTSIDE:
        shp = shape.move((0, -extend/2.0))
    elif edge_type == constants.EDGE_TYPE_SQUARE:
        sf = 1 + 2*extend/width
        shp = Stretch(stretch_factor=(sf,1), stretch_center=shape.center_of_mass)(shape)
    elif edge_type == constants.EDGE_TYPE_SIDE_EXTEND:
        if 'side_extend' not in kwargs:
            raise ValueError('No `side_extend` parameter given.')
        side_extend = kwargs['side_extend']
        sf = 1 + 2*side_extend/width
        shp = Stretch(stretch_factor=(sf,1), stretch_center=shape.center_of_mass)(shape)
    elif edge_type == constants.EDGE_TYPE_EUCLIDEAN:
        pass
    elif edge_type == constants.EDGE_TYPE_NORMAL:
        pass

    original_edge = original_edge.copy(shape=shp, edge_type=edge_type)

    return original_edge


class EdgeGenerator(Group, __LayerElement__):
    """ Generates edge objects for each shape segment. """

    shape = ShapeParameter()
    internal_pid = StringParameter(default='no_pid', doc='A unique polygon ID to which the edge connects.')

    def create_elements(self, elems):

        xpts = list(self.shape.x_coords)
        ypts = list(self.shape.y_coords)

        n = len(xpts)
        xpts.append(xpts[0])
        ypts.append(ypts[0])

        clockwise = 0
        for i in range(0, n):
            clockwise += ((xpts[i+1] - xpts[i]) * (ypts[i+1] + ypts[i]))

        if self.layer.name == 'BBOX': bbox = True
        else: bbox = False

        for i in range(0, n):

            x = np.sign(clockwise) * (xpts[i+1] - xpts[i])
            y = np.sign(clockwise) * (ypts[i] - ypts[i+1])
            orientation = (np.arctan2(x, y) * constants.RAD2DEG) + 90
            midpoint = [(xpts[i+1] + xpts[i])/2, (ypts[i+1] + ypts[i])/2]
            width = np.abs(np.sqrt((xpts[i+1] - xpts[i])**2 + (ypts[i+1]-ypts[i])**2))

            layer = RDD.GDSII.IMPORT_LAYER_MAP[self.layer]
            extend = RDD[layer.process.symbol].MIN_SIZE

            elems += Edge(
                alias='{}_e{}'.format(self.layer.name, i),
                shape=shapes.BoxShape(width=width, height=extend),
                layer=PLayer(process=layer.process, purpose=RDD.PURPOSE.PORT.OUTSIDE_EDGE_DISABLED),
                internal_pid=self.internal_pid,
                width=width,
                extend=extend,
                transformation=Rotation(orientation) + Translation(midpoint) + self.transformation
            )

        return elems


def generate_edges(shape, layer, internal_pid, transformation):
    """ Method call for edge generator. """
    edge_gen = EdgeGenerator(shape=shape, layer=layer, internal_pid=internal_pid, transformation=transformation)
    return edge_gen.elements


