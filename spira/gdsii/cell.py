import gdspy
import numpy as np
import networkx as nx
from copy import copy, deepcopy

from spira import param


from spira.core.lists import ElementList
from spira.lne import *
from spira.gdsii import *

from spira.core.initializer import CellInitializer
from spira.core.mixin.property import CellMixin
from spira.core.mixin.gdsii_output import OutputMixin
from spira.gdsii.elemental.port import __Port__
from spira.core.mixin.transform import TranformationMixin
from spira.rdd import get_rule_deck


RDD = get_rule_deck()


class __Cell__(gdspy.Cell, CellInitializer):

    __name_generator__ = RDD.ADMIN.NAME_GENERATOR
    __mixins__ = [OutputMixin, CellMixin, TranformationMixin]

    name = param.DataField(fdef_name='create_name')

    def __add__(self, other):
        if other is None:
            return self
        if issubclass(type(other), __Port__):
            self.ports += other
        else:
            self.elementals += other
        return self


class CellAbstract(__Cell__):

    ports = param.ElementalListField(fdef_name='create_ports')
    elementals = param.ElementalListField(fdef_name='create_elementals')

    def create_elementals(self, elems):
        return elems

    def create_ports(self, ports):
        return ports

    def create_name(self):
        if not hasattr(self, '__name__'):
            self.__name__ = self.__name_generator__(self)
        return self.__name__

    def flatten(self):
        self.elementals = self.elementals.flatten()
        return self.elementals

    def flat_copy(self, level=-1):
        self.elementals = self.elementals.flat_copy(level)
        return self.elementals

    def dependencies(self):
        deps = self.elementals.dependencies()
        # if hasattr(self, 'routes'):
        #     deps += self.routes.dependencies()
        deps += self
        return deps

    def commit_to_gdspy(self):
        from demo.pdks.ply.base import ProcessLayer
        cell = gdspy.Cell(self.name, exclude_from_current=True)

        for e in self.elementals:
            if not isinstance(e, (SRef, ElementList, Graph, Mesh)):
                e.commit_to_gdspy(cell=cell)

        return cell

    def move(self, midpoint=(0,0), destination=None, axis=None):
        """
        Moves elements of the Device from the midpoint point to
        the destination. Both midpoint and destination can be 1x2
        array-like, Port, or a key corresponding to
        one of the Ports in this device
        """

        if destination is None:
            destination = midpoint
            midpoint = [0,0]

        if issubclass(type(midpoint), __Port__):
            o = midpoint.midpoint
        elif np.array(midpoint).size == 2:
            o = midpoint
        elif midpoint in self.ports:
            o = self.ports[midpoint].midpoint
        else:
            raise ValueError('[DeviceReference.move()] ``midpoint`` ' + \
                             'not array-like, a port, or port name')

        if issubclass(type(destination), __Port__):
            d = destination.midpoint
        elif np.array(destination).size == 2:
            d = destination
        elif destination in self.ports:
            d = self.ports[destination].midpoint
        else:
            raise ValueError('[DeviceReference.move()] ``destination`` ' + \
                             'not array-like, a port, or port name')

        if axis == 'x':
            d = (d[0], o[1])
        if axis == 'y':
            d = (o[0], d[1])

        dx, dy = np.array(d) - o

        from demo.pdks.ply.base import ProcessLayer
        for e in self.elementals:
            if issubclass(type(e), (LabelAbstract, PolygonAbstract)):
                e.translate(dx, dy)
            if issubclass(type(e), ProcessLayer):
                e.move(destination=d, midpoint=o)
            if isinstance(e, SRef):
                e.move(destination=d, midpoint=o)

        for p in self.ports:
            mc = np.array(p.midpoint) + np.array(d) - np.array(o)
            p.move(midpoint=p.midpoint, destination=mc)

        return self

    def reflect(self, p1=(0,0), p2=(1,0)):
        """ Reflects the cell around the line [p1, p2]. """
        for e in self.elementals:
            if not issubclass(type(e), LabelAbstract):
                e.reflect(p1, p2)
        for p in self.ports:
            p.midpoint = self.__reflect__(p.midpoint, p1, p2)
            phi = np.arctan2(p2[1]-p1[1], p2[0]-p1[0])*180 / np.pi
            p.orientation = 2*phi - p.orientation
        return self

    def rotate(self, angle=45, center=(0,0)):
        """ Rotates the cell with angle around a center. """
        from demo.pdks.ply.base import ProcessLayer
        if angle == 0:
            return self
        for e in self.elementals:
            if issubclass(type(e), PolygonAbstract):
                e.rotate(angle=angle, center=center)
            elif isinstance(e, SRef):
                e.rotate(angle, center)
            elif issubclass(type(e), ProcessLayer):
                e.rotate(angle, center)

        ports = self.ports
        self.ports = ElementList()
        for p in ports:
            if issubclass(type(p), __Port__):
                p.midpoint = self.__rotate__(p.midpoint, angle, center)
                p.orientation = np.mod(p.orientation + angle, 360)
                self.ports += p
        return self

    def get_ports(self, level=None):
        """ Returns copies of all the ports of the Device """
        port_list = [p._copy() for p in self.ports]
        if level is None or level > 0:
            for r in self.elementals.sref:
                if level is None:
                    new_level = None
                else:
                    new_level = level - 1

                ref_ports = r.ref.get_ports(level=new_level)

                tf = {
                    'midpoint': r.midpoint,
                    'rotation': r.rotation,
                    'magnification': r.magnification,
                    'reflection': r.reflection
                }

                ref_ports_transformed = []
                for rp in ref_ports:
                    new_port = rp._copy()
                    new_port = new_port.transform(tf)
                    ref_ports_transformed.append(new_port)
                port_list += ref_ports_transformed
        return port_list


class Cell(CellAbstract):
    """ A Cell encapsulates a set of elementals that
    describes the layout being generated. """

    def __init__(self, name=None, elementals=None, ports=None, nets=None, library=None, **kwargs):
        CellInitializer.__init__(self, **kwargs)
        gdspy.Cell.__init__(self, self.name, exclude_from_current=True)

        self.g = nx.Graph()
 
        if name is not None:
            s = '{}_{}'.format(name, self.__class__._ID)
            self.__dict__['__name__'] = s
            __Cell__.name.__set__(self, s)
            self.__class__._ID += 1

        if library is not None:
            self.library = library
        if elementals is not None:
            self.elementals = elementals
        if ports is not None:
            self.ports = ports
        # FIXME!
        if nets is not None:
            self.nets = nets

    def __repr__(self):
        if hasattr(self, 'elementals'):
            elems = self.elementals
            return ("[SPiRA: Cell(\'{}\')] " +
                    "({} elementals: {} sref, {} cells, {} polygons, " +
                    "{} labels, {} ports)").format(
                        self.name,
                        elems.__len__(),
                        elems.sref.__len__(),
                        elems.cells.__len__(),
                        elems.polygons.__len__(),
                        elems.labels.__len__(),
                        self.ports.__len__()
                    )
        else:
            return "[SPiRA: Cell(\'{}\')]".format(self.__class__.__name__)

    # FIXME: Has to be placed here for deepcopy().
    def __str__(self):
        return self.__repr__()

    def _copy(self):
        cell = Cell(
            name=self.name,
            elementals=deepcopy(self.elementals),
            ports=deepcopy(self.ports),
            nets=self.nets
        )
        return cell











