import gdspy
import numpy as np
import networkx as nx
from copy import copy, deepcopy
from spira.yevon import utils

from spira.core.param.restrictions import RestrictType
from spira.core.initializer import FieldInitializer
from spira.core.descriptor import DataFieldDescriptor, FunctionField, DataField
from spira.core.elem_list import ElementList, ElementalListField
from spira.yevon.geometry.coord import CoordField, Coord
from spira.yevon.visualization.color import ColorField
from spira.yevon.visualization import color
from spira.core.param.variables import NumberField
from spira.core.initializer import MetaCell
from spira.core.port_list import PortList
from spira.yevon.gdsii import *
from spira.yevon.rdd import get_rule_deck
from spira.core.mixin import MixinBowl
from spira.yevon.gdsii.sref import SRef


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
        
    # def __deepcopy__(self, memo):
    #     print('wjfbwejfbjwekfbwejewkjfbkjbjfbijkbjrjvfdnivndfijvndkv')
    #     cell = Cell(
    #         name=self.name,
    #         elementals=deepcopy(self.elementals),
    #         ports=deepcopy(self.ports)
    #     )
    #     cell.__name__ = self.name
    #     cell.name = self.name
    #     print(cell)
    #     return cell


class CellAbstract(gdspy.Cell, __Cell__):

    def create_name(self):
        if not hasattr(self, '__name__'):
            self.__name__ = self.__name_generator__(self)
        return self.__name__

    def flatten(self):
        self.elementals = self.elementals.flatten()
        return self.elementals

    def dependencies(self):
        deps = self.elementals.dependencies()
        deps += self
        return deps

    def flat_copy(self, level=-1):
        name = '{}_{}'.format(self.name, 'flat'),
        C = Cell(name, self.elementals.flat_copy(level=level))
        return C

    def flat_polygons(self, subj):
        from spira.yevon.process.processlayer import ProcessLayer
        from spira.yevon.gdsii.sref import SRef
        for e1 in self.elementals:
            if isinstance(e1, ProcessLayer):
                subj += e1
            elif isinstance(e1, SRef):
                e1.ref.flat_polygons(subj=subj)
        return subj

    def commit_to_gdspy(self, cell, transformation=None):
        cell = gdspy.Cell(self.name, exclude_from_current=True)
        for e in self.elementals:
            # e = deepcopy(e)
            e.commit_to_gdspy(cell=cell, transformation=transformation)
        for p in self.ports:
            p.commit_to_gdspy(cell=cell, transformation=transformation)
        return cell

    def move(self, midpoint=(0,0), destination=None, axis=None):
        from spira.yevon import process as pc
        from spira.yevon.geometry.ports.base import __Port__
        # d, o = utils.move_algorithm(obj=self, midpoint=midpoint, destination=destination, axis=axis)

        if destination is None:
            destination = midpoint
            midpoint = [0,0]
    
        if issubclass(type(midpoint), __Port__):
            o = midpoint.midpoint
        elif isinstance(midpoint, Coord):
            o = midpoint
        elif np.array(midpoint).size == 2:
            o = midpoint
        elif midpoint in obj.ports:
            o = obj.ports[midpoint].midpoint
        else:
            raise ValueError("[PHIDL] [DeviceReference.move()] ``midpoint`` " +
                                "not array-like, a port, or port name")
    
        if issubclass(type(destination), __Port__):
            d = destination.midpoint
        elif isinstance(destination, Coord):
            d = destination
        elif np.array(destination).size == 2:
            d = destination
        elif destination in obj.ports:
            d = obj.ports[destination].midpoint
        else:
            raise ValueError("[PHIDL] [DeviceReference.move()] ``destination`` " +
                                "not array-like, a port, or port name")
    
        if axis == 'x':
            d = (d[0], o[1])
        if axis == 'y':
            d = (o[0], d[1])
    
        d = Coord(d[0], d[1])
        o = Coord(o[0], o[1])

        for e in self.elementals:
            e.move(midpoint=o, destination=d)

        for p in self.ports:
            mc = np.array(p.midpoint) + np.array(d) - np.array(o)
            p.move(midpoint=p.midpoint, destination=mc)

        return self


class Cell(CellAbstract):
    """ A Cell encapsulates a set of elementals that
    describes the layout being generated. """

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

    alias = FunctionField(get_alias, set_alias, doc='Functions to generate an alias for cell name.')

    def __init__(self, name=None, elementals=None, ports=None, nets=None, library=None, **kwargs):

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

    def transform(self, transformation=None):
        self.elementals.transform(transformation)
        self.ports.transform(transformation)
        return self

    def expand_transform(self):
        for S in self.elementals.sref:
            S.expand_transform()
            S.ref.expand_transform()
        return self

    @property
    def alias_cells(self):
        childs = {}
        for c in self.dependencies():
            childs[c.alias] = c
        return childs

    @property
    def alias_elems(self):
        elems = {}
        for e in self.elementals.polygons:
            elems[e.alias] = e
        return elems

    def __getitem__(self, key):
        from spira.yevon.gdsii.sref import SRef
        from spira.yevon.gdsii.polygon import Polygon
        keys = key.split(':')

        item = None
        if keys[0] in self.alias_cells:
            item = self.alias_cells[keys[0]]
        elif keys[0] in self.alias_elems:
            item = self.alias_elems[keys[0]]
        else:
            raise ValueError('Alias {} key not found!'.format(keys[0]))

        return item


class Connector(Cell):
    """
    Terminals are horizontal ports that connect SRef instances
    in the horizontal plane. They typcially represents the
    i/o ports of a components.

    Examples
    --------
    >>> term = spira.Terminal()
    """

    midpoint = CoordField()
    orientation = NumberField(default=0.0)
    width = NumberField(default=2*1e6)

    def __repr__(self):
        return ("[SPiRA: Connector] (name {}, midpoint {}, " +
            "width {}, orientation {})").format(self.name,
            self.midpoint, self.width, self.orientation
        )

    def create_ports(self, ports):
        ports += Terminal(name='P1', midpoint=self.midpoint, width=self.width, orientation=self.orientation)
        ports += Terminal(name='P2', midpoint=self.midpoint, width=self.width, orientation=self.orientation-180)
        return ports


def CellField(name=None, elementals=None, ports=None, library=None, **kwargs):
    from spira.yevon.gdsii.cell import Cell
    if 'default' not in kwargs:
        kwargs['default'] = Cell(name=name, elementals=elementals, library=library)
    R = RestrictType(Cell)
    return DataFieldDescriptor(restrictions=R, **kwargs)
