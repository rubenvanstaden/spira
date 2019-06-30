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


def generate_polygon_edges(shape, layer):
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


class __Edge__(Group):

    width = NumberParameter(default=1)
    inward_extend = NumberParameter(default=1)
    inside = Parameter(fdef_name='create_inside')
    process = ProcessParameter()

    def create_inside(self):
        for e in self.elements:
            if e.layer.purpose == RDD.PURPOSE.PORT.INSIDE_EDGE_DISABLED:
                return e
        return None


class Edge(__Edge__):
    """
    
    Example
    -------
    >>> edge Edge()
    """

    pid = StringParameter(default='no_pid')
    outward_extend = NumberParameter(default=1)
    outside = Parameter(fdef_name='create_outside')

    def create_outside(self):
        for e in self.elements:
            purposes = [RDD.PURPOSE.PORT.OUTSIDE_EDGE_ENABLED, RDD.PURPOSE.PORT.OUTSIDE_EDGE_DISABLED]
            if e.layer.purpose in purposes:
                return e
        return None

    def create_elements(self, elems):

        c1 = Coord(0, self.inward_extend/2)
        layer = PLayer(process=self.process, purpose=RDD.PURPOSE.PORT.INSIDE_EDGE_DISABLED)
        p1 = Box(alias='InsideEdge', 
            width=self.width, 
            height=self.inward_extend, 
            center=c1, layer=layer)

        c1 = Coord(0, -self.outward_extend/2)
        layer = PLayer(process=self.process, purpose=RDD.PURPOSE.PORT.OUTSIDE_EDGE_DISABLED)
        p2 = Box(alias='OutsideEdge', 
            width=self.width, 
            height=self.outward_extend, 
            center=c1, layer=layer)

        elems += [p1, p2]

        # elems += self.inside
        # elems += self.outside
        return elems


class EdgeEuclidean(Edge):

    radius = NumberParameter(default=1)

    def __init__(self, **kwargs):
        pass

    def create_elements(self, elems):

        return elems


class EdgeSquare(Edge):

    def __init__(self, **kwargs):
        pass

    def create_elements(self, elems):

        return elems


class EdgeSideExtend(Edge):

    side_extend = NumberParameter(default=1)

    def __init__(self, **kwargs):
        pass

    def create_elements(self, elems):

        return elems






