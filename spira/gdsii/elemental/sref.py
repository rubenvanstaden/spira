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
            midpoint=alias_device.midpoint,
            rotation=alias_device.rotation,
            magnification=alias_device.magnification,
            reflection=alias_device.reflection
        )

        if self.reflection:
            new_reference.reflect((1,0))
        if self.rotation is not None:
            new_reference.rotate(self.rotation)
        if self.midpoint is not None:
            new_reference.move(self.midpoint)

        return new_reference

    def __deepcopy__(self, memo):
        return SRef(
            structure=deepcopy(self.ref),
            midpoint=deepcopy(self.midpoint),
            rotation=self.rotation,
            magnification=self.magnification,
            reflection=self.reflection
        )

    def __eq__(self, other):
        return self.__str__() == other.__str__()


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
    def ports(self):
        """
        This property allows you to access
        my_device_reference.ports, and receive a
        copy of the ports dict which is correctly
        rotated and translated
        """
        for port in self._parent_ports:

            tf = {
                'midpoint': self.midpoint,
                'rotation': self.rotation,
                'magnification': self.magnification,
                'reflection': self.reflection
            }

            new_port = port._copy()
            # new_port = copy(port)
            # new_port = deepcopy(port)
            self._local_ports[port.name] = new_port.transform(tf)
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

    def __init__(self, structure, **kwargs):

        ElementalInitializer.__init__(self, **kwargs)

        self.ref = structure
        self._parent_ports = spira.ElementList()

        for p in structure.ports:
            self._parent_ports += p
        for t in structure.terms:
            self._parent_ports += t
        # self._local_ports = {port.name:copy(port) for port in self._parent_ports}
        self._local_ports = {port.name:deepcopy(port) for port in self._parent_ports}

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

    # def get_node_id(self):
    #     if self.__id__:
    #         return self.__id__
    #     else:
    #         return '{}_{}'.format(self.ref.name, self.midpoint)









