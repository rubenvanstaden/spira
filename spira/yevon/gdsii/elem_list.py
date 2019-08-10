import collections

from spira.yevon.gdsii.base import __Element__
from spira.core.typed_list import TypedList
from spira.core.parameters.restrictions import RestrictType
from spira.core.parameters.descriptor import ParameterDescriptor
from spira.core.transformable import Transformable


class __ElementList__(TypedList, Transformable):

    def __repr__(self):
        string = '\n'.join('{}'.format(k) for k in enumerate(self._list))
        return string

    def __str__(self):
        return self.__repr__()

    def __getitem__(self, value):
        from spira.yevon.gdsii.cell import Cell
        from spira.yevon.gdsii.sref import SRef
        from spira.yevon.gdsii.polygon import Polygon
        r_val = None
        if isinstance(value, str):
            for e in self._list:
                if issubclass(type(e), (Cell, SRef, Polygon)):
                    if e.alias == value:
                        r_val = e
        elif isinstance(value, int):
            r_val = self._list[value]
        else:
            raise ValueError('Invalid value to get element.')
        if r_val is None:
            raise ValueError('Element not found!')
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

    __item_type__ = __Element__

    @property
    def labels(self):
        from spira.yevon.gdsii.label import Label
        elems = ElementList()
        for e in self._list:
            if isinstance(e, Label):
                elems += e
        return elems

    @property
    def polygons(self):
        # from spira.yevon.gdsii.polygon import Polygon
        from spira.yevon.gdsii.polygon import __ShapeElement__
        elems = ElementList()
        for e in self._list:
            # if isinstance(e, Polygon):
            if isinstance(e, __ShapeElement__):
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
    def bbox_info(self):
        from spira.yevon.geometry.bbox_info import BoundaryInfo
        if len(self) == 0:
            return BoundaryInfo()
        else:
            SI = self._list[0].bbox_info
            for e in self._list[1::]:
                SI += e.bbox_info
            return SI

    def nets(self, lcar=100):
        from spira.yevon.geometry.nets.net_list import NetList
        nets = NetList()
        for e in self._list:
            nets += e.nets(lcar=lcar)
        return nets

    def dependencies(self):
        from spira.yevon.gdsii.cell_list import CellList
        cells = CellList()
        for e in self._list:
            cells.add(e.dependencies())
        return cells

    def expand_transform(self):
        for S in self.sref:
            S.expand_transform()
            S.reference.expand_transform()
        return self

    def transform(self, transformation=None):
        for c in self._list:
            c.transform(transformation)
        return self

    def add(self, item):
        import spira.all as spira
        from spira.yevon.gdsii.cell_list import CellList
        cells = CellList()
        for e in self._list:
            cells.add(e.dependencies())
        return cells

    def flat_elems(self):
        def _flatten(list_to_flatten):
            for elem in list_to_flatten:
                if isinstance(elem, (ElementList, list, tuple)):
                    for x in _flatten(elem): yield x
                else: yield elem
        return _flatten(self._list)

    def flat_copy(self, level=-1):
        elems = ElementList()
        for e in self._list:
            elems += e.flat_copy(level)
        return elems

    def flatten(self, level=-1, name_tree=[]):
        elems = ElementList()
        for e in self._list:
            elems += e.flatten(level, name_tree)
        return elems
        
    def flat_container(self, cc, name_tree=[]):
        for e in self._list:
            e.flat_container(cc, name_tree)

    def is_stored(self, pp):
        for e in self._list:
            return pp == e

    def is_empty(self):
        if (len(self._list) == 0):
            return True
        for e in self._list:
            if not e.is_empty():
                return False
        return True

    def append(self, item):
        from spira.yevon.gdsii.group import Group
        if isinstance(item, Group):
            self._list.extend(item.elements)
        elif isinstance(item, self.__item_type__):
            self._list.append(item)
        elif isinstance(item, list):
            self._list.extend(item)
        else:
            error_message = "You are trying to add an element of type {} to {}. You can only add elements of type {}."
            raise ValueError(error_message.format(str(type(item)), str(self.__class__), str(self.__item_type__)))


class ElementListParameter(ParameterDescriptor):
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
        new_value = self.__cache_parameter_value__(obj, value)
        return new_value

