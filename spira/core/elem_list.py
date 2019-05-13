import collections
from spira.core.param.field.typed_list import TypedList
from spira.core.descriptor import DataFieldDescriptor
from spira.core.param.restrictions import RestrictType


class ElementFilterMixin(object):

    def get_polygons(self, layer=None, cell_type=None):
        from spira.yevon.layer import Layer
        from spira.yevon.rdd.layer import PurposeLayer
        elems = ElementList()
        if layer is None:
            raise ValueError('Layer not set.')
        for ply in self.polygons:
            if cell_type is not None:
                if isinstance(layer, Layer):
                    if layer.is_equal_number(ply.gds_layer):
                        if ply.gds_layer.datatype == cell_type:
                            elems += ply
                elif isinstance(layer, PurposeLayer):
                    if ply.gds_layer.number == layer.datatype:
                        if ply.gds_layer.datatype == cell_type:
                            elems += ply
            else:
                if isinstance(layer, Layer):
                    if layer.is_equal_number(ply.gds_layer):
                        elems += ply
                elif isinstance(layer, PurposeLayer):
                    if ply.gds_layer.number == layer.datatype:
                        elems += ply
        return elems

    @property
    def polygons(self):
        from spira.yevon.gdsii.polygon import PolygonAbstract
        elems = ElementList()
        for e in self._list:
            if issubclass(type(e), PolygonAbstract):
                elems += e
        return elems

    @property
    def labels(self):
        from spira.yevon.gdsii.label import Label
        elems = ElementList()
        for e in self._list:
            if isinstance(e, Label):
                elems += e
        return elems

    @property
    def sref(self):
        from spira.yevon.gdsii.sref import SRef
        elems = ElementList()
        for e in self._list:
            if isinstance(e, SRef):
                elems += e
        return elems

    @property
    def cells(self):
        from spira.yevon.gdsii.cell import Cell
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
        from spira.yevon.gdsii.cell import Cell
        from spira.yevon.gdsii.polygon import Polygon
        r_val = None
        if isinstance(value, str):
            # for e in self.cells:
            for e in self._list:
                if issubclass(type(e), (Cell, Polygon)):
                    if e.alias == value:
                        r_val = e
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
        import spira.all as spira
        for item in self._list:
            if isinstance(item, spira.Cell):
                if item.name == name:
                    return True
        return False

    def __reversed__(self):
        for e in self._list[::-1]:
            yield e 


class ElementList(__ElementList__):

    def dependencies(self):
        import spira.all as spira
        from spira.yevon.gdsii.cell_list import CellList
        from spira.yevon import process as pc
        from spira.yevon.process.processlayer import ProcessLayer
        cells = CellList()
        for e in self._list:
            if not issubclass(type(e), ProcessLayer):
                cells.add(e.dependencies())
        return cells

    def add(self, item):
        import spira.all as spira
        from spira.yevon.gdsii.cell_list import CellList
        cells = CellList()
        for e in self._list:
            cells.add(e.dependencies())
        return cells

    def expand_transform(self):
        for c in self._list:
            c.expand_transform()
        return self

    def transform(self, transformation=None):
        for c in self._list:
            c.transform(transformation)
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

    def commit_to_gdspy(self, cell, transformation=None):
        for e in self._list:
            if isinstance(e, ElementList):
                e.commit_to_gdspy(cell=cell, transformation=transformation)
            else:
                e.commit_to_gdspy(cell=cell, transformation=transformation)
        return self

    def flat_copy(self, level=-1):
        el = ElementList()
        for e in self._list:
            el += e.flat_copy(level)
        if level == -1:
            return el.flatten()
        else:
            return el

    def flatten(self):
        from spira.yevon.gdsii.cell import Cell
        from spira.yevon.gdsii.polygon import PolygonAbstract
        from spira.yevon.gdsii.sref import SRef
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


class ElementalListField(DataFieldDescriptor):
    __type__ = ElementList

    def __init__(self, default=[], **kwargs):
        kwargs['default'] = self.__type__(default)
        kwargs['restrictions'] = RestrictType([self.__type__])
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

