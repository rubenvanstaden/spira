import numpy as np

from copy import deepcopy
from spira.core.transforms import *
from spira.yevon.gdsii.elem_list import ElementList
from spira.yevon.gdsii.group import Group
from spira.yevon.gdsii.polygon import Polygon
from spira.yevon.geometry import shapes
from spira.yevon.geometry.shapes import ShapeParameter
from spira.yevon.geometry.coord import Coord
from spira.yevon.gdsii.base import __LayerElement__
from spira.core.parameters.descriptor import Parameter
from spira.yevon.process.process_layer import ProcessParameter
from spira.core.parameters.variables import *
from spira.yevon.process.physical_layer import PLayer
from spira.yevon.process import get_rule_deck


__all__ = [
    'Edge',
    'EdgeInside',
    'EdgeOutside',
    'EdgeEuclidean',
    'EdgeSquare',
    'EdgeSideExtend',
    'EdgeGenerator',
    'generate_edges',
]


RDD = get_rule_deck()


class __EdgeElement__(Polygon):
    """ Base class for an edge element. """

    width = NumberParameter(default=1, doc='The width of the edge.')
    pid = StringParameter(default='no_pid', doc='A unique polygon ID to which the edge connects.')


class Edge(__EdgeElement__):
    """ Edge elements are object that represents the edge
    of a polygonal shape.

    Example
    -------
    >>> edge Edge()
    """

    extend = NumberParameter(default=1, doc='The distance the edge extends from the shape.')

    def __init__(self, shape, layer, transformation=None, **kwargs):
        super().__init__(shape=shape, layer=layer, transformation=transformation, **kwargs)

    def __repr__(self):
        if self is None:
            return 'Edge is None!'
        layer = RDD.GDSII.IMPORT_LAYER_MAP[self.layer]
        class_string = "[SPiRA: Edge \'{}\'] (center {}, vertices {}, process {}, purpose {})"
        return class_string.format(self.alias, self.center, self.count, self.process, self.purpose)

    def __str__(self):
        return self.__repr__()


def EdgeSymmetric(width=1, extend=1, process=None, transformation=None):
    """  """
    layer = PLayer(process=process, purpose=RDD.PURPOSE.PORT.INSIDE_EDGE_DISABLED)
    shape = shapes.BoxShape(width=width, height=2*extend, center=Coord(0, extend/4))
    return Edge(shape=shape, layer=layer, transformation=transformation)


def EdgeInside(width=1, extend=1, process=None, purpose=None):
    """  """
    layer = PLayer(process=process, purpose=RDD.PURPOSE.PORT.INSIDE_EDGE_DISABLED)
    # shape = Box(width=self.width, height=self.extend, center=Coord(0, self.extend/2), layer=self.layer)
    # return Edge(shape=shape)


def EdgeOutside(width=1, extend=1, process=None, purpose=None):
    """  """
    layer = PLayer(process=process, purpose=RDD.PURPOSE.PORT.OUTSIDE_EDGE_DISABLED)
    # return Edge(width=width, height=extend, center=Coord(0, -extend/2), layer=layer)


def EdgeEuclidean(radius=1.0):
    """  """
    pass


def EdgeSquare():
    """  """
    pass


def EdgeSideExtend(side_extend=0.0):
    """  """
    pass


class EdgeGenerator(Group, __LayerElement__):
    """ Generates edge objects for each shape segment. """

    shape = ShapeParameter()

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
    
            name = '{}_e{}'.format(self.layer.name, i)
            x = np.sign(clockwise) * (xpts[i+1] - xpts[i])
            y = np.sign(clockwise) * (ypts[i] - ypts[i+1])
            orientation = (np.arctan2(x, y) * constants.RAD2DEG) + 90
            midpoint = [(xpts[i+1] + xpts[i])/2, (ypts[i+1] + ypts[i])/2]
            width = np.abs(np.sqrt((xpts[i+1] - xpts[i])**2 + (ypts[i+1]-ypts[i])**2))
    
            layer = RDD.GDSII.IMPORT_LAYER_MAP[self.layer]
            extend = RDD[layer.process.symbol].MIN_SIZE / 2
    
            T = Rotation(orientation) + Translation(midpoint)
            elems += EdgeSymmetric(width=width, extend=extend, process=layer.process, transformation=T)
    
        return elems


def generate_edges(shape, layer):
    """ Method call for edge generator. """
    edge_gen = EdgeGenerator(shape=shape, layer=layer)
    return edge_gen.elements


# def generate_edges(shape, layer):
#     """ Generates edge objects for each shape segment. """

#     xpts = list(shape.x_coords)
#     ypts = list(shape.y_coords)

#     n = len(xpts)
#     xpts.append(xpts[0])
#     ypts.append(ypts[0])

#     clockwise = 0
#     for i in range(0, n):
#         clockwise += ((xpts[i+1] - xpts[i]) * (ypts[i+1] + ypts[i]))

#     if layer.name == 'BBOX': bbox = True
#     else: bbox = False

#     edges = ElementList()
#     for i in range(0, n):

#         name = '{}_e{}'.format(layer.name, i)
#         x = np.sign(clockwise) * (xpts[i+1] - xpts[i])
#         y = np.sign(clockwise) * (ypts[i] - ypts[i+1])
#         orientation = (np.arctan2(x, y) * constants.RAD2DEG)
#         midpoint = [(xpts[i+1] + xpts[i])/2, (ypts[i+1] + ypts[i])/2]
#         width = np.abs(np.sqrt((xpts[i+1] - xpts[i])**2 + (ypts[i+1]-ypts[i])**2))

#         layer = RDD.GDSII.IMPORT_LAYER_MAP[layer]
#         inward_extend = RDD[layer.process.symbol].MIN_SIZE / 2
#         outward_extend = RDD[layer.process.symbol].MIN_SIZE / 2

#         edge = Edge(width=width,
#             inward_extend=inward_extend,
#             outward_extend=outward_extend,
#             process=layer.process)

#         T = Rotation(orientation+90) + Translation(midpoint)
#         edge.transform(T)
#         edges += edge

#     return edges




# from spira.yevon.geometry.ports.port import Port
# from spira.yevon.process.gdsii_layer import Layer
# def shape_edge_ports(shape, layer, local_pid='None', center=(0,0), loc_name=''):

#     edges = PortList()

#     xpts = list(shape.x_coords)
#     ypts = list(shape.y_coords)

#     n = len(xpts)

#     xpts.append(xpts[0])
#     ypts.append(ypts[0])

#     clockwise = 0
#     for i in range(0, n):
#         clockwise += ((xpts[i+1] - xpts[i]) * (ypts[i+1] + ypts[i]))

#     if layer.name == 'BBOX': bbox = True
#     else: bbox = False

#     layer = RDD.GDSII.IMPORT_LAYER_MAP[layer]

#     for i in range(0, n):
#         # name = 'E{}_{}'.format(i, layer.process.symbol)
#         # name = 'E{}_{}_{}'.format(i, layer.process.symbol, shape.bbox_info.center)
#         name = '{}E{}_{}'.format(loc_name, i, layer.process.symbol)
#         x = np.sign(clockwise) * (xpts[i+1] - xpts[i])
#         y = np.sign(clockwise) * (ypts[i] - ypts[i+1])
#         orientation = (np.arctan2(x, y) * constants.RAD2DEG)
#         midpoint = [(xpts[i+1] + xpts[i])/2, (ypts[i+1] + ypts[i])/2]
#         width = np.abs(np.sqrt((xpts[i+1] - xpts[i])**2 + (ypts[i+1]-ypts[i])**2))
#         P = Port(
#             name=name,
#             process=layer.process,
#             purpose=RDD.PURPOSE.PORT.OUTSIDE_EDGE_DISABLED,
#             midpoint=midpoint,
#             orientation=orientation,
#             width=width,
#             length=0.2,
#             local_pid=local_pid
#         )
#         edges += P
#     return edges

