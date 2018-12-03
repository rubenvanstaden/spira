import collections
from spira.kernel.parameters.field.typed_list import TypedList


class PortList(TypedList):
    """

    """

    def __repr__(self):
        if len(self._list) == 0: print('PortList is empty')
        return '\n'.join('{}'.format(k) for k in enumerate(self._list))

    def __str__(self):
        return self.__repr__()

    def __getitem__(self, i):
        from spira.kernel.elemental.sref import SRef
        from spira.kernel.cell import Cell
        from spira.kernel.elemental.polygons import Polygons

        if isinstance(i, str):
            for port in self._list:
                if port.name == i:
                    return port._copy()
        else:
            return self._list[i]


class ElementFilterMixin(object):

    def add_elem_to_cell(self, elem, cellname):
        for sref in self.sref:
            if sref.ref.name == cellname:
                self += elem

    def get_polygons(self, layer=None, datatype=None):
        elems = ElementList()
        for ply in self.polygons:
            if layer is not None:
                if ply.gdslayer.number == layer:
                    elems += ply
            if datatype is not None:
                if ply.gdslyaer.datatype == datatype:
                    elems += ply
        return elems

    @property
    def ports(self):
        from spira.kernel.elemental.port import PortAbstract
        elems = PortList()
        for e in self._list:
            if issubclass(type(e), PortAbstract):
                elems += e
        return elems

    @property
    def polygons(self):
        from spira.kernel.elemental.polygons import PolygonAbstract
        from spira.kernel.elemental.path import Path
        elems = ElementList()
        for e in self._list:
            if issubclass(type(e), PolygonAbstract):
                elems += e
            elif isinstance(e, Path):
                elems += e.polygon
        return elems

    @property
    def metals(self):
        from spira.rdd import get_rule_deck
        from spira.kernel.elemental.polygons import PolygonAbstract
        RDD = get_rule_deck()
        elems = ElementList()
        for p in self.polygons:
            if p.gdslayer.number in RDD.METALS.layers:
                elems += p
        return elems

    @property
    def mlayers(self):
        from spira.lpe.primitives import MLayer
        elems = ElementList()
        for S in self._list:
            if isinstance(S.ref, MLayer):
                elems += S
        return elems

    @property
    def dlayers(self):
        from spira.lpe.primitives import NLayer
        elems = ElementList()
        for S in self._list:
            if isinstance(S.ref, NLayer):
                elems += S
        return elems

    def get_dlayer(self, layer):
        elems = ElementList()
        for S in self.dlayers:
            for p in S.ref.elementals.polygons:
                if isinstance(layer, int):
                    if p.gdslayer.number == layer:
                        elems += S
                else:
                    if p.gdslayer.number == layer.number:
                        elems += S
        return elems

    def get_mlayer(self, layer):
        elems = ElementList()
        for S in self.mlayers:
            for p in S.ref.elementals.polygons:
                if isinstance(layer, int):
                    if p.gdslayer.number == layer:
                        elems += S
                else:
                    if p.gdslayer.number == layer.number:
                        elems += S
        return elems

    @property
    def labels(self):
        from spira.kernel.elemental.label import Label
        elems = ElementList()
        for e in self._list:
            if isinstance(e, Label):
                elems += e
        return elems

    @property
    def sref(self):
        from spira.kernel.elemental.sref import SRef
        elems = ElementList()
        for e in self._list:
            if isinstance(e, SRef):
                elems += e
        return elems

    @property
    def mesh(self):
        from spira.lne.mesh import Mesh
        for g in self._list:
            if isinstance(g, Mesh):
                return g
        raise ValueError('No graph was generate for Cell')

    @property
    def graph(self):
        from spira.lne.mesh import MeshAbstract
        for e in self._list:
            if issubclass(type(e), MeshAbstract):
                return e.g
        return None

    @property
    def subgraphs(self):
        subgraphs = {}
        for e in self.sref:
            cell = e.ref
            if cell.graph is not None:
                subgraphs[cell.name] = cell.graph
        return subgraphs


class ElementList(TypedList, ElementFilterMixin):
    """

    """

    def __repr__(self):
        string = '\n'.join('{}'.format(k) for k in enumerate(self._list))
        return string

    def __str__(self):
        return self.__repr__()

    def __getitem__(self, i):
        if isinstance(i, str):
            for cell_ref in self.sref:
                name = cell_ref.ref.name
                rest = name.split('-', 1)[0]
                if i == rest: return cell_ref
        elif isinstance(i, tuple):
            elems = ElementList()
            for e in self.polygons:
                if e.gdslayer.key == i:
                    elems += e
            return elems
        else:
            return self._list[i]

    def __delitem__(self, key):
        for i in range(0, len(self._list)):
            if self._list[i] is key:
                return list.__delitem__(self._list, i)

    def __deepcopy__(self, memo):
        from copy import deepcopy
        L = self.__class__()
        for item in self._list:
            L.append(deepcopy(item))
            # L += deepcopy(item)
        return L

    def __contains__(self, name):
        import spira
        for item in self._list:
            if isinstance(item, spira.Cell):
                if item.name == name:
                    return True
        return False

    # def dependencies(self):
    #     d = ElementList()
    #     for e in self._list:
    #         d.add(e.dependencies())
    #     return d

    def dependencies(self):
        import spira
        from spira.kernel.cell import CellList

        cells = CellList()
        for e in self._list:
            cells.add(e.dependencies())
        return cells

    def add(self, item):
        import spira
        from spira.kernel.cell import CellList

        cells = CellList()
        for e in self._list:
            cells.add(e.dependencies())
        return cells

        # types = (spira.ElementList, list, set)
        # if item == None:
        #     return
        # if isinstance(item, spira.Cell):
        #     if not self.__contains__(item.name):
        #         self += item
        # elif isinstance(item, types):
        #     for s in item:
        #         self.add(s)
        # else:
        #     raise ValueError('add element not implemented!!!')

    def stretch(self, stretch_class):
        for c in self:
            c.stretch(stretch_class)
        return self

    def transform(self, transform):
        for c in self:
            c.transform(transform)
        return self

    def flat_elems(self):
        import spira

        def flat(S):
            if S == []:
                return S
            if isinstance(S[0], list):
                return flat(S[0]) + flat(S[1:])
            elif isinstance(S[0], ElementList):
                return S[0].flat_elems()
            return S[:1] + flat(S[1:])

        if len(self._list[0]) == 1:
            return self._list

        elems = ElementList()
        for e in flat(self._list):
            if issubclass(type(e), spira.Cell):
                e = e.elementals.flat_elems()
            elems += e
        return elems

    def flat_copy(self, level=-1, commit_to_gdspy=False):
        el = ElementList()
        for e in self._list:
            el += e.flat_copy(level, commit_to_gdspy)
        if level == -1:
            return el.flatten()
        else:
            return el

    def flatten(self):
        from spira.kernel.cell import Cell
        from spira.kernel.elemental.polygons import PolygonAbstract
        from spira.kernel.elemental.sref import SRef
        if isinstance(self, collections.Iterable):
            flat_list = ElementList()
            for i in self._list:
                if issubclass(type(i), Cell):
                    i = i.flat_copy()
                elif isinstance(i, SRef):
                    i = i.flat_copy()
                for a in i.flatten():
                    flat_list += a
            return flat_list
        else:
            return [self._list]

    def generate_cell(self, name):
        from spira.kernel.elemental.sref import SRef
        from spira.kernel.cell import Cell
        cc = Cell(name=name)
        for e in self._list: cc += e
        return SRef(cc)

    def isstored(self, pp):
        for e in self._list:
            return pp == e


from spira.kernel.parameters.descriptor import DataFieldDescriptor
class ElementListField(DataFieldDescriptor):
    __type__ = ElementList

    def __init__(self, default=[], **kwargs):
        kwargs['default'] = self.__type__(default)
        super().__init__(**kwargs)

    def __repr__(self):
        return ''

    def __str__(self):
        return ''

    def call_param_function(self, obj):
        f = self.get_param_function(obj)
        value = f(self.__type__())
        if value is None:
            value = self.__type__()
        obj.__store__[self.__name__] = value
        return value

