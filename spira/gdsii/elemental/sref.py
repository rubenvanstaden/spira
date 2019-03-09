import gdspy
import numpy
import inspect
import numpy as np
import spira
from copy import copy, deepcopy

from spira import param
from spira.gdsii.elemental.port import __Port__
from spira.gdsii.elemental.port import Port
from spira.core.initializer import ElementalInitializer
from spira.core.mixin.transform import TranformationMixin


class __SRef__(gdspy.CellReference, ElementalInitializer):

    __mixins__ = [TranformationMixin]

    def __deepcopy__(self, memo):
        return SRef(
            # structure=deepcopy(self.ref),
            structure=self.ref,
            port_locks=self.port_locks,
            midpoint=deepcopy(self.midpoint),
            rotation=self.rotation,
            magnification=self.magnification,
            node_id=deepcopy(self.node_id),
            reflection=self.reflection
        )

    def __eq__(self, other):
        return self.__str__() == other.__str__()

    def __move_net__(self, g):
        for n in g.nodes():
            p = np.array(g.node[n]['pos'])
            m = np.array(self.midpoint)
            g.node[n]['pos'] = p + m
        return g

    def __equal_ports__(self, p1, p2):
        if p1.encloses_midpoint(p2.edge.points[0]):
            if p1.gdslayer.number == p2.gdslayer.number:
                return True
        return False

    @property
    def tf(self):
        tf = {
            'midpoint': self.midpoint,
            'rotation': self.rotation,
            'magnification': self.magnification,
            'reflection': self.reflection
        }
        return tf


class SRefAbstract(__SRef__):

    midpoint = param.MidPointField()
    rotation = param.FloatField(default=None)
    reflection = param.BoolField(default=False)
    magnification = param.FloatField(default=1)

    def dependencies(self):
        from spira.gdsii.lists.cell_list import CellList
        d = CellList()
        d.add(self.ref)
        d.add(self.ref.dependencies())
        return d

    def flatten(self):
        return self.ref.flatten()

    def flat_copy(self, level=-1, commit_to_gdspy=False):
        """  """
        if level == 0:
            el = spira.ElementList()
            el += self
            return el
        transform = {
            'midpoint': self.midpoint,
            'rotation': self.rotation,
            'magnification': self.magnification,
            'reflection': self.reflection
        }
        el = self.ref.elementals.flat_copy(level-1)
        el.transform(transform)
        return el

    @property
    def polygons(self):
        # FIXME: Assums all elementals are ply.Polygon.
        elems = spira.ElementList()
        tf = {
            'midpoint': self.midpoint,
            'rotation': self.rotation,
            'magnification': self.magnification,
            'reflection': self.reflection
        }
        for p in self.ref.elementals:
            new_p = deepcopy(p)
            elems += new_p.transform(tf)
        return elems

    @property
    def netlist(self):
        g = self.ref.netlist
        for n in g.nodes():
            if 'device' not in g.node[n]:
                pc_ply = g.nodes[n]['surface']
                for p in pc_ply.edge_ports:
                    p1 = p.transform(self.tf)
                    for key, p2 in self.instance_ports.items():
                        if self.__equal_ports__(p1, p2):
                            if p2.locked is False:
                                g.node[n]['device'] = pc_ply
                                eid = self.port_connects[key]
                                if 'connect' in g.node[n]:
                                    g.node[n]['connect'].append(eid)
                                else:
                                    g.node[n]['connect'] = [eid]
        return self.__move_net__(g)
    
    @property
    def instance_ports(self):
        """ This property allows you to access
        my_device_reference.ports, and receive a
        copy of the ports dict which is correctly
        rotated and translated. """
        for port in self._parent_ports:

            key = list(port.key)
            key[2] += self.midpoint[0]
            key[3] += self.midpoint[1]
            key = tuple(key)

            new_port = deepcopy(port)
            self.iports[key] = new_port.transform(self.tf)

            if key in self.port_locks.keys():
                self.iports[key].locked = self.port_locks[key]
            if key in self.port_connects.keys():
                self.iports[key].connections.append(self.port_connects[key])

        return self.iports

    @property
    def ports(self):
        """ This property allows you to access
        my_device_reference.ports, and receive a
        copy of the ports dict which is correctly
        rotated and translated. """
        for port in self._parent_ports:
            new_port = deepcopy(port)
            self._local_ports[port.name] = new_port.transform(self.tf)
        return self._local_ports

    def move(self, midpoint=(0,0), destination=None, axis=None):
        d, o = super().move(midpoint=midpoint, destination=destination, axis=axis)
        dxdy = np.array(d) - np.array(o)
        self.midpoint = np.array(self.midpoint) + dxdy
        return self

    def translate(self, dx=0, dy=0):
        """ Translate port by dx and dy. """
        self.origin = self.midpoint
        super().translate(dx=dx, dy=dy)
        self.midpoint = self.origin
        return self

    def rotate(self, angle=45, center=(0,0)):
        if angle == 0:
            return self
        if self.rotation is None:
            self.rotation = 0
        if issubclass(type(center), __Port__):
            center = center.midpoint
        self.rotation += angle
        self.midpoint = self.__rotate__(self.midpoint, angle, center)
        return self

    def reflect(self, p1=(0,0), p2=(1,0)):
        if issubclass(type(p1), __Port__):
            p1 = p1.midpoint
        if issubclass(type(p2), __Port__):
            p2 = p2.midpoint
        if self.rotation is None:
            self.rotation = 0
        p1 = np.array(p1)
        p2 = np.array(p2)

        # Translate so reflection axis passes through midpoint
        self.midpoint = self.midpoint - p1

        # Rotate so reflection axis aligns with x-axis
        angle = np.arctan2((p2[1]-p1[1]), (p2[0]-p1[0]))*180 / np.pi
        self.midpoint = self.__rotate__(self.midpoint, angle=-angle, center=[0,0])
        self.rotation -= angle

        # Reflect across x-axis
        self.reflection = not self.reflection
        self.midpoint = [self.midpoint[0], -self.midpoint[1]]
        self.rotation = -self.rotation

        # Un-rotate and un-translate
        self.midpoint = self.__rotate__(self.midpoint, angle=angle, center=[0,0])
        self.rotation += angle
        self.midpoint = self.midpoint + p1

        return self

    def connect(self, port, destination, overlap=0):
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

    def align(p1, p2, distance):
        pass
        # # TODO:Get port direction and distance
        # self.connect(port=p1, destination=p2)
        # self.move(midpoint=p2, destination=d)

    def stretch(self, port, center=[0,0], vector=[1,1]):
        """  """
        from spira.lgm.shape.stretch import Stretch
        self.stretching[port] = Stretch(center=center, vector=vector)
        return self


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

    iports = param.DictField(default={})
    port_locks = param.DictField(default={})
    port_connects = param.DictField(default={})

    def __init__(self, structure, **kwargs):
        ElementalInitializer.__init__(self, **kwargs)
        self.ref = structure
        self._parent_ports = []
        for p in structure.ports:
            self._parent_ports.append(p)
        for t in structure.terms:
            self._parent_ports.append(t)
        self._local_ports = {}
        # self._local_ports = {port.node_id:deepcopy(port) for port in self._parent_ports}
        # self._local_ports = {port.name:deepcopy(port) for port in self._parent_ports}

    def __repr__(self):
        name = self.ref.name
        return ("[SPiRA: SRef] (\"{}\", at {}, srefs {}, cells {}, " +
           "polygons {}, ports {}, labels {})").format(
            name, self.midpoint,
            len(self.ref.elementals.sref),
            len(self.ref.elementals.cells),
            len(self.ref.elementals.polygons),
            len(self.ref.ports),
            len(self.ref.elementals.labels)
        )

    def __str__(self):
        return self.__repr__()









