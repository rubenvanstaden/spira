import gdspy
import numpy
import inspect
import numpy as np

from spira.yevon.geometry.ports.base import __Port__
from spira.yevon.gdsii.base import __Element__
from spira.yevon.geometry.coord import CoordParameter, Coord
from spira.yevon import utils
from spira.core.transforms import *
from spira.core.parameters.initializer import SUPPRESSED
from spira.core.parameters.descriptor import ParameterDescriptor, FunctionParameter, Parameter

from spira.core.parameters.variables import *
from spira.yevon.geometry.vector import *
from spira.yevon.geometry.line import *
from copy import copy, deepcopy
from spira.core.transforms import stretching
from spira.yevon.gdsii.cell import CellParameter


class __RefElement__(__Element__):

    reference = CellParameter()
    alias = StringParameter(allow_none=True, default=None)

    def __init__(self, transformation=None, **kwargs):
        super().__init__(transformation=transformation, **kwargs)

    @property
    def bbox_info(self):
        T = self.transformation + Translation(self.midpoint)
        return self.reference.bbox_info.transform(T)


class SRef(__RefElement__):
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

    midpoint = CoordParameter(default=(0,0))

    def __init__(self, reference, midpoint=(0,0), alias=None, transformation=None, **kwargs):
        super().__init__(reference=reference, midpoint=midpoint, alias=alias, transformation=transformation, **kwargs)

    def __repr__(self):
        name = self.reference.name
        ps = "[SPiRA: SRef] (\"{}\", alias {}, midpoint {}, transforms {})"
        return (ps.format(name, self.alias, self.midpoint, self.transformation))

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return hash(self.__repr__())

    def __deepcopy__(self, memo):
        # return SRef(
        return self.__class__(
            alias=self.alias,
            reference=deepcopy(self.reference),
            midpoint=deepcopy(self.midpoint),
            # midpoint=self.midpoint,
            transformation=deepcopy(self.transformation)
        )

    def __eq__(self, other):
        if not isinstance(other, SRef):
            return False
        return (
            (self.reference == other.reference) and
            (self.midpoint == other.position) and
            (self.transformation == other.transformation)
        )

    def id_string(self):
        return self.__repr__()

    def dependencies(self):
        from spira.yevon.gdsii.cell_list import CellList
        d = CellList()
        d.add(self.reference)
        d.add(self.reference.dependencies())
        return d

    def net_source(self):
        return 'source: {}'.format(self.reference.name)

    def net_target(self):
        return 'target: {}'.format(self.reference.name)

    def is_valid_path(self):
        return True

    def expand_transform(self):
        from spira.yevon.gdsii.sref import SRef
        from spira.yevon.gdsii.polygon import Polygon
        from spira.core.transforms.identity import IdentityTransform

        C = self.reference.__class__(
            name='{}_{}'.format(self.reference.name, self.transformation.id_string()),
            elements=deepcopy(self.reference.elements),
            ports=deepcopy(self.reference.ports)
        )

        T = self.transformation + spira.Translation(self.midpoint)

        for i, e in enumerate(C.elements):
            if isinstance(e, SRef):
                e.midpoint = self.transformation.apply_to_coord(e.midpoint).move(self.midpoint)
                e.transform(self.transformation)
            elif isinstance(e, Polygon):
                e.transform(T)
        C.ports.transform(T)

        self.reference = C
        self.transformation = None
        self.midpoint = (0, 0)

        return self

    def expand_flat_copy(self):
        """  """
        D = self.reference.expand_flat_copy()
        return SRef(reference=D)
        # return self.__class__(reference=D)

    def flat_copy(self, level=-1):
        if level == 0: return spira.ElementList(self.__copy__())
        elems = self.reference.elements.flat_copy(level-1)
        T = self.transformation + Translation(self.midpoint)
        elems = elems.transform(T)
        return elems

    def flatten(self, level=-1, name_tree=[]):
        if level == 0: return self.reference
        name_tree.append(self.alias)
        nt = deepcopy(name_tree)
        D = self.reference.flatten(level, name_tree=nt)
        name_tree.pop()
        return D.elements
        
    def flat_container(self, cc, name_tree=[]):
        if self.alias is None:
            self.alias = ''
        name_tree.append(self.alias)
        nt = deepcopy(name_tree)
        self.reference.flat_container(cc, name_tree=nt)
        name_tree.pop()

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
        elif destination in self.ports.get_names():
            d = self.ports[destination.name].midpoint
        else:
            raise ValueError("[PHIDL] [DeviceReference.move()] ``destination`` " +
                                "not array-like, a port, or port name")

        position = np.array([d[0], d[1]]) - np.array([o[0], o[1]])
        self.midpoint = Coord(self.midpoint[0] + position[0], self.midpoint[1] + position[1])
        # dxdy = Coord(self.midpoint[0] + position[0], self.midpoint[1] + position[1])
        # self.translate(dxdy)
        return self

    def connect(self, port, destination, ignore_process=False):
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
            raise ValueError('Destination has to be a port.')

        if (ignore_process is False) and (p.process != destination.process):
            raise ValueError('Cannot connect ports from different processes.')

        T = vector_match_transform(v1=p, v2=destination)
        self.midpoint = T.apply_to_coord(self.midpoint)
        self.transform(T - spira.Translation(self.midpoint))
        # self.transformation = T - spira.Translation(self.midpoint)
        # self.transformation = T
        # print(T - spira.Translation(self.midpoint))
        # print(T)

        return self

    def distance_alignment(self, port, destination, distance):
        """ Align the reference using an internal port with an external port.

        Example:
        --------
        >>> S.distance_alignment()
        """
        destination = deepcopy(destination)
        self.connect(port, destination)

        L = line_from_point_angle(point=destination.midpoint, angle=destination.orientation)
        dx, dy = L.get_coord_from_distance(destination, distance)

        # self.move(midpoint=self.midpoint, destination=(dx,dy))
        T = spira.Translation(translation=(dx, dy))
        self.midpoint = T.apply_to_coord(self.midpoint)
        # self.transform(T - spira.Translation(self.midpoint))
        # self.transform(T)

        return self

    def center_alignment(self, p1, p2):
        """
        Place the reference `midpoint` at the virtual
        intersection line of two ports.

        Example
        -------
        >>> s.center_alignment(p1=self.p3, p2=self.via1_i5.ports['M5_P2'])
        """
        l1 = line_from_point_angle(point=p1.midpoint, angle=p1.orientation)
        l2 = line_from_point_angle(point=p2.midpoint, angle=p2.orientation)
        coord = l1.intersection(l2)
        self.move(midpoint=self.midpoint, destination=coord)
        return self

    # FIXME~~~~ Look at lieze_dcsfq.py
    def port_alignment(self, ports, p1, p2):
        """
        Align `ports[0]` of reference with `p1` and 
        `ports[1]` of reference with external port `p2`.

        Example
        -------
        >>>
        """
        self.connect(ports[0], deepcopy(p1))
        # print(self.transformation)

        if isinstance(ports[1], str):
            pin1 = self.ports[ports[1]]
        elif issubclass(type(ports[1]), __Port__):
            # pin1 = ports[1].transform(self.transformation)
            pin1 = ports[1].transform(spira.Translation(self.midpoint))

        # print(pin1)
        # print(p2)
        # print(ports[0])

        if ports[0].orientation in (0, 180):
            T = vector_match_axis(v1=pin1, v2=p2, axis='x')
        elif ports[0].orientation in (90, 270):
            T = vector_match_axis(v1=pin1, v2=p2, axis='y')

        T = T + self.transformation
        # self.midpoint = T.apply_to_coord(Coord(0,0))
        # self.midpoint = T.apply_to_coord(self.midpoint)
        # self.transform(T + spira.Translation(self.midpoint))
        self.transform(T)

        return self

    def stretch_by_factor(self, factor=(1,1), center=(0,0)):
        """
        Strecth the entire instance by a factor and around a specified center.

        Example
        -------
        >>> S.stretch_by_factor(factor=(2,1))
        """
        S = self.expand_flat_copy()
        T = spira.Stretch(stretch_factor=factor, stretch_center=center)
        for i, e in enumerate(S.reference.elements):
            S.reference.elements[i].transform(T)
        return self

    def stretch_p2c(self, port_name, destination_coord):
        """
        Stretch port to port. Stretch the polygon by moving
        the polygon edge port to the destination port location.

        Note
        ----
        The opposite port position is used as the stretching center.
        This overcomes the issue of distorting the entiry structure.

        Example
        -------
        >>> S.stretch_p2p(port_name='S1:Sr1:E3_R1', destination_coord=(10,0))
        """
        from spira.yevon.gdsii.polygon import Polygon
        from spira.yevon.geometry.bbox_info import bbox_info_opposite_boundary_port
        D = self.expand_flat_copy()
        
        port = D.ports[port_name]
        destination = D.ports[destination_name]
    
        for i, e in enumerate(D.reference.elements.polygons):
            if e.id_string() == port.local_pid:
                opposite_port = bbox_info_opposite_boundary_port(e, port)
                T = stretching.stretch_element_by_port(self, opposite_port, port, destination)
                T.apply(D.reference.elements[i])

    def stretch_p2p(self, port_name, destination_name):
        """
        Stretch port to port. Stretch the polygon by moving
        the polygon edge port to the destination port location.

        Note
        ----
        The opposite port position is used as the stretching center.
        This overcomes the issue of distorting the entiry structure.

        Example
        -------
        >>> S.stretch_p2p(port_name='S1:Sr1:E3_R1', destination_name='S2:Sr2:E1_R1')
        """
        from spira.yevon.gdsii.polygon import Polygon
        from spira.yevon.geometry.ports import PortList
        from spira.yevon.geometry.bbox_info import bbox_info_opposite_boundary_port

        D = self.expand_flat_copy()

        # print(D.ports)
        # print('\n------------------\n')

        # print('\n*************************************')
        ports = PortList()
        for e in D.reference.elements.polygons:
            # print(e.edge_ports)
            ports += e.edge_ports

        port = ports[port_name]
        destination = ports[destination_name]

        # print(port)
        # print(destination)

        for i, e in enumerate(D.reference.elements.polygons):
            if e.id_string() == port.local_pid:
                opposite_port = bbox_info_opposite_boundary_port(e, port)
                T = stretching.stretch_element_by_port(self, opposite_port, port, destination)
                T.apply(D.reference.elements[i])

    def nets(self, lcar):
        """  """

        from spira.yevon.geometry.nets.net_list import NetList
        nets = NetList()
        nets += self.reference.netlist

        # FIXME: Is this transformation required?
        # T = self.transformation + Translation(self.midpoint)
        # nets.transform(T)

        return nets 


class ARef(__RefElement__):
    pass






