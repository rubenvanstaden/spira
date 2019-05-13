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
from spira.yevon.geometry.vector import *
from spira.yevon.geometry.line import *


class __RefElemental__(__Elemental__):

    __committed__ = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return SRef(
            reference=deepcopy(self.ref),
            # reference=self.ref,
            midpoint=deepcopy(self.midpoint),
            transformation=deepcopy(self.transformation),
            node_id=deepcopy(self.node_id)
        )

    def __eq__(self, other):
        if not isinstance(other, SRef):
            return False
        return (self.ref == other.ref) and (self.midpoint == other.position) and (self.transformation == other.transformation)

    def expand_transform(self):

        if self.transformation is None:
            name = self.ref.name + '_None'
        else:
            name = self.ref.name + self.transformation.id_string()

        S = spira.Cell(
            # name=self.ref.name + self.transformation.id_string(),
            name=name,
            alias=self.ref.alias + self.alias,
            elementals=deepcopy(self.ref.elementals),
            ports=deepcopy(self.ref.ports)
        )

        if self.transformation is None:
            tf = spira.Translation(self.midpoint)
        else:
            tf= self.transformation + spira.Translation(self.midpoint)

        S = S.transform(tf)

        # NOTE: Applies expantion hierarchically.
        # Expands all references in the cell.
        S.expand_transform()

        self.ref = S
        self.transformation = None
        self.midpoint = (0,0)
        return self

    def flat_expand(self):
        from spira.yevon import process as pc
        S = self.expand_transform()
        C = spira.Cell(name=S.ref.name + '_ExpandedCell')
        def flat_polygons(subj, cell):
            for e in cell.elementals:
                if issubclass(type(e), pc.ProcessLayer):
                    subj += e
                elif isinstance(e, spira.SRef):
                    flat_polygons(subj=subj, cell=e.ref)
            return subj
        D = flat_polygons(C, S.ref)
        return D


class SRefAbstract(gdspy.CellReference, __RefElemental__):

    midpoint = CoordField(default=(0,0))

    def commit_to_gdspy(self, cell, transformation=None):

        if self.__repr__() not in list(__RefElemental__.__committed__.keys()):

            # # tf = self.transformation
            # if self.transformation is None:
            #     tf = spira.Translation(self.midpoint)
            # else:
            #     tf = self.transformation + spira.Translation(self.midpoint)
            # if transformation is not None:
            #     tf = tf + transformation
            # self.ref.commit_to_gdspy(cell=cell, transformation=tf)

            self.ref.commit_to_gdspy(cell=cell)

            __RefElemental__.__committed__.update({self.__repr__(): self})
        else:
            __RefElemental__.__committed__[self.__repr__()]

    def transform_copy(self, transformation):
        self = super().transform_copy(transformation)
        return self.expand_transform()

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
        # if self.transformation is None:
        #     el.transform(Translation(self.midpoint))
        # else:
        #     el.transform(self.transformation + Translation(self.midpoint))
        return el

    @property
    def ports(self):
        ports = spira.PortList()
        for p in self.ref.ports:

            # ports += p.transform_copy(self.transformation)
            # ports += p.transform_copy(self.transformation).move(self.midpoint)

            pp = p.transform_copy(self.transformation).move(self.midpoint)
            # T = spira.Rotation(90, center=(-10*1e6, 0))
            # pp = pp.transform(T)
            ports += pp

            # if self.transformation is not None:
            #     ports += p.transform_copy(self.transformation).move(self.midpoint).transform(-self.transformation)

        return ports

    # def move(self, position):
    #     self.midpoint = Coord(self.midpoint[0] + position[0], self.midpoint[1] + position[1])
    #     return self

    def move(self, midpoint=(0,0), destination=None, axis=None):
        """ Move the reference internal port to the destination.

        Example:
        --------
        >>> S.move()
        """

        if destination is None:
            destination = midpoint
            midpoint = [0,0]

        if isinstance(midpoint, Coord):
            o = midpoint
        elif np.array(midpoint).size == 2:
            o = midpoint
        # elif midpoint in self.ports:
            # o = self.ports[midpoint].midpoint
        elif midpoint in self.ports.get_names():
            o = self.ports[midpoint.name].midpoint
        elif issubclass(type(midpoint), __Port__):
            o = midpoint.midpoint
        else:
            raise ValueError("[PHIDL] [DeviceReference.move()] ``midpoint`` " +
                                "not array-like, a port, or port name")

        if issubclass(type(destination), __Port__):
            d = destination.midpoint
        elif isinstance(destination, Coord):
            d = destination
        elif np.array(destination).size == 2:
            d = destination
        # elif destination in self.ports:
        #     d = self.ports[destination].midpoint
        elif destination in self.ports.get_names():
            d = self.ports[destination.name].midpoint
        else:
            raise ValueError("[PHIDL] [DeviceReference.move()] ``destination`` " +
                                "not array-like, a port, or port name")

        position = np.array([d[0], d[1]]) - np.array([o[0], o[1]])
        self.midpoint = Coord(self.midpoint[0] + position[0], self.midpoint[1] + position[1])
        return self

    def connect(self, port, destination):
        """ Connect the reference internal port with an external port.

        Example:
        --------
        >>> S.connect()
        """
        if port in self.ports.get_names():
            if issubclass(type(port), __Port__):
                p = self.ports[port.name]
            elif isinstance(port, str):
                p = self.ports[port]
        elif issubclass(type(port), __Port__):
            p = port
        else:
            raise ValueError("[SPiRA] connect() did not receive a Port or " +
                "valid port name - received ({}), ports available " +
                "are ({})".format(port, self.ports.get_names()))

        if not isinstance(destination, spira.Terminal):
            raise ValueError('Destination is not a terminal.')

        T = vector_match_transform(v1=p, v2=destination)
        self.transform(T)

        return self

    def align(self, port, destination, distance):
        """ Align the reference using an internal port with an external port.

        Example:
        --------
        >>> S.align()
        """
        destination = deepcopy(destination)
        self.connect(port, destination)

        L = line_from_point_angle(point=destination.midpoint, angle=destination.orientation)
        dx, dy = L.get_coord_from_distance(destination, distance)

        T = spira.Translation(translation=(dx, dy))
        self.transform(T)

        return self


from spira.core.transforms.generic import GenericTransform
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

    def get_alias(self):
        if not hasattr(self, '__alias__'):
            self.__alias__ = '_S0'
        return self.__alias__

    def set_alias(self, value):
        self.__alias__ = '_' + value

    alias = FunctionField(get_alias, set_alias, doc='Functions to generate an alias for cell name.')

    def __init__(self, reference, **kwargs):
        __RefElemental__.__init__(self, **kwargs)

        self.ref = reference

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
        return ("[SPiRA: SRef] (\"{}\", midpoint {}, transforms {})".format(name, self.midpoint, self.transformation))

    def __str__(self):
        return self.__repr__()
        
    @property
    def _translation(self):
        # if self.transformation is not None:
        if issubclass(type(self.transformation), GenericTransform):
            return self.transformation.translation
        else:
            return (0,0)

    @property
    def rotation(self):
        # if self.transformation is not None:
        if issubclass(type(self.transformation), GenericTransform):
            return self.transformation.rotation
        else:
            return 0.0

    @property
    def reflection(self):
        # if self.transformation is not None:
        if issubclass(type(self.transformation), GenericTransform):
            return self.transformation.reflection
        else:
            return False

    @property
    def magnification(self):
        # if self.transformation is not None:
        if issubclass(type(self.transformation), GenericTransform):
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










