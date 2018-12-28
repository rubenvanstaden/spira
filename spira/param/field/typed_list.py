import collections


class TypedList(collections.abc.MutableSequence):
    __item_type__ = object

    def __init__(self, items=[]):
        super().__init__()
        self._list = list(items)

    def __repr__(self):
        return '\n'.join('{}'.format(k) for k in enumerate(self._list))

    def __str__(self):
        return str(self._list)

    def __add__(self, other):
        L = self.__class__(self)
        if other:
            if isinstance(other, list):
                L.extend(other)
            else:
                L.append(other)
        return L

    def __radd__(self, other):
        L = self.__class__(other)
        if other:
            if isinstance(other, self.__item_type__):
                L = self.__class__([other])
                L.extend(self)
            elif isinstance(other, list):
                L.extend(self)
        return L

    def __iadd__(self, other):
        if other:
            if isinstance(other, list):
                self.extend(other)
            else:
                self.append(other)
        return self

    def __len__(self):
        return len(self._list)

    def __getitem__(self, i):
        return self._list[i]

    def __setitem__(self, i, v):
        self._list[i] = v

    def __deepcopy__(self, memo):
        from copy import deepcopy
        L = self.__class__()
        for item in self._list:
            L.append(deepcopy(item))
        return L

    def check(self, v):
        if not isinstance(v, self.oktypes):
            raise TypeError('Invalid type')

    def insert(self, i, v):
        self._list.insert(i, v)

    def append(self, val):
        self.insert(len(self._list), val)
        # self._list.append(val)

    @property
    def value(self):
        value_list = []
        for i in self._list:
            if isinstance(i, float):
                value_list.append(i._val)
        return value_list

    def clear(self):
        del self[:]


from spira.core.descriptor import DataFieldDescriptor
class ListField(DataFieldDescriptor):
    __type__ = TypedList

    def __init__(self, default=[], **kwargs):
        kwargs['default'] = self.__type__(default)
        super().__init__(**kwargs)

    def get_stored_value(self, obj):
        value = obj.__store__[self.__name__]
        return list(value)

    def __set__(self, obj, value):
        if isinstance(value, self.__type__):
            obj.__store__[self.__name__] = value
        elif isinstance(value, list):
            obj.__store__[self.__name__] = self.__type__(items=value)
        else:
            raise TypeError("Invalid type in setting value " + 
                            "of {} (expected {}): {}"
                            .format(self.__class_, type(value)))



