import collections
from spira.param.field.typed_list import TypedList


class ElementFilterMixin(object):

    def get_polygons(self, layer=None, cell_type=None):
        from spira.layer import Layer
        from spira.rdd.layer import PurposeLayer
        elems = ElementList()
        if layer is None:
            raise ValueError('Layer not set.')
        for ply in self.polygons:
            if cell_type is not None:
                if isinstance(layer, Layer):
                    if layer.is_equal_number(ply.gdslayer):
                        if ply.gdslayer.datatype == cell_type:
                            elems += ply
                elif isinstance(layer, PurposeLayer):
                    if ply.gdslayer.number == layer.datatype:
                        if ply.gdslayer.datatype == cell_type:
                            elems += ply
            else:
                if isinstance(layer, Layer):
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
            if issubclass(type(e), Cell):
            # if isinstance(e, Cell):
                elems += e
        return elems


class __ElementList__(TypedList, ElementFilterMixin):

    def __repr__(self):
        string = '\n'.join('{}'.format(k) for k in enumerate(self._list))
        return string

    def __str__(self):
        return self.__repr__()

    def __getitem__(self, value):
        r_val = None
        if isinstance(value, str):
            for e in self.cells:
                # print(e.name)
                name = e.name.split('_')[0]
                if name == value:
                    r_val = e
            # for p in self.polygons:
            #     if e.name == value:
            #         r_val = e
            # for e in self._list:
            #     if e.node_id == value:
            #         r_val = e
        else:
            r_val = self._list[value]
        if r_val is None:
            raise ValueError('Elemental not found!')
        return r_val

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

    def dependencies(self):
        import spira
        from spira.gdsii.lists.cell_list import CellList
        from spira import pc
        from spira.process.processlayer import ProcessLayer
        cells = CellList()
        for e in self._list:
            if not issubclass(type(e), ProcessLayer):
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

    def flat_copy(self, level=-1):
        el = ElementList()
        for e in self._list:
            el += e.flat_copy(level)
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

    def isstored(self, pp):
        for e in self._list:
            return pp == e




