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

    def __move_net__(self, g):
        for n in g.nodes():
            p = np.array(g.node[n]['pos'])
            m = np.array(self.midpoint)
            g.node[n]['pos'] = p + m
        return g

    def __equal_ports__(self, p1, p2):
        if p1.encloses_midpoint(p2.edge.points[0]):
            if p1.gds_layer.number == p2.gds_layer.number:
                return True
        return False

    def expand_transform(self):
        S = spira.Cell(
            name=self.ref.name + self.transformation.id_string(),
            alias=self.ref.alias + self.alias,
            elementals=deepcopy(self.ref.elementals)
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
        self.midpoint = utils.rotate_algorithm(self.midpoint, angle, center)
        return self

    def __reflect__(self, p1=(0,0), p2=(1,0)):
        self.midpoint = utils.reflect_algorithm(self.midpoint)
        return self

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
        el.transform(self.transformation + Translation(self.midpoint))
        return el

    @property
    def ports(self):
        for port in self._parent_ports:
            self._local_ports[port.name] = port.transform_copy(self.transformation)
        return self._local_ports

    def move(self, midpoint=(0,0), destination=None, axis=None):
        d, o = utils.move_algorithm(midpoint=midpoint, destination=destination, axis=axis)
        dxdy = np.array(d) - np.array(o)
        self.midpoint = np.array(self.midpoint) + dxdy
        return self

    def connect(self, port, destination):
        """  """
        if port in self.ports.keys():
            p = self.ports[port]
        elif issubclass(type(port), __Port__):
            p = port
        else:
            raise ValueError("[SPiRA] connect() did not receive a Port or " +
                "valid port name - received ({}), ports available " +
                "are ({})").format(port, self.ports.keys()
            )
        angle = 180 + destination.orientation - p.orientation
        self.rotate(angle=angle, center=p.midpoint)
        self.move(midpoint=p, destination=destination)
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

        # self._parent_ports = []
        # for p in structure.ports:
        #     self._parent_ports.append(p)
        # for t in structure.terms:
        #     self._parent_ports.append(t)
        # self._local_ports = {}
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










