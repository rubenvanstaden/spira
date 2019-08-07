from spira.yevon import constants
from spira.log import SPIRA_LOG as LOG
from spira.yevon.filters.filter import Filter
from spira.yevon.gdsii.elem_list import ElementList
from spira.yevon.gdsii.polygon import Polygon
from spira.yevon.geometry.shapes.adapters import ShapeEdge
from spira.core.parameters.variables import *
from spira.yevon.process.purpose_layer import PurposeLayerParameter


__all__ = ['EdgeShapeFilter', 'EdgeToPolygonFilter']


class __EdgeFilter__(Filter):
    """ Base class for edge filters. """

    purposes = PurposeLayerParameter()
    width = NumberParameter(allow_none=True, default=None)
    edge_type = IntegerParameter(default=constants.EDGE_TYPE_NORMAL)


class EdgeShapeFilter(__EdgeFilter__):
    """ Filter only passes edges with the specified purpose. """

    def filter_Cell(self, item):
        from copy import deepcopy
        from spira.yevon.gdsii.cell import Cell

        elems = ElementList()
        if self.width is None:
            for p1 in deepcopy(item.elements.polygons):
                if p1.layer.purpose in self.purposes:
                    for edge in p1.edges:
                        shape = ShapeEdge(
                            original_shape=edge.line_shape,
                            edge_width=edge.width,
                            edge_type=self.edge_type
                        )
                        elems += edge.copy(shape=shape)
                    elems += p1
        else:
            for p1 in deepcopy(item.elements.polygons):
                if p1.layer.purpose in self.purposes:
                    for edge in p1.edges:
                        shape = ShapeEdge(
                            original_shape=edge.line_shape,
                            edge_width=self.width,
                            edge_type=self.edge_type
                        )
                        elems += edge.copy(shape=shape)
                    elems += p1


        cell = Cell(elements=elems)
        return cell

    def filter_Group(self, item):
        pass

    def __repr__(self):
        return "[SPiRA: EdgeShapeFilter] ())".format()


class EdgeToPolygonFilter(__EdgeFilter__):

    def filter_Edge(self, item):
        edge_ply = Polygon(shape=item.shape, layer=item.layer, transformation=item.transformation)
        return edge_ply

    def __repr__(self):
        return "[SPiRA: EdgeShapeFilter] ())".format()

