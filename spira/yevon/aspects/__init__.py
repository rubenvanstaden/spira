from spira.yevon.gdsii.cell import Cell
from spira.yevon.gdsii.sref import SRef
from spira.yevon.gdsii.polygon import Polygon
from spira.yevon.aspects.cell import CellAspects
from spira.yevon.aspects.polygon import PolygonAspects, PolygonClipperAspects
from spira.yevon.aspects.port import PortProperty, SRefPortProperty, PolygonPortProperty, CellPortProperty
from spira.yevon.aspects.netlist import NetlistAspects
from spira.core.transformable import Transformable
# from spira.core.outputs.base import Outputs
from spira.yevon.aspects.output import OutputGdsiiAspect
from spira.yevon.aspects.shape import ShapeClipperAspects
from spira.yevon.geometry.shapes import Shape


def load_aspect():
    """ Mix the aspects into their corresponding classes. """

    Cell.mixin(CellAspects)
    Cell.mixin(CellPortProperty)
    Cell.mixin(NetlistAspects)
    Cell.mixin(Transformable)
    Cell.mixin(OutputGdsiiAspect)

    SRef.mixin(SRefPortProperty)
    SRef.mixin(NetlistAspects)
    Shape.mixin(ShapeClipperAspects)

    Polygon.mixin(PolygonAspects)
    Polygon.mixin(NetlistAspects)
    Polygon.mixin(PolygonPortProperty)
    Polygon.mixin(PolygonClipperAspects)


load_aspect()
