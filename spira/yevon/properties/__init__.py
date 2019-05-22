from spira.yevon.gdsii.cell import Cell
from spira.yevon.gdsii.sref import SRef
from spira.yevon.gdsii.polygon import Polygon
from spira.yevon.properties.cell import CellProperties
from spira.yevon.properties.polygon import PolygonProperties
from spira.yevon.properties.port import PortProperty, SRefPortProperty, PolygonPortProperty, CellPortProperty
from spira.yevon.properties.net import NetProperties
from spira.core.transformable import Transformable
from spira.core.outputs.base import Outputs


def load_properties():
    Cell.mixin(CellProperties)
    Cell.mixin(CellPortProperty)
    Cell.mixin(NetProperties)
    Cell.mixin(Transformable)
    Cell.mixin(Outputs)

    SRef.mixin(SRefPortProperty)

    Polygon.mixin(PolygonProperties)
    Polygon.mixin(PolygonPortProperty)


load_properties()
