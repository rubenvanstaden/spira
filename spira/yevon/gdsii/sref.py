import gdspy
import numpy
import inspect
import numpy as np
import spira.all as spira

from spira.yevon.geometry.ports.base import __Port__
from spira.yevon.gdsii.base import __Element__
from spira.yevon.geometry.coord import CoordParameter, Coord
from spira.yevon import utils
from spira.core.transforms import *
from spira.core.parameters.descriptor import ParameterDescriptor, FunctionParameter, Parameter

from spira.core.parameters.variables import *
from spira.yevon.geometry.vector import *
from spira.yevon.geometry.line import *
from copy import copy, deepcopy
from spira.core.transforms import stretching


class __RefElement__(__Element__):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def flatten(self):
        return self.ref.flatten()

    def flat_copy(self, level=-1):
        if level == 0: return spira.ElementList(self._copy__())
        el = self.ref.elements.flat_copy(level-1)
        T = self.transformation + Translation(self.midpoint)
        el.transform(T)
        return el


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
    alias = StringParameter(allow_none=True, default=None)

    def __init__(self, reference, alias=None, **kwargs):
        __RefElement__.__init__(self, alias=alias, **kwargs)
        self.ref = reference

    def __repr__(self):
        name = self.ref.name
        ps = "[SPiRA: SRef] (\"{}\", alias {}, midpoint {}, transforms {})"
        return (ps.format(name, self.alias, self.midpoint, self.transformation))

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return hash(self.__repr__())

    def __deepcopy__(self, memo):
        return SRef(
        # return self.__class__(
            alias=self.alias,
            reference=deepcopy(self.ref),
            midpoint=deepcopy(self.midpoint),
            transformation=deepcopy(self.transformation)
        )

    def __eq__(self, other):
        if not isinstance(other, SRef):
            return False
        return (
            (self.ref == other.ref) and
            (self.midpoint == other.position) and
            (self.transformation == other.transformation)
        )

    @property
    def bbox_info(self):
        T = self.transformation + Translation(self.midpoint)
        return self.ref.bbox_info.transform(T)

    def id_string(self):
        return self.__repr__()

    def dependencies(self):
        from spira.yevon.gdsii.cell_list import CellList
        d = CellList()
        d.add(self.ref)
        d.add(self.ref.dependencies())
        return d

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

        if (ignore_process is False) and (port.process != destination.process):
            raise ValueError('Cannot connect ports from different processes.')

        T = vector_match_transform(v1=p, v2=destination)
        self.transform(T)

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

        T = spira.Translation(translation=(dx, dy))
        self.transform(T)

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

    def port_alignment(self, ports, p1, p2):
        """
        Align `ports[0]` of reference with `p1` and 
        `ports[1]` of reference with external port `p2`.

        Example
        -------
        >>> 
        """
        d0 = deepcopy(p1)
        self.connect(ports[0], d0)
        if isinstance(ports[1], str):
            pin1 = self.ports[ports[1]]
        elif issubclass(type(ports[1]), __Port__):
            pin1 = ports[1].transform(self.transformation)
        if ports[0].orientation in (0, 180):
            T = vector_match_axis(v1=ports[1], v2=p2, axis='x')
        elif ports[0].orientation in (90, 270):
            T = vector_match_axis(v1=ports[1], v2=p2, axis='y')
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
        for i, e in enumerate(S.ref.elements):
            S.ref.elements[i].transform(T)
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
    
        for i, e in enumerate(D.ref.elements.polygons):
            if e.id_string() == port.local_pid:
                opposite_port = bbox_info_opposite_boundary_port(e, port)
                T = stretching.stretch_element_by_port(self, opposite_port, port, destination)
                T.apply(D.ref.elements[i])

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
        from spira.yevon.geometry.bbox_info import bbox_info_opposite_boundary_port
        D = self.expand_flat_copy()

        print(D.ports)

        port = D.ports[port_name]
        destination = D.ports[destination_name]
    
        for i, e in enumerate(D.ref.elements.polygons):
            if e.id_string() == port.local_pid:
                opposite_port = bbox_info_opposite_boundary_port(e, port)
                T = stretching.stretch_element_by_port(self, opposite_port, port, destination)
                T.apply(D.ref.elements[i])




    # # FIXME: Choose which one to use: expand of flat_copy?
    # def stretch(self, factor=(1,1), center=(0,0)):
    #     S = self.expand_flat_copy()
    #     T = spira.Stretch(stretch_factor=factor, stretch_center=center)
    #     for i, e in enumerate(S.ref.elements):
    #         # T.apply(S.ref.elements[i])
    #         S.ref.elements[i].transform(T)
    #     return self
    #     # return S
        
    # # def stretch(self, factor=(1,1), center=(0,0)):
    # #     el = self.flat_copy()
    # #     T = spira.Stretch(stretch_factor=factor, stretch_center=center)
    # #     for i, e in enumerate(el):
    # #         el[i].transform(T)
    # #     self.ref.elements = el
    # #     return self



    # def stretch_p2p(self, port_name, destination_name):
        # for i, e in enumerate(self.ref.elements):
        #     if isinstance(e, Polygon):
        #         if e.id_string() == port.local_pid:
        #             opposite_port = bbox_info.bbox_info_opposite_boundary_port(e, port)
        #             Tn = stretching.stretch_element_by_port(self, opposite_port, port, destination)
        #             Tn.apply(self.ref.elements[i])

        # if port.bbox is True:
        #     for i, e in enumerate(self.ref.elements):
        #         T.apply(self.ref.elements[i])
        # else:
        #     for i, e in enumerate(self.ref.elements):
        #         if isinstance(e, Polygon):
        #             if e.id_string() == port.local_pid:
        #                 opposite_port = bbox_info.bbox_info_opposite_boundary_port(e, port)
        #                 Tn = stretching.stretch_element_by_port(self, opposite_port, port, destination)
        #                 Tn.apply(self.ref.elements[i])
        # return self

    def nets(self, lcar):
        """  """

        from spira.yevon.geometry.nets.net_list import NetList
        nets = NetList()
        nets += self.ref.netlist

        # from spira.yevon.gdsii.pcell import Device
        # if isinstance(self.ref, Device):
        #     nets = [self.ref.netlist]
        # else:
        #     nets = self.ref.nets(lcar)

        # nets = self.ref.nets(lcar, contacts)

        # FIXME: Is this transformation required?
        # T = self.transformation + Translation(self.midpoint)
        # nets.transform(T)

        return nets 

    # def expand_transform(self):
    #     """

    #     Note
    #     ----
    #     Use __class__ cause we want to keep the 
    #     subclass tree (spira.Device) in tacks for fitlering.
    #     """

    #     if not self.transformation.is_identity():

    #         if self.alias is None:
    #             name = '{}_{}'.format(self.ref.name, self.transformation.id_string()),
    #         else:
    #             name = '{}_{}'.format(self.ref.name, self.alias),

    #         C = self.ref.__class__(name=name,
    #             alias=self.ref.alias + self.alias,
    #             elements=deepcopy(self.ref.elements),
    #             ports=deepcopy(self.ref.ports))

    #         T = self.transformation + spira.Translation(self.midpoint)
    #         C = C.transform(T)
    #         C.expand_transform()

    #         self.ref = C
    #         self.transformation = None
    #         self.midpoint = (0,0)

    #     return self

    def expand_transform(self):
        """

        Note
        ----
        Use __class__ cause we want to keep the 
        subclass tree (spira.Device) in tacks for fitlering.
        """

        if self.alias is None:
            name = '{}_{}'.format(self.ref.name, self.transformation.id_string()),
        else:
            name = '{}_{}'.format(self.ref.name, self.alias),

        C = self.ref.__class__(name=name,
            elements=deepcopy(self.ref.elements),
            ports=deepcopy(self.ref.ports))

        T = self.transformation + spira.Translation(self.midpoint)
        C = C.transform(T)
        C.expand_transform()

        self.ref = C
        self.transformation = None
        self.midpoint = (0,0)

        return self

    def expand_flat_copy(self):
        """  """
        D = self.ref.expand_flat_copy()
        return SRef(reference=D)
        # return self.__class__(reference=D)

    # def expand_flat_copy(self):
    #     """  """

    #     S = self.expand_transform()
    #     C = spira.Cell(name=S.ref.name + '_ExpandedCell')
    #     def flat_polygons(subj, cell):
    #         for e in cell.elements:
    #             if isinstance(e, spira.Polygon):
    #                 subj += e
    #             elif isinstance(e, spira.SRef):
    #                 flat_polygons(subj=subj, cell=e.ref)
    #         # for p in cell.ports:
    #         #     port = spira.Port(
    #         #         # name=p.name + "_" + cell.name,
    #         #         name=p.name,
    #         #         locked=False,
    #         #         midpoint=deepcopy(p.midpoint),
    #         #         orientation=deepcopy(p.orientation),
    #         #         width=deepcopy(p.width),
    #         #         local_pid=p.local_pid
    #         #     )
    #         #     subj.ports += port
    #         return subj
    #     D = flat_polygons(C, S.ref)
    #     # return SRef(reference=D, alias=self.alias)
    #     return self.__class__(reference=D, alias=self.alias)


class ARef(__RefElement__):
    pass






