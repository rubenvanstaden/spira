import numpy as np
import networkx as nx
from spira.core.parameters.restrictions import RestrictType, RestrictRange
from spira.core.parameters.descriptor import DataFieldDescriptor


NUMBER = RestrictType((int, float, np.int32, np.int64, np.float))
FLOAT = RestrictType(float)
INTEGER = RestrictType(int)
COMPLEX = RestrictType((int, float, complex))
STRING = RestrictType(str)
BOOL = RestrictType(bool)
DICTIONARY = RestrictType(dict)
LIST = RestrictType(list)
TUPLE = RestrictType(tuple)
NUMPY_ARRAY = RestrictType(np.ndarray)
GRAPH = RestrictType(nx.Graph)


def NumberField(restriction=None, **kwargs):
    if 'default' not in kwargs:
        kwargs['default'] = 0
    R = NUMBER & restriction
    return DataFieldDescriptor(restriction=R, **kwargs)
    

def ComplexField(restriction=None, **kwargs):
    from .variables import COMPLEX
    if 'default' not in kwargs:
        kwargs['default'] = 0
    return DataFieldDescriptor(restriction=COMPLEX, **kwargs)


def IntegerField(restriction=None, **kwargs):
    from .variables import INTEGER
    if 'default' not in kwargs:
        kwargs['default'] = 0
    return DataFieldDescriptor(restriction=INTEGER, **kwargs)


def FloatField(restriction=None, **kwargs):
    from .variables import FLOAT
    if 'default' not in kwargs:
        kwargs['default'] = 0.0
    return DataFieldDescriptor(restriction=FLOAT, **kwargs)


def StringField(restriction=None, **kwargs):
    from .variables import STRING
    if 'default' not in kwargs:
        kwargs['default'] = ''
    R = STRING & restriction
    return DataFieldDescriptor(restriction=R, **kwargs)


def BoolField(restriction=None, **kwargs):
    from .variables import BOOL
    if 'default' not in kwargs:
        kwargs['default'] = False
    return DataFieldDescriptor(restriction=BOOL, **kwargs)


def ListField(restriction=None, **kwargs):
    from .variables import LIST
    if 'default' not in kwargs:
        kwargs['default'] = []
    return DataFieldDescriptor(restriction=LIST, **kwargs)


def TupleField(restriction=None, **kwargs):
    from .variables import TUPLE
    if 'default' not in kwargs:
        kwargs['default'] = []
    return DataFieldDescriptor(restriction=TUPLE, **kwargs)


def DictField(restriction=None, **kwargs):
    from .variables import DICTIONARY
    if 'default' not in kwargs:
        kwargs['default'] = {}
    return DataFieldDescriptor(restriction=DICTIONARY, **kwargs)


def NumpyArrayField(restriction=None, **kwargs):
    from .variables import NUMPY_ARRAY
    if 'default' not in kwargs:
        kwargs['default'] = np.array([])
    return DataFieldDescriptor(restriction=NUMPY_ARRAY, **kwargs)


def GraphField(restriction=None, **kwargs):
    from .variables import GRAPH
    if 'default' not in kwargs:
        kwargs['default'] = nx.Graph()
    R = GRAPH
    return DataFieldDescriptor(restriction=R, **kwargs)

