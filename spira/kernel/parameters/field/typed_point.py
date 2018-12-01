import numpy as np
from spira.kernel.parameters.descriptor import DataFieldDescriptor
from spira.kernel.utils import scale_coord_up as scu
from spira.kernel.utils import SCALE_UP


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

        s1 = abs(value[0]/SCALE_UP)
        s2 = abs(value[1]/SCALE_UP)
        if (s1 < 1e-1):
            value[0] = SCALE_UP*value[0]
        if (s2 < 1e-1):
            value[1] = SCALE_UP*value[1]
        obj.__store__[self.__name__] = value

