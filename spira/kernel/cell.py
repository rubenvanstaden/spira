from spira.kernel.parameters.initializer import FieldInitializer
from spira.kernel.mixin.gdsii_output import OutputMixin
# from spira.kernel.mixins import TranformationMixin
import spira.kernel.parameters as param
from spira.kernel import utils
from numpy.linalg import norm

from spira.kernel.parameters.field.element_list import ElementList

from spira.kernel.elemental.polygons import PolygonAbstract
from spira.kernel.elemental.polygons import Polygons
from spira.kernel.elemental.label import LabelAbstract
from spira.lne.geometry import Geometry
from spira.lne.graph import Graph
from spira.lne.mesh import Mesh
from spira.lne.graph import GraphAbstract
from spira.lne.mesh import MeshAbstract
from spira.kernel.elemental.port import PortAbstract
from spira.kernel.elemental.port import Port
from spira.kernel.elemental.sref import SRef
from copy import copy, deepcopy

import gdspy
import inspect
import numpy as np
from spira.kernel.parameters.initializer import MetaBase
from spira.kernel.parameters.initializer import BaseCell
from spira.rdd import get_rule_deck


# ----------------------------------------------------------------------------------------------

# http://tobyho.com/2009/01/18/auto-mixin-in-python/
# http://code.activestate.com/recipes/577730-mixin-and-overlay/
# https://stackoverflow.com/questions/6966772/using-the-call-
# method-of-a-metaclass-instead-of-new

# ----------------------------------------------------------------------------------------------


RDD = get_rule_deck()


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

    def ls(self):
        print('\n------------------------')
        for i, e in enumerate(self.elementals.sref):
            print('{}. {}'.format(i, e.ref))

    def get_mlayers(self, layer):
        from spira.lpe.layers import MLayer
        from spira.kernel.elemental.polygons import Polygons
        elems = ElementList()
        for S in self.elementals.sref:
            if isinstance(S.ref, MLayer):
                if S.ref.layer.number == layer:
                    for p in S.ref.elementals:
                        # FIXME!!!
                        # if isinstance(p, ELayers):
                            # raise Errors
                        if isinstance(p, Polygons):
                            elems += p
        return elems


    @property
    def bbox(self):
        bbox = self.get_bounding_box()
        if bbox is None:  bbox = ((0,0),(0,0))
        return np.array(bbox)

    @property
    def cell(self):
        cell = Cell(name=self.name)
        for elem in self.elementals:
            cell += elem
        return cell

    @property
    def polygon_points(self):
        return self.get_polygons()

    @property
    def ports(self):
        return self.elementals.ports

    @property
    def graph(self):
        return self.elementals.graph

    @property
    def subgraphs(self):
        return self.elementals.subgraphs

    @property
    def id(self):
        return self.__id__

    @id.setter
    def id(self, _id):
        self.__id__ = _id

    def metal_polygons(self):
        from spira.rdd import get_rule_deck
        RDD = get_rule_deck()

        elems = ElementList()

        for p in self.elementals.polygons:
            if p.gdslayer.number in RDD.METALS.layers:
                elems += p
        return elems


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
                        elems.ports.__len__()
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

    def __init__(self, name=None, elementals=None, library=None, **kwargs):
        super().__init__(name=None, elementals=None, **kwargs)

        gdspy.Cell.__init__(self, name, exclude_from_current=True)

        if library is not None:
            self.library = library

        if elementals is not None:
            self.elementals = elementals

    def create_elementals(self, elems):
        result = ElementList()
        return result

    def dependencies(self):
        deps = self.elementals.dependencies()
        deps += self
        return deps

    def commit_to_gdspy(self):
        cell = gdspy.Cell(self.name, exclude_from_current=True)
        for e in self.elementals:
            if not isinstance(e, (Cell, SRef, ElementList, Graph, Mesh)):
                e.commit_to_gdspy(cell=cell)
        return cell

    def wrapper(self, c, c2dmap):
        from spira.kernel.utils import scale_coord_down as scd
        from spira.kernel.utils import scale_polygon_up as spu
        elems = c.elementals.flat_elems()
        # elems = c.elementals
        for e in elems:
            G = c2dmap[c]
            if isinstance(e, SRef):
                G.add(gdspy.CellReference(ref_cell=c2dmap[e.ref],
                                        origin=scd(e.origin),
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

    @property
    def gdspycell(self):
        cd = gdspy.current_library.cell_dict
        if self.name not in cd.keys():
            self.to_gdspy

            cell = gdspy.Cell(self.name, exclude_from_current=True)
            cell.elements = self.elements
            cell.labels = self.labels
            return cell
        else:
            return cd[self.name]

    @property
    def to_gdspy(self):
        for e in self.elementals.flat_copy(commit_to_gdspy=None):
            if not isinstance(e, ElementList):
                e.commit_to_gdspy(cell=self)

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

        if issubclass(type(origin), PortAbstract):
            o = origin.midpoint
        elif np.array(origin).size == 2:
            o = origin
        elif origin in self.ports:
            o = self.ports[origin].midpoint
        else:
            raise ValueError('[DeviceReference.move()] ``origin`` ' + \
                             'not array-like, a port, or port name')

        if issubclass(type(destination), PortAbstract):
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
            if not issubclass(type(e), (LabelAbstract, PortAbstract)):
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
            if issubclass(type(p), PortAbstract):
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

    def add_none_duplicate(self, p1):
        if issubclass(type(p1), PolygonAbstract):
            dup = False
            for p2 in self.elementals.polygons:
                if p1 == p2:
                    dup = True
            if not dup:
                self += p1
        elif isinstance(p1, SRef):
            dup = False
            for p2 in self.elementals.sref:
                if p1.equal_geometry(p2):
                    dup = True
            if not dup:
                self += p1


class Cell(CellAbstract):
    pass


from spira.kernel.parameters.field.typed_list import TypedList
class CellList(TypedList):

    __item_type__ = Cell

    def is_empty(self):
        if (len(self._list) == 0): return True
        for e in self._list:
            if not e.is_empty(): return False
        return True

    def __getitem__(self, key):
        if isinstance(key, str):
            for i in self._list:
                if i.name == key: return i
            raise IndexError("Structure " + key + " cannot be found in StructureList.")
        else:
            return list.__getitem__(self._list, key)

    def __setitem__(self, key, value):
        if isinstance(key, str):
            for i in range(0, len(self._list)):
                if self._list[i].name == key: 
                    return list.__setitem__(self._list, i, value)
            list.append(self._list, value)
        else:
            return list.__setitem__(self._list, key, value)

    def __delitem__(self, key):
        if isinstance(key, str):
            for i in range(0, len(self._list)):
                if self._list[i].name == key: 
                    return list.__delitem__(self._list, i)
                return
            return list.__delitem__(self._list, key)
        else:
            return list.__delitem__(self._list, key)

    def __contains__(self, item):
        if isinstance(item, Cell):
            name = item.name
        else:
            name = item
        if isinstance(name, str):
            for i in self._list:
                if i.name == name: return True
            return False
        else:
            return list.__contains__(self._list, item)

    def __fast_contains__(self, name):
        for i in self._list:
            if i.name == name:
                return True
        return False

    def index(self, item):
        if isinstance(item, str):
            for i in range(0, len(self._list)):
                if list.__getitem__(self._list, i).name == item:
                    return i
            raise ValueError("Cell " + item + " is not in CellList")
        else:
            list.index(self._list, item)

    def add(self, item, overwrite=False):
        if item == None:
            return
        if isinstance(item, Cell):
            if overwrite:
                self._list[item.name] = item
                return
            elif not self.__fast_contains__(item.name):
                self._list.append(item)
        elif isinstance(item, (CellList, list, set)):
            for s in item:
                self.add(s, overwrite)
        else:
            raise ValueError('Cannot add cell!')

    def append(self, other, overwrite = False):
        return self.add(other, overwrite)

    def extend(self, other, overwrite = False):
        return self.add(other, overwrite)


from spira.kernel.parameters.descriptor import DataFieldDescriptor
def CellField(name=None, elementals=None, library=None):
    F = Cell(name=name, elementals=elementals, library=library)
    return DataFieldDescriptor(default=F)









