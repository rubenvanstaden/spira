import gdspy
import numpy
import inspect
import numpy as np
import spira.all as spira
from copy import copy, deepcopy

from spira.yevon.geometry.ports.base import __Port__
from spira.core import param
from spira.yevon.gdsii.base import __Elemental__
from spira.yevon.geometry.coord import CoordField, Coord
from spira.yevon import utils
from spira.core.transforms import *
from spira.core.descriptor import DataFieldDescriptor, FunctionField, DataField

from spira.core.param.variables import *


class __SRef__(__Elemental__):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return SRef(
            # reference=self.ref,
            reference=deepcopy(self.ref),
            transformation=deepcopy(self.transformation),
            port_locks=self.port_locks,
            midpoint=deepcopy(self.midpoint),
            # rotation=self.rotation,
            # magnification=self.magnification,
            node_id=deepcopy(self.node_id),
            # reflection=self.reflection
        )

    # def __eq__(self, other):
    #     return self.__str__() == other.__str__()

    def __eq__(self, other):
        if not isinstance(other, SRef):
            return False
        return (self.ref == other.ref) and (self.midpoint == other.position) and (self.transformation == other.transformation) 

    def expand_transform(self):
        S = spira.Cell(
            name=self.ref.name + self.transformation.id_string(),
            alias=self.ref.alias + self.alias,
            elementals=deepcopy(self.ref.elementals),
            ports=deepcopy(self.ref.ports)
        )
        S = S.transform(self.transformation)
        self.ref = S
        self.transformation = None
        return self


class SRefAbstract(gdspy.CellReference, __SRef__):

    midpoint = CoordField(default=(0,0))

    def __translate__(self, dx=0, dy=0):
        self.origin = self.midpoint
        super().translate(dx=dx, dy=dy)
        self.midpoint = self.origin
        return self

    def __rotate__(self, angle=45, center=(0,0)):
        if angle == 0:
            return self
        if issubclass(type(center), __Port__):
            center = center.midpoint
        if isinstance(center, Coord):
            center = center.convert_to_array()
        if isinstance(self.midpoint, Coord):
            self.midpoint = self.midpoint.convert_to_array()
        # if self.transformation is None:
        #     self.transformation = spira.Rotation(rotation=angle, center=center)
        # else:
        #     self.transformation += spira.Rotation(rotation=angle, center=center)
        self.midpoint = utils.rotate_algorithm(self.midpoint, angle, center)
        return self

    def __reflect__(self, p1=(0,0), p2=(1,0)):
        self.midpoint = utils.reflect_algorithm(self.midpoint)
        return self
        
    def commit_to_gdspy(self, cell, transformation=None):
        self.ref.commit_to_gdspy(cell=cell, transformation=self.transformation)

    def dependencies(self):
        from spira.yevon.gdsii.cell_list import CellList
        d = CellList()
        d.add(self.ref)
        d.add(self.ref.dependencies())
        return d

    def flatten(self):
        return self.ref.flatten()

    def flat_copy(self, level=-1):
        """  """
        if level == 0:
            el = spira.ElementList()
            el += self
            return el
        el = self.ref.elementals.flat_copy(level-1)
        if self.transformation is None:
            el.transform(Translation(self.midpoint))
        else:
            el.transform(self.transformation + Translation(self.midpoint))
        return el

    @property
    def ports(self):
        ports = spira.PortList()
        for p in self.ref.ports:
            ports += p.transform_copy(self.transformation)
        return ports
        
    def move(self, midpoint=(0,0), destination=None, axis=None):

        if destination is None:
            destination = midpoint
            midpoint = [0,0]
    
        if issubclass(type(midpoint), __Port__):
            o = midpoint.midpoint
        elif isinstance(midpoint, Coord):
            o = midpoint
        elif np.array(midpoint).size == 2:
            o = midpoint
        elif midpoint in self.ports:
            o = self.ports[midpoint].midpoint
        else:
            raise ValueError("[PHIDL] [DeviceReference.move()] ``midpoint`` " +
                                "not array-like, a port, or port name")
    
        if issubclass(type(destination), __Port__):
            d = destination.midpoint
        elif isinstance(destination, Coord):
            d = destination
        elif np.array(destination).size == 2:
            d = destination
        elif destination in self.ports:
            d = self.ports[destination].midpoint
        else:
            raise ValueError("[PHIDL] [DeviceReference.move()] ``destination`` " +
                                "not array-like, a port, or port name")

        # d = Coord(d[0], d[1])
        # o = Coord(o[0], o[1])

        # dxdy = d - o

        dxdy = np.array([d[0], d[1]]) - np.array([o[0], o[1]])

        if self.transformation is None:
            self.transformation = spira.Translation(translation=dxdy)
        else:
            self.transformation += spira.Translation(translation=dxdy)

        # self.__translate__(dx=dxdy[0], dy=dxdy[1])
        # self.midpoint = Coord(self.midpoint[0] + dxdy[0], self.midpoint[1] + dxdy[1])
        # self.midpoint = Coord(self.midpoint[0] - d[0], self.midpoint[1] - d[1])
        # self.midpoint = Coord(self.midpoint) + dxdy
        # self.midpoint = np.array(self.midpoint) + dxdy
        return self

    # def move(self, midpoint=(0,0), destination=None, axis=None):
    #     d, o = utils.move_algorithm(obj=self, midpoint=midpoint, destination=destination, axis=axis)
    #     dxdy = np.array(d) - np.array(o)
    #     print(dxdy)
    #     if not isinstance(self.midpoint, Coord):
    #         self.midpoint = Coord(self.midpoint)
    #     # self.midpoint = np.array(self.midpoint) + np.array(dxdy)
    #     # self.midpoint += dxdy
    #     if self.transformation is None:
    #         self.transformation = spira.Translation(translation=dxdy)
    #     else:
    #         self.transformation += spira.Translation(translation=dxdy)
    #     # self.midpoint.move(dxdy)
    #     return self

    def connect(self, port, destination):
        """  """
        # if port in self.ports.keys():
        #     p = self.ports[port]
        if port in self.ports.get_names():
            p = self.ports[port]
        elif issubclass(type(port), __Port__):
            p = port
        else:
            raise ValueError("[SPiRA] connect() did not receive a Port or " +
                "valid port name - received ({}), ports available " +
                "are ({})").format(port, self.ports.keys()
            )
        angle = 180 + destination.orientation - p.orientation
        # print('------------ angle')
        # print(angle)
        # self.rotate(angle=angle, center=p.midpoint)
        # self._rotate(rotation=angle, center=p.midpoint)
        print(self.midpoint)
        self.__rotate__(angle=angle, center=p.midpoint)
        # # self.midpoint = utils.rotate_algorithm(self.midpoint, angle, p.midpoint)
        # self.transformation.apply_to_object(self)
        print(destination)
        print(p.midpoint)
        # self.move(midpoint=p, destination=destination)
        print(self.midpoint)
        # self.transformation.apply_to_object(self)
        return self

    def align(self, p1, p2, distance):
        """  """
        pass


class SRef(SRefAbstract):
    """ Cell reference (SRef) is the reference to a cell layout
    to create a hierarchical layout structure. It creates copies
    of the ports and terminals defined by the cell. These
    copied ports can be used to connect different
    cell reference instances.

    Examples
    --------
    >>> cell = spira.Cell(name='Layout')
    >>> sref = spira.SRef(structure=cell)
    """

    port_locks = DictField(default={})
    port_connects = DictField(default={})

    def get_alias(self):
        if not hasattr(self, '__alias__'):
            self.__alias__ = '_S0'
        return self.__alias__

    def set_alias(self, value):
        self.__alias__ = '_' + value

    alias = FunctionField(get_alias, set_alias, doc='Functions to generate an alias for cell name.')

    def __init__(self, reference, **kwargs):
        __SRef__.__init__(self, **kwargs)

        self.ref = reference

        # self._local_ports = {}
        # self._parent_ports = []

        # for p in reference.ports:
        #     self._parent_ports.append(p)
        # for t in reference.terms:
        #     self._parent_ports.append(t)

        # self.iports = {}

    # def __repr__(self):
    #     name = self.ref.name
    #     return ("[SPiRA: SRef] (\"{}\", at {}, srefs {}, cells {}, " +
    #        "polygons {}, ports {}, labels {})").format(
    #         name, self.midpoint,
    #         len(self.ref.elementals.sref),
    #         len(self.ref.elementals.cells),
    #         len(self.ref.elementals.polygons),
    #         len(self.ref.ports),
    #         len(self.ref.elementals.labels)
    #     )

    def __repr__(self):
        name = self.ref.name
        return ("[SPiRA: SRef] (\"{}\", transforms {})".format(name, self.transformation))

    def __str__(self):
        return self.__repr__()

    @property
    def translation(self):
        if self.transformation is not None:
            return self.transformation.translation
        else:
            return 0.0

    @property
    def rotation(self):
        if self.transformation is not None:
            return self.transformation.rotation
        else:
            return 0.0

    @property
    def reflection(self):
        if self.transformation is not None:
            return self.transformation.reflection
        else:
            return False

    @property
    def magnification(self):
        if self.transformation is not None:
            return self.transformation.magnification
        else:
            return 1.0

    @property
    def polygons(self):
        # FIXME: Assums all elementals are ply.Polygon.
        elems = spira.ElementList()
        for p in self.ref.elementals:
            elems += p.transform_copy(self.transformation)
        return elems










