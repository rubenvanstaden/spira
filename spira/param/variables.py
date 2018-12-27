import numpy as np


class __Constraint__(object):

    def __init__(self, **kwargs):
        pass


class ConstaintType(__Constraint__):
    """ restrict the type or types the argument can have. Pass a type or tuple of types """
    def __init__(self, allowed_types):
        self.allowed_types = ()
        self .__types_set = False
        self.__add_type__(allowed_types)
        if not self.__types_set:
            raise ValueError("allowed_typed of Type Restriction should be set on initialization")

    def __add_type__(self, type_type):
        if isinstance(type_type, type):
            self.allowed_types += (type_type,)
            self .__types_set = True
        elif isinstance(type_type, (tuple, list)):
            for T in type_type:
                self.__add_type__(T)
        else:
            raise TypeError("Restrict type should have a 'type' or 'tuple' of types as argument")

    def validate(self, value, obj=None):
        return isinstance(value, self.allowed_types)

    # def __repr__(self):
    #     return "Type Restriction:" + ",".join([T.__name__ for T in self.allowed_types])


FLOAT = ConstaintType(float)
INTEGER = ConstaintType(int)
STRING = ConstaintType(str)
BOOL = ConstaintType(bool)
DICTIONARY = ConstaintType(dict)
LIST = ConstaintType(list)
NUMPY_ARRAY = ConstaintType(np.ndarray)





