from spira.core.initializer import FieldInitializer
from spira.core.mixin.gdsii_output import OutputMixin
from spira import param

from spira.core.lists import ElementList
from spira.lne import *
from spira.gdsii import *

import gdspy
import numpy as np
from copy import copy, deepcopy
from spira.core.initializer import MetaBase
from spira.core.initializer import BaseCell
from spira.rdd import get_rule_deck
from spira.core.mixin.inspect import InspectMixin
from spira.gdsii.elemental.port import __Port__


# ----------------------------------------------------------------------------------------------


RDD = get_rule_deck()


glib = gdspy.GdsLibrary(name='s2g')


class __Cell__(gdspy.Cell, BaseCell):

    _ID = 0

    __mixins__ = [OutputMixin, InspectMixin]

    name = param.StringField()

    def __init__(self, name=None, elementals=None, **kwargs):

        if name is not None:
            self.__dict__['__name__'] = name
            Cell.name.__set__(self, name)

        BaseCell.__init__(self, **kwargs)

        if 'id0' in kwargs.keys():
            self.__id__ = '_{}'.format(self.id0)
        else:
            self.__id__ = '_{}'.format(Cell._ID)
            Cell._ID += 1

    def __repr__(self):
        if hasattr(self, 'elementals'):
            elems = self.elementals
            return ("[SPiRA: Cell(\'{}\')] " +
                    "({} elementals: {} sref, {} polygons, " +
                    "{} labels, {} ports)").format(
                        self.name,
                        elems.__len__(),
                        elems.sref.__len__(),
                        elems.polygons.__len__(),
                        elems.labels.__len__(),
                        self.ports.__len__()
                    )
        else:
            return "[SPiRA: Cell(\'{}\')]".format(self.__class__.__name__)

    def __str__(self):
        return self.__repr__()

    def __getitem__(self, val):
        try:
            return self.elementals[val]
        except:
            raise ValueError('[SPiRA: Cell] No Device found in Cell.')

    def __sub__(self, other):
        self.elements = []
        elements = self.elementals
        self.elementals = ElementList()

        for e in elements:
            if isinstance(e, Polygons):
                p1 = e.polygons
                p2 = other.polygons

                polygons = bool_operation(subj=p1, clip=p2,
                                          method='difference')

                if polygons:
                    self += Polygons(polygons=polygons,
                                     gdslayer=e.gdslayer)

    def __add__(self, other):
        if other is None:
            return self
        if isinstance(other, Cell):
            raise ValueError('Use SRef to add to Cell')
        self.elementals += other
        return self

    def __contains__(self, elemental):
        return elemental in self.elementals


class CellAbstract(__Cell__):
    """
    Cell API class that wrapper around gdspy.Cell.

    Parameters
    ----------
    name : string
        Name of the cell.
    cell : gdspy.Cell
        Copies the elements and labels of an existing gdspy.Cell.
    elements: list
        List of gds elements.
    """

    id0 = param.StringField()
    color = param.ColorField(default='#F0B27A')

    elementals = param.ElementListField(fdef_name='create_elementals')
    # ports = param.PortListField(fdef_name='create_ports')
    ports = param.ElementListField(fdef_name='create_ports')

    def __init__(self, name=None, elementals=None, ports=None, library=None, **kwargs):
        super().__init__(name=None, elementals=None, **kwargs)

        gdspy.Cell.__init__(self, name, exclude_from_current=True)

        if library is not None:
            self.library = library

        if elementals is not None:
            self.elementals = elementals

        if ports is not None:
            self.ports = ports

    def create_elementals(self, elems):
        result = ElementList()
        return result

    def create_ports(self, ports):
        return ports

    @property
    def terms(self):
        from spira.gdsii.elemental.term import Term
        terms = ElementList()
        for p in self.ports:
            if isinstance(p, Term):
                terms += p
        return terms

    @property
    def term_ports(self):
        from spira.gdsii.elemental.term import Term
        terms = {}
        for p in self.ports:
            if isinstance(p, Term):
                terms[p.name] = p
        return terms

    def dependencies(self):
        deps = self.elementals.dependencies()
        deps += self
        return deps

    def commit_to_gdspy(self):
        cell = gdspy.Cell(self.name, exclude_from_current=True)
        for e in self.elementals:
            if not isinstance(e, (Cell, SRef, ElementList, Graph, Mesh)):
                e.commit_to_gdspy(cell=cell)
        for e in self.ports:
            e.commit_to_gdspy(cell=cell)
        return cell

    def wrapper(self, c, c2dmap):
        from spira.gdsii.utils import scale_coord_down as scd
        from spira.gdsii.utils import scale_polygon_up as spu
        elems = c.elementals.flat_elems()
        # elems = c.elementals
        for e in elems:
            G = c2dmap[c]
            if isinstance(e, SRef):
                G.add(gdspy.CellReference(ref_cell=c2dmap[e.ref],
                                          origin=e.origin,
                                        #   origin=scd(e.origin),
                                          rotation=e.rotation,
                                          magnification=e.magnification,
                                          x_reflection=e.x_reflection))
            # elif isinstance(e, Polygons):
            #     G.add(gdspy.PolygonSet(polygons=spu(e.polygons),
            #                            layer=e.gdslayer.number,
            #                            datatype=e.gdslayer.datatype))

    def construct_gdspy_tree(self):
        d = self.dependencies()
        c2dmap = {}
        for c in d:
            G = c.commit_to_gdspy()
            c2dmap.update({c:G})

        for c in d:
            self.wrapper(c, c2dmap)
            glib.add(c2dmap[c])

        gdspy.LayoutViewer(library=glib)

        return c2dmap[self]

    def get_purpose_layers(self, purpose_symbol):
        players = RDD.PLAYER.get_physical_layers(purposes=purpose_symbol)
        elems = ElementList()
        for ply in self.elementals.polygons:
            for phys in players:
                if ply.gdslayer == phys.layer:
                    elems += ply
        return elems

    def flat_copy(self, level=-1, commit_to_gdspy=False):
        self.elementals = self.elementals.flat_copy(level, commit_to_gdspy)
        return self.elementals

    def flatten(self):
        self.elementals = self.elementals.flatten()
        return self.elementals

    def remove_sref(self, sref):
        elems = ElementList()
        for e in self.elementals:
            if e is not sref:
                elems += e
        self.elementals = elems

    @property
    def references(self):
        return list(self.elementals.sref)

    def move(self, origin=(0,0), destination=None, axis=None):
        """
        Moves elements of the Device from the origin point to
        the destination. Both origin and destination can be 1x2
        array-like, Port, or a key corresponding to
        one of the Ports in this device
        """

        if destination is None:
            destination = origin
            origin = [0,0]

        if issubclass(type(origin), __Port__):
            o = origin.midpoint
        elif np.array(origin).size == 2:
            o = origin
        elif origin in self.ports:
            o = self.ports[origin].midpoint
        else:
            raise ValueError('[DeviceReference.move()] ``origin`` ' + \
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

        for e in self.elementals:
            if issubclass(type(e), (LabelAbstract, PolygonAbstract)):
                e.translate(dx, dy)
            if isinstance(e, (Cell, SRef)):
                e.move(destination=d, origin=o)

        for p in self.ports:
            p.midpoint = np.array(p.midpoint) + np.array(d) - np.array(o)

        return self

    def reflect(self, p1=(0,1), p2=(0,0)):
        for e in self.elementals:
            if not issubclass(type(e), (LabelAbstract, __Port__)):
                e.reflect(p1, p2)
        for p in self.ports:
            p.midpoint = self._reflect_points(p.midpoint, p1, p2)
            phi = np.arctan2(p2[1]-p1[1], p2[0]-p1[0])*180 / np.pi
            p.orientation = 2*phi - p.orientation
        return self

    def rotate(self, angle=45, center=(0,0)):
        if angle == 0:
            return self

        for e in self.elementals:
            if issubclass(type(e), PolygonAbstract):
                e.rotate(angle=angle, center=center)
            elif isinstance(e, SRef):
                e.rotate(angle, center)

        elements = self.elementals
        self.elementals = ElementList()
        for p in elements:
            if issubclass(type(p), __Port__):
                p.midpoint = self._rotate_points(p.midpoint, angle, center)
                p.orientation = np.mod(p.orientation + angle, 360)
                self.elementals += p
            else:
                self.elementals += p

        return self

    def get_plys(self, level=None):
        """ Returns copies of all the ports of the Device """

        port_list = [deepcopy(S) for S in self.elementals.polygons]

        if level is None or level > 0:
            for r in self.references:
                if level is None:
                    new_level = None
                else:
                    new_level = level - 1

                ref_ports = r.ref.get_plys(level=new_level)

                tf = {
                    'origin': r.origin,
                    'rotation': r.rotation,
                    'magnification': r.magnification,
                    'x_reflection': r.x_reflection
                }

                ref_ports_transformed = []
                for rp in ref_ports:
                    new_port = deepcopy(rp)
                    new_port = new_port.transform(tf)
                    ref_ports_transformed.append(new_port)

                port_list += ref_ports_transformed

        return port_list

    def get_srefs(self, level=None):
        """ Returns copies of all the ports of the Device """

        port_list = [deepcopy(S) for S in self.elementals.sref]

        if level is None or level > 0:
            for r in self.references:
                if level is None:
                    new_level = None
                else:
                    new_level = level - 1

                ref_ports = r.ref.get_srefs(level=new_level)

                tf = {
                    'origin': r.origin,
                    'rotation': r.rotation,
                    'magnification': r.magnification,
                    'x_reflection': r.x_reflection
                }

                ref_ports_transformed = []
                for rp in ref_ports:
                    # new_port = deepcopy(rp)
                    new_port = rp._copy()
                    new_port = new_port.transform(tf)
                    ref_ports_transformed.append(new_port)

                port_list += ref_ports_transformed

        return port_list

    def get_ports(self, level=None):
        """ Returns copies of all the ports of the Device """

        port_list = [p._copy() for p in self.ports]

        if level is None or level > 0:
            for r in self.references:
                if level is None:
                    new_level = None
                else:
                    new_level = level - 1

                ref_ports = r.ref.get_ports(level=new_level)

                tf = {
                    'origin': r.origin,
                    'rotation': r.rotation,
                    'magnification': r.magnification,
                    'x_reflection': r.x_reflection
                }

                ref_ports_transformed = []
                for rp in ref_ports:
                    new_port = rp._copy()
                    # if new_port.name in r.stretching.keys():
                    #     new_port.stretch(r.stretching[new_port.name])
                    new_port = new_port.transform(tf)
                    ref_ports_transformed.append(new_port)
                port_list += ref_ports_transformed

        return port_list


class Cell(CellAbstract):
    pass










