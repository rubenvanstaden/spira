

class EdgeCapacitor(object):
    _ID = 0

    def __init__(self, node_id=None):
        if node_id is None:
            self.id = 'C{}'.format(EdgeCapacitor._ID)
        else:
            self.id = node_id

        EdgeCapacitor._ID += 1


class EdgeInductor(object):
    _ID = 0

    def __init__(self, node_id=None):
        if node_id is None:
            self.id = 'L{}'.format(EdgeInductor._ID)
        else:
            self.id = node_id

        EdgeInductor._ID += 1





from spira.core.parameters.initializer import ParameterInitializer
class typed_list(ParameterInitializer, list):
    __item_type__ = object

    def __init__(self, items=[]):
        if isinstance(items, list) or isinstance(items, set):
            self.extend(items)
        else:
            self.append(items)
        super(typed_list, self).__init__()

    def __add__(self, other):
        L = self.__class__(self)
        if isinstance(other, list):
            L.extend(other)
        else:
            L.append(other)
        return L

    def __radd__(self, other):
        if isinstance(other, self.__item_type__):
            L = self.__class__([other])
            L.extend(self)
        elif isinstance(other, list):
            L = self.__class__(other)
            L.extend(self)
        return L

    def __iadd__(self, other):
        if isinstance(other, list):
            self.extend(other)
        else:
            self.append(other)
        return self

    def clear(self):
        del self[:]

    def append(self, item):
        if isinstance(item, self.__item_type__):
            list.append(self, item)
        else:
            self.__raise_invalid_type_exception__(item)

    def extend(self, items):
        if type(self) == type(items):
            list.extend(self, items)
        elif isinstance(items, list) or isinstance(items, set):
            for i in items:
                list.append(self, i)
        else:
            raise Exception('items is not a list or set')

    def __deepcopy__(self, memo):
        from copy import deepcopy
        L = self.__class__()
        for item in self:
            L.append(deepcopy(item))
        return L


class PathList(typed_list):
    """A list of Structure objects"""

    def is_empty(self):
        if (len(self) == 0): return True
        for e in self:
            if not e.is_empty(): return False
        return True

    def __getitem__(self, key):
        if isinstance(key, str):
            for i in self:
                if i.name == key: return i
            raise IndexError("Structure " + key + " cannot be found in StructureList.")
        else:
            return list.__getitem__(self,key)

    def __setitem__(self, key, value):
        if isinstance(key, str):
            for i in range(0, len(self)):
                if self[i].name == key: return list.__setitem__(self, i, value)
            list.append(self, value)
        else:
            return list.__setitem__(self,key, value)

    def __delitem__(self, key):
        if isinstance(key, str):
            for i in range(0, len(self)):
                if self[i].name == key: return list.__delitem__(self,i)
                return
            return list.__delitem__(self,key)
        else:
            return list.__delitem__(self,key)

    def __contains__(self, item):
        if isinstance(item, Structure):
            name = item.name
        else:
            name = item
        if isinstance(name, str):
            for i in self:
                if i.name == name: 
                    return True
            return False
        else:
            return list.__contains__(self, item)

    def __fast_contains__(self, name):
        for i in self:
            if i.name == name: 
                return True
        return False

    def index(self, item):
        if isinstance(item, str):
            for i in range(0, len(self)):
                if list.__getitem__(self, i).name == item:
                    return i
            raise ValueError("Structure " + item + " is not in StructureList")
        else:
            list.index(self, item)

    def append(self, other, overwrite=False):
        if len(other) == 2:
            list.append(self, other)

        valid = True
#         for path in self:
#             if set([other[0], other[-1]]).issubset(path):
#                 valid = False

        if valid is True:
            list.append(self, other)


