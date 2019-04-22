import spira.all as spira
from copy import copy, deepcopy
from numpy.linalg import norm
from spira.yevon import utils

from spira.yevon.gdsii.base import __Elemental__
from spira.yevon.rdd import get_rule_deck

from spira.core.param.variables import *
from spira.yevon.layer import LayerField
from spira.core.descriptor import DataField
from spira.yevon.geometry.coord import CoordField
from spira.yevon.geometry.ports.base import __VerticalPort__
from spira.yevon.gdsii.group import Group


class Port(Group, __VerticalPort__):
    """  """

    radius = FloatField(default=0.25*1e6)
    surface = DataField(fdef_name='create_surface')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        return ("[SPiRA: Port] (name {}, number {}, datatype {}, midpoint {}, " +
            "radius {}, orientation {})").format(self.name,
            self.gds_layer.number, self.gds_layer.datatype, self.midpoint,
            self.radius, self.orientation
        )
        
    # def commit_to_gdspy(self, cell=None):
    #     if self.__repr__() not in list(__Port__.__committed__.keys()):
    #         self.surface.commit_to_gdspy(cell=cell)
    #         self.label.commit_to_gdspy(cell=cell)
    #         Port.__committed__.update({self.__repr__(): self})
    #     else:
    #         p = Port.__committed__[self.__repr__()]
    #         p.surface.commit_to_gdspy(cell=cell)
    #         p.label.commit_to_gdspy(cell=cell)

    def create_surface(self):
        from spira.yevon.geometry import shapes
        shape = shapes.CircleShape(
            center=self.midpoint,
            box_size=[self.radius, self.radius]
        )
        layer = deepcopy(self.gds_layer)
        ply = spira.Polygon(shape=shape, gds_layer=layer)
        ply.move(midpoint=ply.center, destination=self.midpoint)
        return ply

    def create_elementals(self, elems):
        elems += self.surface
        elems += self.label
        return elems












