from spira.yevon.gdsii.cell import Cell
from spira.yevon.properties.cell import CellProperties
from spira.yevon.properties.port import PortProperties
from spira.yevon.properties.net import NetProperties
from spira.core.transformable import Transformable
from spira.core.outputs.base import Outputs


def load_properties():
    Cell.mixin(CellProperties)
    Cell.mixin(PortProperties)
    Cell.mixin(NetProperties)
    Cell.mixin(Transformable)
    Cell.mixin(Outputs)


load_properties()
