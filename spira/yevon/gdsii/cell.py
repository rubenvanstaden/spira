import gdspy
import numpy as np
import networkx as nx
from copy import copy, deepcopy

from spira.core.initializer import FieldInitializer
from spira.core.descriptor import DataFieldDescriptor, FunctionField, DataField
from spira.core.elem_list import ElementList, ElementalListField
from spira.yevon.geometry.coord import CoordField
from spira.yevon.visualization.color import ColorField
from spira.yevon.visualization import color
from spira.core.param.variables import NumberField
from spira.core.initializer import MetaCell
from spira.core.port_list import PortList
from spira.yevon.gdsii import *
from spira.yevon.rdd import get_rule_deck
from spira.core.mixin import MixinBowl


RDD = get_rule_deck()


__all__ = ['Cell', 'Connector', 'CellField']


class __Cell__(FieldInitializer, metaclass=MetaCell):

    __name_generator__ = RDD.ADMIN.NAME_GENERATOR

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_node_id(self):
        if self.__id__:
            return self.__id__
        else:
            return self.__str__()

    def set_node_id(self, value):
        self.__id__ = value

    # node_id = param.FunctionField(get_node_id, set_node_id, doc='Unique elemental ID.')
    node_id = FunctionField(get_node_id, set_node_id, doc='Unique elemental ID.')
    
    def __add__(self, other):
        from spira.yevon.geometry.ports.port import __Port__
        if other is None:
            return self
        if issubclass(type(other), __Port__):
            self.ports += other
        else:
            self.elementals += other
        return self


class CellAbstract(gdspy.Cell, __Cell__):

    def create_name(self):
        if not hasattr(self, '__name__'):
            self.__name__ = self.__name_generator__(self)
        return self.__name__

    def flatten(self):
        self.elementals = self.elementals.flatten()
        return self.elementals

    def transform(self, transformation=None):
        self.elementals.transform(transformation)
        return self

    def dependencies(self):
        deps = self.elementals.dependencies()
        deps += self
        return deps

    # def flat_copy(self, level=-1):
    #     elems = self.elementals.flat_copy(level)
    #     ports = self.ports.flat_copy(level)
    #     C = self.modified_copy(elementals=elems, ports=ports)
    #     return C

    # def flat_copy(self, level=-1):
    #     self.elementals = self.elementals.flat_copy(level)
    #     return self.elementals

    # def expand_transform(self):
    #     self.elementals.expand_transform()
    #     # self.transformation = None
    #     return self

    def commit_to_gdspy(self):
        from spira.yevon.gdsii.sref import SRef
        cell = gdspy.Cell(self.name, exclude_from_current=True)
        for e in self.elementals:
            if isinstance(e, SRef):
                e.ref.commit_to_gdspy()
            else:
                e.commit_to_gdspy(cell=cell)
        return cell

    def translate(self, dx, dy):
        for e in self.elementals:
            e.translate(dx=dx, dy=dy)
        for p in self.ports:
            p.translate(dx=dx, dy=dy)
        return self

    def move(self, midpoint=(0,0), destination=None, axis=None):
        from spira import pc
        d, o = super().move(midpoint=midpoint, destination=destination, axis=axis)
        for e in self.elementals:
            e.move(destination=d, midpoint=o)
        for p in self.ports:
            mc = np.array(p.midpoint) + np.array(d) - np.array(o)
            p.move(midpoint=p.midpoint, destination=mc)
        return self

    def reflect(self, p1=(0,0), p2=(1,0)):
        """ Reflects the cell around the line [p1, p2]. """
        for e in self.elementals:
            if not issubclass(type(e), LabelAbstract):
                e.reflect(p1, p2)
        for p in self.ports:
            p.midpoint = self.__reflect__(p.midpoint, p1, p2)
            phi = np.arctan2(p2[1]-p1[1], p2[0]-p1[0])*180 / np.pi
            p.orientation = 2*phi - p.orientation
        return self

    def rotate(self, angle=45, center=(0,0)):
        """ Rotates the cell with angle around a center. """
        from spira import pc
        if angle == 0:
            return self
        for e in self.elementals:
            if issubclass(type(e), PolygonAbstract):
                e.rotate(angle=angle, center=center)
            elif isinstance(e, SRef):
                e.rotate(angle=angle, center=center)
            elif issubclass(type(e), ProcessLayer):
                e.rotate(angle=angle, center=center)
        ports = self.ports
        self.ports = PortList()
        for p in ports:
            p.midpoint = self.__rotate__(p.midpoint, angle, center)
            p.orientation = np.mod(p.orientation + angle, 360)
            self.ports += p
        return self

    def get_ports(self, level=None):
        """ Returns copies of all the ports of the Device. """
        port_list = [deepcopy(p) for p in self.ports]
        if level is None or level > 0:
            for r in self.elementals.sref:

                if level is None:
                    new_level = None
                else:
                    new_level = level - 1

                ref_ports = r.ref.get_ports(level=new_level)

                ref_ports_transformed = []
                for rp in ref_ports:
                    pt = rp.transform_copy(r.get_transformation)
                    ref_ports_transformed.append(pt)
                port_list += ref_ports_transformed

        return port_list


class Cell(CellAbstract):
    """ A Cell encapsulates a set of elementals that
    describes the layout being generated. """

    # um = param.NumberField(default=1e6)
    # name = param.DataField(fdef_name='create_name', doc='Name of the cell instance.')
    # routes = param.ElementalListField(fdef_name='create_routes')
    # color = param.ColorField(default=color.COLOR_DARK_SLATE_GREY, doc='Color that a default cell will represent in a netlist.')
    
    um = NumberField(default=1e6)
    name = DataField(fdef_name='create_name', doc='Name of the cell instance.')
    routes = ElementalListField(fdef_name='create_routes')
    color = ColorField(default=color.COLOR_DARK_SLATE_GREY, doc='Color that a default cell will represent in a netlist.')

    _next_uid = 0

    def create_routes(self, routes):
        return routes

    def get_alias(self):
        if not hasattr(self, '__alias__'):
            self.__alias__ = self.name.split('__')[0]
        return self.__alias__

    def set_alias(self, value):
        self.__alias__ = value

    # alias = param.FunctionField(get_alias, set_alias, doc='Functions to generate an alias for cell name.')
    alias = FunctionField(get_alias, set_alias, doc='Functions to generate an alias for cell name.')

    def __init__(self, name=None, elementals=None, ports=None, nets=None, library=None, **kwargs):

        # CellInitializer.__init__(self, **kwargs)
        __Cell__.__init__(self, **kwargs)
        gdspy.Cell.__init__(self, self.name, exclude_from_current=True)

        self.g = nx.Graph()
        self.uid = Cell._next_uid
        Cell._next_uid += 1

        if name is not None:
            s = '{}_{}'.format(name, self.__class__._ID)
            self.__dict__['__name__'] = s
            Cell.name.__set__(self, s)
            self.__class__._ID += 1

        if library is not None:
            self.library = library
        if elementals is not None:
            self.elementals = elementals
        if ports is not None:
            self.ports = ports

    def __repr__(self):
        if hasattr(self, 'elementals'):
            elems = self.elementals
            return ("[SPiRA: Cell(\'{}\')] " +
                    "({} elementals: {} sref, {} cells, {} polygons, " +
                    "{} labels, {} ports)").format(
                        self.name,
                        elems.__len__(),
                        elems.sref.__len__(),
                        elems.cells.__len__(),
                        elems.polygons.__len__(),
                        elems.labels.__len__(),
                        self.ports.__len__()
                    )

    def __str__(self):
        return self.__repr__()


class Connector(Cell):
    """
    Terminals are horizontal ports that connect SRef instances
    in the horizontal plane. They typcially represents the
    i/o ports of a components.

    Examples
    --------
    >>> term = spira.Term()
    """

    # midpoint = param.MidPointField()
    midpoint = CoordField()
    # orientation = param.NumberField(default=0.0)
    # width = param.NumberField(default=2*1e6)
    orientation = NumberField(default=0.0)
    width = NumberField(default=2*1e6)

    def __repr__(self):
        return ("[SPiRA: Connector] (name {}, midpoint {}, " +
            "width {}, orientation {})").format(self.name,
            self.midpoint, self.width, self.orientation
        )

    def create_ports(self, ports):
        ports += Term(name='P1', midpoint=self.midpoint, width=self.width, orientation=self.orientation)
        ports += Term(name='P2', midpoint=self.midpoint, width=self.width, orientation=self.orientation-180)
        return ports


def CellField(name=None, elementals=None, ports=None, library=None, **kwargs):
    from spira.yevon.gdsii.cell import Cell
    if 'default' not in kwargs:
        kwargs['default'] = Cell(name=name, elementals=elementals, library=library)
    R = RestrictType(Cell)
    return DataFieldDescriptor(restrictions=R, **kwargs)
