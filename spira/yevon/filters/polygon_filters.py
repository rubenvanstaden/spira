from spira.yevon import constants
from spira.log import SPIRA_LOG as LOG
from spira.yevon.filters.filter import Filter
from spira.yevon.gdsii.elem_list import ElementList
from spira.yevon.gdsii.polygon import Polygon
from spira.yevon.gdsii.group import Group
from spira.yevon.geometry.shapes.adapters import ShapeEdge
from spira.core.parameters.variables import *
from spira.yevon.process.purpose_layer import PurposeLayerParameter


__all__ = ['PortToPolygonFilter', 'RouteToPolygonFilter']


class __PolygonFilter__(Filter):
    """ Base class for edge filters. """


class PortToPolygonFilter(__PolygonFilter__):

    arrow_width = NumberParameter()
    arrow_length = NumberParameter()
    
    surface_width = NumberParameter()
    surface_length = NumberParameter()

    def filter_Port(self, item):
        edge_ply = Polygon(shape=item.shape, layer=item.layer, transformation=item.transformation)
        return edge_ply

    def filter_Cell(self, item):
        elems = ElementList()
        for p in item.ports:
            elems += self.filter_Port(p)
        return Group(elements=elems)

    def __repr__(self):
        return "[SPiRA: PortToPolygonFilter] ())".format()


class RouteToPolygonFilter(__PolygonFilter__):

    def filter_Route(self, item):
        edge_ply = Polygon(shape=item.shape, layer=item.layer, transformation=item.transformation)
        return edge_ply

    def __repr__(self):
        return "[SPiRA: RouteToPolygonFilter] ())".format()

