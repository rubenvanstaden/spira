import numpy as np


class __Integer__(object):

    def __init__(self, val=0, **kwargs):
        self._val = int(val)

    def __add__(self, val):
        if isinstance(val, Integer):
            return Integer(self._val + val._val)
        return self._val + val

    def __iadd__(self, val):
        self._val += val
        return self

    def __repr__(self):
        return 'Integer(%s)' % self._val

    def __str__(self):
        return str(self._val)

    def __eq__(self, other):
        if isinstance(other, int):
            value = Integer(other)
        elif isinstance(other, Integer):
            value = other
        else:
            raise TypeError('other must be of type int')
        return self._val == value._val

    def __int__(self):
        return self._val

    
from spira.core.descriptor import DataFieldDescriptor
class IntegerField(DataFieldDescriptor):
    __type__ = __Integer__

    def __init__(self, default=0, **kwargs):
        kwargs['default'] = default
        super().__init__(**kwargs)

    def get_stored_value(self, obj):
        value = obj.__store__[self.__name__]
        return value.__int__()

    def __set__(self, obj, value):
        if isinstance(value, self.__type__):
            obj.__store__[self.__name__] = value
        elif isinstance(value, (float, int, np.int64)):
            obj.__store__[self.__name__] = self.__type__(val=value)
        else:
            raise TypeError("Invalid type in setting value " + 
                            "of {} (expected {}): {}"
                            .format(self.__class_, type(value)))
