from spira.yevon.gdsii.cell import Cell
from spira.yevon.gdsii.sref import SRef
from spira.yevon.gdsii.polygon import Polygon
from spira.yevon.properties.cell import CellAspects
from spira.yevon.properties.polygon import PolygonAspects, PolygonClipperAspects
from spira.yevon.properties.port import PortProperty, SRefPortProperty, PolygonPortProperty, CellPortProperty
from spira.yevon.properties.net import NetAspects
from spira.core.transformable import Transformable
from spira.core.outputs.base import Outputs


def load_properties():
    Cell.mixin(CellAspects)
    Cell.mixin(CellPortProperty)
    Cell.mixin(NetAspects)
    Cell.mixin(Transformable)
    Cell.mixin(Outputs)

    SRef.mixin(SRefPortProperty)

    Polygon.mixin(PolygonAspects)
    Polygon.mixin(PolygonPortProperty)
    Polygon.mixin(PolygonClipperAspects)


load_properties()
