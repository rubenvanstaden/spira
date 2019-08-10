from spira.yevon import constants
from spira.log import SPIRA_LOG as LOG
from spira.yevon.filters.filter import Filter
from spira.yevon.gdsii.elem_list import ElementList
from spira.yevon.gdsii.polygon import Polygon, Box
from spira.yevon.gdsii.group import Group
from spira.yevon.gdsii.cell import Cell
from spira.yevon.gdsii.label import Label
from spira.core.transforms import Rotation
from spira.yevon.geometry.shapes.adapters import ShapeEdge
from spira.core.parameters.variables import *
from spira.yevon.process.physical_layer import PLayer
from spira.yevon.geometry import shapes
from copy import deepcopy
from spira.yevon.geometry.vector import transformation_from_vector
from spira.yevon.process.purpose_layer import PurposeLayerParameter
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = ['PortCellFilter', 'PortPolygonFilter', 'PortToPolygonFilter', 'RouteToPolygonFilter']


class __PolygonFilter__(Filter):
    """ Base class for edge filters. """

    arrow_width = NumberParameter()
    arrow_length = NumberParameter()

    surface_width = NumberParameter()
    surface_length = NumberParameter()

    def _create_edge(self, item):
        dw = item.width
        dl = item.length/10
        layer = PLayer(process=item.process, purpose=item.purpose)
        p = Box(width=dw, height=dl, layer=layer)
        T = transformation_from_vector(item) + Rotation(rotation=-90, rotation_center=item.midpoint)
        p.transform(T)
        return p

    def _create_arrow(self, item):
        layer = PLayer(item.process, RDD.PURPOSE.PORT.DIRECTION)
        w = 0.01
        l = 0.2
        arrow_shape = shapes.ArrowShape(width=w, length=l, head=l*0.2)
        p = Polygon(shape=arrow_shape, layer=layer)
        T = transformation_from_vector(item)
        p.transform(T)
        return p

    def _create_label(self, item):
        purpose = RDD.PURPOSE.TEXT[item.purpose.symbol+'T']
        layer = PLayer(item.process, purpose)
        return Label(
            position=item.midpoint,
            text=item.name,
            orientation=item.orientation,
            layer=layer
        )


class PortToPolygonFilter(__PolygonFilter__):

    def filter_Port(self, item):
        elems = ElementList()
        elems += self._create_edge(item)
        elems += self._create_arrow(item)
        elems += self._create_label(item)
        cell = Cell(elements=elems)
        return cell

    def filter_Polygon(self, item):
        elems = ElementList()
        for p in item.edge_ports:
            el = self.filter_Port(p).elements
            elems += el
            # elems += el.transform(item.transformation)
        for p in item.ports:
            el = self.filter_Port(p).elements
            elems += el.transform(item.transformation)
        cell = Cell(elements=elems)
        return cell

    def __repr__(self):
        return "[SPiRA: PortCellFilter] ())".format()


class PortCellFilter(PortToPolygonFilter):

    def filter_Cell(self, item):
        for p in item.ports:
            if p.purpose.symbol != 'E':
                el = self.filter_Port(p).elements
                item += el.transform(item.transformation)
        return item

    def __repr__(self):
        return "[SPiRA: PortCellFilter] ())".format()


class PortPolygonFilter(PortToPolygonFilter):

    def filter_Cell(self, item):
        elems = ElementList()
        for c in item.dependencies():
            for p in c.elements.polygons:
                c += self.filter_Polygon(p).elements
        return item

    def __repr__(self):
        return "[SPiRA: PortCellFilter] ())".format()


class RouteToPolygonFilter(__PolygonFilter__):

    def filter_Route(self, item):
        edge_ply = Polygon(shape=item.shape, layer=item.layer, transformation=item.transformation)
        return edge_ply

    def __repr__(self):
        return "[SPiRA: RouteToPolygonFilter] ())".format()

