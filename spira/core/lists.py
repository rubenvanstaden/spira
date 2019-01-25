
import collections
from spira.param.field.typed_list import TypedList


class ElementFilterMixin(object):

    def add_elem_to_cell(self, elem, cellname):
        for sref in self.sref:
            if sref.ref.name == cellname:
                self += elem

    def get_polygons(self, layer=None):
        from spira.gdsii.layer import Layer
        from spira.rdd.layer import PurposeLayer
        elems = ElementList()
        for ply in self.polygons:
            if layer is not None:
                if isinstance(layer, Layer):
                    # if ply.gdslayer == layer:
                    if layer.is_equal_number(ply.gdslayer):
                        elems += ply
                elif isinstance(layer, PurposeLayer):
                    if ply.gdslayer.number == layer.datatype:
                        elems += ply
        return elems

    @property
    def polygons(self):
        from spira.gdsii.elemental.polygons import PolygonAbstract
        elems = ElementList()
        for e in self._list:
            if issubclass(type(e), PolygonAbstract):
                elems += e
        return elems

    @property
    def cells(self):
        from spira.gdsii.cell import Cell
        elems = ElementList()
        for e in self._list:
            if issubclass(type(e), Cell):
                elems += e
        return elems

    @property
    def metals(self):
        from spira.rdd import get_rule_deck
        from spira.gdsii.elemental.polygons import PolygonAbstract
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
            for Sm in S.ref.elementals.sref:
                if isinstance(Sm.ref, MLayer):
                    elems += Sm
        return elems

    @property
    def dlayers(self):
        from spira.lpe.primitives import NLayer
        elems = ElementList()
        for S in self._list:
            for Sn in S.ref.elementals.sref:
                if isinstance(Sn.ref, NLayer):
                    elems += Sn
        return elems

    def get_dlayer(self, layer):
        elems = ElementList()
        for S in self.dlayers:
            for p in S.ref.elementals.polygons:
                if isinstance(layer, int):
                    if p.gdslayer.number == layer:
                        elems += S
                else:
                    if p.gdslayer == layer:
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
        from spira.gdsii.elemental.label import Label
        elems = ElementList()
        for e in self._list:
            if isinstance(e, Label):
                elems += e
        return elems

    @property
    def sref(self):
        from spira.gdsii.elemental.sref import SRef
        elems = ElementList()
        for e in self._list:
            if isinstance(e, SRef):
                elems += e
        return elems

    @property
    def cells(self):
        from spira.gdsii.cell import Cell
        elems = ElementList()
        for e in self._list:
            if isinstance(e, Cell):
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
            if cell.elementals.graph is not None:
                subgraphs[cell.name] = cell.elementals.graph
        return subgraphs


class __ElementList__(TypedList, ElementFilterMixin):

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
        return L

    def __contains__(self, name):
        import spira
        for item in self._list:
            if isinstance(item, spira.Cell):
                if item.name == name:
                    return True
        return False


class ElementList(__ElementList__):
    """

    """

    def dependencies(self):
        import spira
        from spira.gdsii.lists.cell_list import CellList

        cells = CellList()
        for e in self._list:
            cells.add(e.dependencies())
        return cells

    def add(self, item):
        import spira
        from spira.gdsii.lists.cell_list import CellList

        cells = CellList()
        for e in self._list:
            cells.add(e.dependencies())
        return cells

    def stretch(self, stretch_class):
        for c in self:
            c.stretch(stretch_class)
        return self

    def transform(self, transform):
        for c in self:
            c.transform(transform)
        return self

    def flat_elems(self):
        def _flatten(list_to_flatten):
            for elem in list_to_flatten:
                if isinstance(elem, (ElementList, list, tuple)):
                    for x in _flatten(elem):
                        yield x
                else:
                    yield elem

        return _flatten(self._list)

    def flat_copy(self, level=-1, commit_to_gdspy=False):
        el = ElementList()
        for e in self._list:
            el += e.flat_copy(level, commit_to_gdspy)
        if level == -1:
            return el.flatten()
        else:
            return el

    def flatten(self):
        from spira.gdsii.cell import Cell
        from spira.gdsii.elemental.polygons import PolygonAbstract
        from spira.gdsii.elemental.sref import SRef
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
        from spira.gdsii.elemental.sref import SRef
        from spira.gdsii.cell import Cell
        cc = Cell(name=name)
        for e in self._list: cc += e
        return SRef(cc)

    def isstored(self, pp):
        for e in self._list:
            return pp == e




