import gdspy
import numpy as np
import networkx as nx
from copy import copy, deepcopy
from spira.yevon import utils

from spira.core.parameters.restrictions import RestrictType
from spira.core.parameters.initializer import ParameterInitializer
from spira.core.parameters.descriptor import ParameterDescriptor, FunctionParameter, Parameter
from spira.yevon.gdsii.elem_list import ElementList, ElementListParameter
from spira.yevon.geometry.coord import CoordParameter, Coord
from spira.yevon.visualization.color import ColorParameter
from spira.yevon.visualization import color
from spira.core.parameters.variables import NumberParameter
from spira.core.parameters.initializer import MetaInitializer
from spira.yevon.geometry.ports.port_list import PortList
from spira.yevon.gdsii import *
from spira.core.mixin import MixinBowl
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = ['Cell', 'CellParameter']


class MetaCell(MetaInitializer):
    """
    Called when an instance of a SPiRA class is
    created. Pareses all kwargs and passes it to
    the ParameterInitializer for storing.

    class Via(spira.Cell):
        layer = param.LayerParameter()

    Gets called here and passes
    kwargs['layer': 50] to ParameterInitializer.
    >>> via = Via(layer=50)
    """

    def __call__(cls, *params, **keyword_params):

        kwargs = cls.__map_parameters__(*params, **keyword_params)

        from spira import settings
        lib = None
        if 'library' in kwargs:
            lib = kwargs['library']
            del(kwargs['library'])
        if lib is None:
            lib = settings.get_current_library()

        if 'name' in kwargs:
            if kwargs['name'] is None:
                kwargs['__name_prefix__'] = cls.__name__

        cls.__keywords__ = kwargs
        cls = super().__call__(**kwargs)

        retrieved_cell = lib.get_cell(cell_name=cls.name)
        if retrieved_cell is None:
            lib += cls
            return cls
        else:
            del cls
            return retrieved_cell


class __Cell__(ParameterInitializer, metaclass=MetaCell):

    __name_generator__ = RDD.ADMIN.NAME_GENERATOR

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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

    def __add__(self, other):
        from spira.yevon.geometry.ports.port import __Port__
        if other is None:
            return self
        if issubclass(type(other), __Port__):
            self.ports += other
        else:
            self.elements += other
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
        for e in self.elements.polygons:
            elems[e.alias] = e
        return elems

    def dependencies(self):
        deps = self.elements.dependencies()
        deps += self
        return deps

    def flat_copy(self, level=-1):
        name = '{}_{}'.format(self.name, 'Flat'),
        # return self.__class__(name, self.elements.flat_copy(level=level))
        return Cell(name, elements=self.elements.flat_copy(level=level))

    def is_layer_in_cell(self, layer):
        D = deepcopy(self)
        for e in D.flatten():
            return (e.layer == layer)
        return False


class Cell(__Cell__):
    """ A Cell encapsulates a set of elements that
    describes the layout being generated. """

    _next_uid = 0

    lcar = NumberParameter(default=100)
    name = Parameter(fdef_name='create_name', doc='Name of the cell instance.')

    def get_alias(self):
        if not hasattr(self, '__alias__'):
            self.__alias__ = self.name.split('__')[0]
        return self.__alias__

    def set_alias(self, value):
        self.__alias__ = value

    alias = FunctionParameter(get_alias, set_alias, doc='Functions to generate an alias for cell name.')

    def __init__(self, name=None, elements=None, ports=None, library=None, **kwargs):
        super().__init__(**kwargs)

        if name is not None:
            s = '{}_{}'.format(name, Cell._next_uid)
            self.__dict__['__name__'] = s
            Cell.name.__set__(self, s)

        self.uid = Cell._next_uid
        Cell._next_uid += 1

        if library is not None:
            self.library = library
        if elements is not None:
            self.elements = ElementList(elements)
        if ports is not None:
            self.ports = PortList(ports)

    def __repr__(self):
        class_string = "[SPiRA: Cell(\'{}\')] (elements {}, ports {})"
        return class_string.format(self.name, self.elements.__len__(), self.ports.__len__())

    def __str__(self):
        return self.__repr__()

    def __deepcopy__(self, memo):
        # FIXME: Check with stretching.
        return self.__class__(
        # return Cell(
            # name=self.name + '_copy',
            # name=self.name,
            alias=self.alias,
            elements=deepcopy(self.elements),
            ports=deepcopy(self.ports)
        )

    def create_name(self):
        if not hasattr(self, '__name__'):
            self.__name__ = self.__name_generator__(self)
        return self.__name__

    def create_netlist(self):
        net = self.nets(lcar=self.lcar).disjoint()
        return net

    def nets(self, lcar):
        return self.elements.nets(lcar=lcar)

    def expand_transform(self):
        self.elements.expand_transform()
        return self

    def flat_container(self, cc, name_tree=[]):
        self.elements.flat_container(cc, name_tree=name_tree)
        return cc

    def expand_flat_copy(self, exclude_devices=False):
        from spira.yevon.gdsii.pcell import Device
        from spira.yevon.gdsii.polygon import Polygon
        from spira.yevon.gdsii.sref import SRef
        S = self.expand_transform()
        cell = Cell(name=S.name + '_ExpandedCell')
        D = S.flat_container(cc=cell, name_tree=[])
        return cell

    def move(self, midpoint=(0,0), destination=None, axis=None):
        """  """
        from spira.yevon.geometry.ports.base import __Port__

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

        for e in self.elements:
            e.move(midpoint=o, destination=d)

        for p in self.ports:
            # mc = np.array(p.midpoint) + np.array(d) - np.array(o)
            mc = np.array([p.midpoint[0], p.midpoint[1]]) + np.array([d[0], d[1]]) - np.array([o[0], o[1]])
            # p.move(midpoint=p.midpoint, destination=mc)
            # print(p)
            p.move(mc)

        return self

    def stretch_p2p(self, port, destination):
        """
        The element by moving the subject port, without
        distorting the entire element. Note: The opposite
        port position is used as the stretching center.
        """
        from spira.core.transforms import stretching
        from spira.yevon.geometry import bbox_info
        from spira.yevon.gdsii.polygon import Polygon
        opposite_port = bbox_info.bbox_info_opposite_boundary_port(self, port)
        T = stretching.stretch_element_by_port(self, opposite_port, port, destination)
        if port.bbox is True:
            self = T(self)
        else:
            for i, e in enumerate(self.elements):
                if isinstance(e, Polygon):
                    if e.id_string() == port.local_pid:
                        self.elements[i] = T(e)
        return self


def CellParameter(local_name=None, restriction=None, **kwargs):
    R = RestrictType(Cell) & restriction
    return ParameterDescriptor(local_name, restriction=R, **kwargs)


