import numpy as np

from copy import deepcopy
from spira.yevon.gdsii.group import Group
from spira.core.transforms import *
from spira.yevon.gdsii.elem_list import ElementList
from spira.yevon.gdsii.polygon import Box, Polygon
from spira.yevon.geometry.coord import Coord
from spira.yevon.gdsii.base import __LayerElement__
from spira.core.parameters.descriptor import Parameter
from spira.yevon.process.process_layer import ProcessParameter
from spira.core.parameters.variables import *
from spira.yevon.process.physical_layer import PLayer
from spira.yevon.process import get_rule_deck


__all__ = ['Edge', 'EdgeEuclidean', 'EdgeSquare', 'EdgeSideExtend']


RDD = get_rule_deck()


class __EdgeElement__(Group):
    """ Base class for an edge element. """

    process = ProcessParameter(doc='Process to which the edge connects.')
    width = NumberParameter(default=1, doc='The width of the edge.')
    pid = StringParameter(default='no_pid', doc='A unique polygon ID to which the edge connects.')


class Edge(__EdgeElement__):
    """ Edge elements are object that represents the edge
    of a polygonal shape.
    
    Example
    -------
    >>> edge Edge()
    """

    inward_extend = NumberParameter(default=1, doc='The distance the edge extends inwards to the shape.')
    inside = Parameter(fdef_name='create_inside')

    outward_extend = NumberParameter(default=1, doc='The distance the edge extends outwards to the shape.')
    outside = Parameter(fdef_name='create_outside')

    def create_inside(self):
        for e in self.elements:
            purposes = [RDD.PURPOSE.PORT.INSIDE_EDGE_ENABLED, RDD.PURPOSE.PORT.INSIDE_EDGE_DISABLED]
            if e.layer.purpose in purposes:
                return e
        return None

    def create_outside(self):
        for e in self.elements:
            purposes = [RDD.PURPOSE.PORT.OUTSIDE_EDGE_ENABLED, RDD.PURPOSE.PORT.OUTSIDE_EDGE_DISABLED]
            if e.layer.purpose in purposes:
                return e
        return None

    def create_elements(self, elems):

        layer = PLayer(process=self.process, purpose=RDD.PURPOSE.PORT.INSIDE_EDGE_DISABLED)
        elems += Box(alias='InsideEdge',
            width=self.width,
            height=self.inward_extend,
            center=Coord(0, self.inward_extend/2),
            layer=layer)

        layer = PLayer(process=self.process, purpose=RDD.PURPOSE.PORT.OUTSIDE_EDGE_DISABLED)
        elems += Box(alias='OutsideEdge',
            width=self.width,
            height=self.outward_extend,
            center=Coord(0, -self.outward_extend/2),
            layer=layer)

        return elems


def EdgeEuclidean(radius=1.0):
    """  """
    pass


def EdgeSquare():
    """  """
    pass


def EdgeSideExtend(side_extend=0.0):
    """  """
    pass


def generate_edges(shape, layer):
    """ Generates edge objects for each shape segment. """

    xpts = list(shape.x_coords)
    ypts = list(shape.y_coords)

    n = len(xpts)
    xpts.append(xpts[0])
    ypts.append(ypts[0])

    clockwise = 0
    for i in range(0, n):
        clockwise += ((xpts[i+1] - xpts[i]) * (ypts[i+1] + ypts[i]))

    if layer.name == 'BBOX': bbox = True
    else: bbox = False

    edges = ElementList()
    for i in range(0, n):

        name = '{}_e{}'.format(layer.name, i)
        x = np.sign(clockwise) * (xpts[i+1] - xpts[i])
        y = np.sign(clockwise) * (ypts[i] - ypts[i+1])
        orientation = (np.arctan2(x, y) * constants.RAD2DEG)
        midpoint = [(xpts[i+1] + xpts[i])/2, (ypts[i+1] + ypts[i])/2]
        width = np.abs(np.sqrt((xpts[i+1] - xpts[i])**2 + (ypts[i+1]-ypts[i])**2))

        layer = RDD.GDSII.IMPORT_LAYER_MAP[layer]
        inward_extend = RDD[layer.process.symbol].MIN_SIZE / 2
        outward_extend = RDD[layer.process.symbol].MIN_SIZE / 2

        edge = Edge(width=width,
            inward_extend=inward_extend,
            outward_extend=outward_extend,
            process=layer.process)

        T = Rotation(orientation+90) + Translation(midpoint)
        edge.transform(T)
        edges += edge

    return edges




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

