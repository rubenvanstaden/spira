import numpy as np
from spira.core.descriptor import DataFieldDescriptor


class PointField(DataFieldDescriptor):
    __type__ = list

    def __init__(self, default=(0,0), **kwargs):
        kwargs['default'] = self.__type__(default)
        super().__init__(**kwargs)

    def get_stored_value(self, obj):
        value = obj.__store__[self.__name__]
        return self.__type__(value)

    def __set__(self, obj, value):
        if isinstance(value, (list, set, tuple, np.ndarray)):
            value = self.__type__(value)
        else:
            raise TypeError("Invalid type in setting value " +
                            "of {} (expected {}): {}"
                            .format(self.__class__, type(value)))

        obj.__store__[self.__name__] = value





