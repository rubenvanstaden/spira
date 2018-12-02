import gdspy
import numpy
import inspect
import numpy as np
import spira
from copy import deepcopy

from spira.kernel.parameters.initializer import BaseSRef
from spira.kernel.elemental.port import PortAbstract
from spira.kernel.elemental.port import Port
from spira.kernel.elemental.polygons import PolygonAbstract
from spira.kernel.elemental.polygons import Polygons
import spira.kernel.parameters as param
from spira.kernel.mixins import TranformationMixin


class InspectMixin(object):

    def rm(self, cellname):
        print('\n - removed cell: \'{}\''.format(cellname))
        elems = self.elementals
        self.elementals = ElementList()
        for e in elems:
            if isinstance(e, SRef):
                if cellname != e.ref.name:
                    self.elementals += e
            else:
                self.elementals += e

    def ls_ports(self):
        print('\n------------------------')
        for name, port in self._local_ports.items():
            print('{} : {}'.format(name, port))


class __SRef__(gdspy.CellReference, BaseSRef):

    __mixins__ = [TranformationMixin]

    def __init__(self, structure, **kwargs):

        BaseSRef.__init__(self, **kwargs)

        self.ref = structure
        self._parent_ports = structure.ports
        self._local_ports = {port.name:port._copy() for port in structure.ports}

    def __repr__(self):
        name = self.ref.name
        return ("[SPiRA: SRef] (\"{}\", at {}, srefs {}, " +
               "polygons {}, ports {}, labels {})").format(
                name, self.origin,
                len(self.ref.elementals.sref),
                len(self.ref.elementals.polygons),
                len(self.ref.elementals.ports),
                len(self.ref.elementals.labels))

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return self.__str__() == other.__str__()

    # FIXME: Improve this algorithm.
    def equal_geometry(self, other):
        if self.origin != other.origin:
            return False

        for pi in self.ref.elementals.polygons:
            for pj in other.ref.elementals.polygons:
                if abs(pi.ply_area - pj.ply_area) > 1e-9:
                    return False
        return True

    def __getitem__(self, val):
        """
        This allows you to access an alias from the
        reference's parent, and receive a copy of the
        reference which is correctly rotated and translated.
        """
        try:
            alias_device = self.ref[val]
        except:
            raise ValueError('[PHIDL] Tried to access alias "%s" from parent '
                'Device "%s", which does not exist' % (val, self.ref.name))

        assert isinstance(alias_device, SRef)

        new_reference = SRef(alias_device.ref,
                            origin=alias_device.origin,
                            rotation=alias_device.rotation,
                            magnification=alias_device.magnification,
                            x_reflection=alias_device.x_reflection)

        if self.x_reflection:
            new_reference.reflect((1,0))
        if self.rotation is not None:
            new_reference.rotate(self.rotation)
        if self.origin is not None:
            new_reference.move(self.origin)

        return new_reference

    def __deepcopy__(self, memo):
        return SRef(structure=deepcopy(self.ref),
                    origin=self.origin,
                    rotation=self.rotation,
                    magnification=self.magnification,
                    x_reflection=self.x_reflection)


class SRefAbstract(__SRef__):
    """

    """

    __mixins__ = [InspectMixin]

    origin = param.PointField()
    rotation = param.FloatField()
    magnification = param.FloatField(default=None)
    x_reflection = param.BoolField(default=None)

    def __init__(self, structure, stretching={}, **kwargs):
        self.stretching = stretching
        super().__init__(structure, **kwargs)

    def dependencies(self):
        # d = spira.ElementList()
        from spira.kernel.cell import CellList
        d = CellList()
        d.add(self.ref)
        d.add(self.ref.dependencies())
        return d

    def _copy(self, level=0):
        S = SRef(structure=self.ref, origin=self.origin, 
                 rotation=self.rotation, magnification=self.magnification, 
                 x_reflection=self.x_reflection)
        return S

    def flat_copy(self, level=-1, commit_to_gdspy=False):

        if level == 0:
            el = spira.ElementList()
            el += self
            return el

        transform = {
            'origin': self.origin,
            'rotation': self.rotation,
            'magnification': self.magnification,
            'x_reflection': self.x_reflection
        }

        el = self.ref.elementals.flat_copy(level-1)
        if self.stretching:
            el.stretch(self.stretching)
        el.transform(transform)
        return el

    def transform(self, transform):
        if transform['x_reflection']:
            self.reflect(p1=[0,0], p2=[1,0])
            self.rotate(angle=transform['rotation'])
            self.translate(dx=transform['origin'][0], dy=transform['origin'][1])
        else:
            self.rotate(angle=transform['rotation'])
            # self.move(origin=self.origin, destination=transform['origin'])
            self.translate(dx=transform['origin'][0], dy=transform['origin'][1])
        return self

    def flatten(self):
        return self.ref.flatten()

    def scale_down(self):
        el = self.ref.elementals.scale_down()
        return el

    def commit_to_gdspy(self, cell):
        S = gdspy.CellReference(self.ref.gdspycell,
                                origin=self.origin,
                                rotation=self.rotation,
                                magnification=self.magnification,
                                x_reflection=self.x_reflection)
        cell.add(S)

    @property
    def ports(self):
        """
        This property allows you to access
        my_device_reference.ports, and receive a
        copy of the ports dict which is correctly
        rotated and translated
        """
        for port in self._parent_ports:

            tf = {
                'origin': self.origin,
                'rotation': self.rotation,
                'magnification': self.magnification,
                'x_reflection': self.x_reflection
            }

            key = port.name
            new_port = port._copy()
            self._local_ports[key] = new_port.transform(tf)
        return self._local_ports

    def move(self, origin=(0,0), destination=None, axis=None):
        """
        Moves the DeviceReference from the origin point to the destination.  Both
        origin and destination can be 1x2 array-like, Port, or a key
        corresponding to one of the Ports in this device_ref
        """

        if destination is None:
            destination = origin
            origin = (0,0)

        if issubclass(type(origin), PortAbstract):
            o = origin.midpoint
        elif np.array(origin).size == 2:
            o = origin
        elif origin in self.ports:
            o = self.ports[origin].midpoint
        else:
            raise ValueError("[DeviceReference.move()] ``origin`` " +
                             "not array-like, a port, or port name")

        if issubclass(type(destination), PortAbstract):
            d = destination.midpoint
        elif np.array(destination).size == 2:
            d = destination
        elif destination in self.ports:
            d = self.ports[destination].midpoint
        else:
            raise ValueError("[DeviceReference.move()] ``destination`` " +
                             "not array-like, a port, or port name")

        if axis == 'x':
            d = (d[0], o[1])
        if axis == 'y':
            d = (o[0], d[1])

        dxdy = np.array(d) - np.array(o)
        self.origin = np.array(self.origin) + dxdy
        return self

    def rotate(self, angle=45, center=(0,0)):
        if angle == 0:
            return self

        if issubclass(type(center), PortAbstract):
            center = center.midpoint

        self.rotation += angle
        self.origin = self._rotate_points(self.origin, angle, center)

        return self

    def reflect(self, p1=(0,1), p2=(0,0)):
        if issubclass(type(p1), PortAbstract):
            p1 = p1.midpoint
        if issubclass(type(p2), PortAbstract):
            p2 = p2.midpoint

        p1 = np.array(p1)
        p2 = np.array(p2)

        # Translate so reflection axis passes through origin
        self.origin = self.origin - p1

        # Rotate so reflection axis aligns with x-axis
        angle = np.arctan2((p2[1]-p1[1]), (p2[0]-p1[0]))*180 / np.pi
        self.origin = self._rotate_points(self.origin, angle=-angle, center=[0,0])
        self.rotation -= angle

        # Reflect across x-axis
        self.x_reflection = not self.x_reflection
        self.origin = [self.origin[0], -self.origin[1]]
        self.rotation = -self.rotation

        # Un-rotate and un-translate
        self.origin = self._rotate_points(self.origin, angle=angle, center=[0,0])
        self.rotation += angle
        self.origin = self.origin + p1

        return self

    def connect(self, port, destination, overlap=0):
        if port in self.ports.keys():
            p = self.ports[port]
        elif issubclass(type(port), PortAbstract):
            p = port
        else:
            raise ValueError("[SPiRA] connect() did not receive a Port or " +
                             "valid port name - received ({}), ports available " +
                             "are ({})").format(port, self.ports.keys())

        angle = 180 + destination.orientation - p.orientation
        self.rotate(angle=angle, center=p.midpoint)
        self.move(origin=p, destination=destination)

        return self

    def stretch(self, port, center=[0,0], vector=[1,1]):
        from spira.lgm.shape.stretch import Stretch
        self.stretching[port] = Stretch(center=center, vector=vector)
        return self


class SRef(SRefAbstract):
    pass
