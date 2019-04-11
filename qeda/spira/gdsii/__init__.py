from spira.gdsii.polygon import Polygon
from spira.gdsii.sref import SRef
from spira.gdsii.label import Label
from spira.gdsii.cell_list import CellList
from spira.gdsii.cell import Cell, Connector
from core.outputs.base import Outputs
from core.transformable import Transformable
from spira.properties.cell import CellProperties
from spira.properties.port import PortProperties


def load_properties():
    Cell.mixin(CellProperties)
    Cell.mixin(PortProperties)
    Cell.mixin(Transformable)
    Cell.mixin(Outputs)


load_properties()


