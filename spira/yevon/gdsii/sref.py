import gdspy
import numpy
import inspect
import numpy as np
import spira.all as spira

from spira.yevon.geometry.ports.base import __Port__
from spira.yevon.gdsii.base import __Elemental__
from spira.yevon.geometry.coord import CoordField, Coord
from spira.yevon import utils
from spira.core.transforms import *
from spira.core.parameters.descriptor import DataFieldDescriptor, FunctionField, DataField

from spira.core.parameters.variables import *
from spira.yevon.geometry.vector import *
from spira.yevon.geometry.line import *
from copy import copy, deepcopy
from spira.core.transforms import stretching
from spira.yevon.geometry import bbox_info


class __RefElemental__(__Elemental__):

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
        if not isinstance(other, SRef): return False
        return (self.ref == other.ref) and (self.midpoint == other.position) and (self.transformation == other.transformation)

    def expand_transform(self):

        # C = spira.Cell(
        C = self.ref.__class__(
            name=self.ref.name + self.transformation.id_string(),
            alias=self.ref.alias + self.alias,
            elementals=deepcopy(self.ref.elementals),
            ports=deepcopy(self.ref.ports)
        )

        T = self.transformation + spira.Translation(self.midpoint)
        C = C.transform(T)

        # NOTE: Applies expantion hierarchically.
        # Expands all references in the cell.
        C.expand_transform()

        self.ref = C
        self.transformation = None
        self.midpoint = (0,0)

        return self

    def expand_flat_copy(self):
        S = self.expand_transform()
        C = spira.Cell(name=S.ref.name + '_ExpandedCell')
        def flat_polygons(subj, cell):
            for e in cell.elementals:
                if isinstance(e, spira.Polygon):
                    subj += e
                elif isinstance(e, spira.SRef):
                    flat_polygons(subj=subj, cell=e.ref)
            # for p in cell.ports:
            #     port = spira.Port(
            #         # name=p.name + "_" + cell.name,
            #         name=p.name,
            #         locked=False,
            #         midpoint=deepcopy(p.midpoint),
            #         orientation=deepcopy(p.orientation),
            #         width=deepcopy(p.width),
            #         local_pid=p.local_pid
            #     )
            #     subj.ports += port
            return subj
        D = flat_polygons(C, S.ref)
        return SRef(reference=D)
        # return self.__class__(reference=D)


class SRef(__RefElemental__):
    """
    Cell reference (SRef) is the reference to a cell layout
    to create a hierarchical layout structure. It creates copies
    of the ports and terminals defined by the cell. These
    copied ports can be used to connect different
    cell reference instances.

    Examples
    --------
    >>> cell = spira.Cell(name='Layout')
    >>> sref = spira.SRef(structure=cell)
    """

    supp = IntegerField(default=1)
    midpoint = CoordField(default=(0,0))

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

    def __repr__(self):
        name = self.ref.name
        return ("[SPiRA: SRef] (\"{}\", midpoint {}, transforms {})".format(name, self.midpoint, self.transformation))

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return hash(self.__repr__())

    def id_string(self):
        return self.__repr__()

    def dependencies(self):
        from spira.yevon.gdsii.cell_list import CellList
        d = CellList()
        d.add(self.ref)
        d.add(self.ref.dependencies())
        return d

    def flatten(self):
        return self.ref.flatten()

    def flat_copy(self, level=-1):
        if level == 0: return spira.ElementalList(self.__copy__())
        el = self.ref.elementals.flat_copy(level-1)
        T = self.transformation + Translation(self.midpoint)
        el.transform(T)
        return el

    @property
    def bbox_info(self):
        T = self.transformation + Translation(self.midpoint)
        return self.ref.bbox_info.transform(T)

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
        # self.midpoint = Coord(self.midpoint[0] + position[0], self.midpoint[1] + position[1])
        dxdy = Coord(self.midpoint[0] + position[0], self.midpoint[1] + position[1])
        self.translate(dxdy)
        return self

    def connect(self, port, destination):
        """ Connect the reference internal port with an external port.

        Example:
        --------
        >>> S.connect()
        """
        if issubclass(type(port), __Port__):
            p = port
        elif port in self.ports.get_names():
            if issubclass(type(port), __Port__):
                p = self.ports[port.name]
            elif isinstance(port, str):
                p = self.ports[port]
        else:
            raise ValueError("[SPiRA] connect() did not receive a Port or " +
                "valid port name - received ({}), ports available " +
                "are ({})".format(port, self.ports.get_names()))

        if not isinstance(destination, spira.Port):
            raise ValueError('Destination is not a terminal.')

        T = vector_match_transform(v1=p, v2=destination)
        self.transform(T)
        self.supp = 2

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

    def stretch(self, factor=(1,1), center=(0,0)):
        S = self.expand_flat_copy()
        T = spira.Stretch(stretch_factor=factor, stretch_center=center)
        for i, e in enumerate(S.ref.elementals):
            # T.apply(S.ref.elementals[i])
            S.ref.elementals[i].transform(T)
        return self
        # return S

    def stretch_copy(self, factor=(1,1), center=(0,0)):
        pass
        # S = self.expand_flat_copy()
        # T = spira.Stretch(stretch_factor=factor, stretch_center=center)
        # for i, e in enumerate(S.ref.elementals):
        #     T.apply(S.ref.elementals[i])
        # return self

    def stretch_port(self, port, destination):
        """
        The elemental by moving the subject port, without
        distorting the entire elemental. Note: The opposite port
        position is used as the stretching center.

        Example
        -------
        >>> S_s = S.stretch_port()
        """
        from spira.yevon.gdsii.polygon import Polygon
        opposite_port = bbox_info.get_opposite_boundary_port(self, port)
        T = stretching.stretch_elemental_by_port(self, opposite_port, port, destination)
        if port.bbox is True:
            for i, e in enumerate(self.ref.elementals):
                T.apply(self.ref.elementals[i])
        else:
            for i, e in enumerate(self.ref.elementals):
                if isinstance(e, Polygon):
                    if e.id_string() == port.local_pid:
                        opposite_port = bbox_info.get_opposite_boundary_port(e, port)
                        Tn = stretching.stretch_elemental_by_port(self, opposite_port, port, destination)
                        Tn.apply(self.ref.elementals[i])
        return self

    def nets(self, lcar, contacts=None):
        from spira.yevon.gdsii.pcell import Device
        # if isinstance(self.ref, Device): lcar = 10
        nets = self.ref.nets(lcar, contacts)
        # T = self.transformation + Translation(self.midpoint)
        # nets.transform(T)
        return nets 


class ARef(__RefElemental__):
    pass






