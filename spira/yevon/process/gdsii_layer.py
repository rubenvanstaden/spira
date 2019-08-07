from copy import deepcopy
from spira import settings
from spira.core.parameters.variables import *
# from spira.yevon.process.derived_layers import __Layer__
# from spira.yevon.process.derived_layers import *
from spira.core.parameters.restrictions import RestrictType
from spira.core.parameters.processors import ProcessorInt
from spira.core.parameters.variables import StringParameter, IntegerParameter
from spira.core.parameters.descriptor import RestrictedParameter
from spira.core.parameters.initializer import ParameterInitializer, MetaInitializer
from spira.core.parameters.descriptor import ParameterDescriptor
from spira.core.typed_list import TypedList

import inspect


# __all__ = ['Layer', 'LayerParameter']
# __all__ = ['LayerList', 'LayerListParameter']
# __all__ = ['Layer', 'LayerParameter', 'LayerList', 'LayerListParameter']


class MetaLayer(MetaInitializer):
    """
    Called when a new layer object is created.
    First check is layer already exists in current 
    layer list. If it does, retreive it and return it.
    Otherwise, add this layer to the list and return it. 
    """

    def __call__(cls, *params, **keyword_params):

        kwargs = cls.__map_parameters__(*params, **keyword_params)

        if 'layerlist' in kwargs:
            layerlist = kwargs['layerlist']
            del(kwargs['layerlist'])
        else:
            layerlist = None

        if layerlist is None:
            layerlist = settings.get_current_layerlist()

        cls.__keywords__ = kwargs
        L = super().__call__(**kwargs)
        layer = layerlist.__fast_get_layer__(L.key)
        if layer is None:
            list.append(layerlist, L)
            return L
        else:
            return layer


class __Layer__(ParameterInitializer, metaclass=MetaLayer):
    """  """

    doc = StringParameter()

    def __invert__(self):
        return _DerivedNotLayer(self)

    def __and__(self, other):
        if isinstance(other, __Layer__):
            return _DerivedAndLayer(self, other)
        elif other is None:
            return self
        else:
            raise TypeError("Cannot AND %s with %s" % (type(self),type(other)))

    def __iand__(self, other):
        C = self.__and__(other)
        self = C
        return self

    def __or__(self, other):
        if isinstance(other, __Layer__):
            return _DerivedOrLayer(self, other)
        elif other is None:
            return self
        else:
            raise TypeError("Cannot OR %s with %s" % (type(self),type(other)))

    def __ior__(self, other):
        C = self.__and__(other)
        self = C
        return self

    def __xor__(self, other):
        if isinstance(other, __Layer__):
            return _DerivedXorLayer(self, other)
        elif other is None:
            return self
        else:
            raise TypeError("Cannot XOR %s with %s" % (type(self),type(other)))

    def __ixor__(self, other):
        C = self.__xor__(other)
        self = C
        return self


class Layer(__Layer__):

    name = StringParameter()
    number = IntegerParameter(default=0, preprocess=ProcessorInt())
    datatype = IntegerParameter(default=0, preprocess=ProcessorInt())

    def __init__(self, number=0, datatype=0, layerlist=None, name=None, **kwargs):
        if name is None:
            name = 'layer' + str(number)
        super().__init__(number=number, datatype=datatype, name=name, **kwargs)

    def __repr__(self):
        string = '[SPiRA: Layer] (\'{}\', layer {}, datatype {})'
        return string.format(self.name, self.number, self.datatype)

    def __str__(self):
        return 'Layer{}'.format(self.number)

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        if isinstance(other, Layer):
            return self.key == other.key
        else:
            raise ValueError('Not Implemented!')

    def __neq__(self, other):
        if isinstance(other, Layer):
            return self.key != other.key
        else:
            raise ValueError('Not Implemented!')

    def is_equal_number(self, other):
        return (self.number == other.number)

    @property
    def key(self):
        return (self.number, self.datatype)


class _DerivedSingleLayer(__Layer__):
    name = StringParameter(allow_none=True, default=None)

    def get_layers(self, item):
        if isinstance(item, _DerivedSingleLayer):
            return item.layers()
        else:
            return item

    def __str__(self):
        if self.name != None:
            return self.name
        else:
            return self.__repr__()


class _DerivedDoubleLayer(_DerivedSingleLayer):
    def __init__(self, layer1, layer2):
        super().__init__()
        self.layer1 = layer1
        self.layer2 = layer2      

    def layers(self):
        l = LayerList()
        l += self.get_layers(self.layer1)
        l += self.get_layers(self.layer2)
        return l 


class _DerivedNotLayer(_DerivedSingleLayer):
    def __init__(self, layer1):
        super().__init__()
        self.layer1 = layer1

    def __repr__(self):
        return "(NOT %s)" % (self.layer1)

    @property
    def key(self):
        return "NOT %s"%(self.layer1)

    def layers(self):
        l = LayerList()
        l += self.get_layers(self.layer1)
        return l 


class _DerivedAndLayer(_DerivedDoubleLayer):
    def __repr__(self):
        return "(%s AND %s)" % (self.layer1, self.layer2)

    @property
    def key(self):
        return "%s AND %s"%(self.layer1, self.layer2)


class _DerivedOrLayer(_DerivedDoubleLayer):
    def __repr__(self):
        return "(%s OR %s)" % (self.layer1, self.layer2)

    @property
    def key(self):
        return "%s OR %s"%(self.layer1, self.layer2)


class _DerivedXorLayer(_DerivedDoubleLayer):
    def __repr__(self):
        return "(%s XOR %s)" % (self.layer1, self.layer2)

    @property
    def key(self):
        return "%s XOR %s"%(self.layer1, self.layer2)


class LayerList(TypedList):
    """
    Overload acces routines to get dictionary behaviour 
    but without using the name as primary key.
    """

    __item_type__ = __Layer__

    def __getitem__(self, key):
        if isinstance(key, tuple):
            for i in self._list:
                if i.key == key: 
                    return i
            raise IndexError("layer " + str(key) + " cannot be found in LayerList.")
        elif isinstance(key, str):
            for i in self._list:
                if i.name == key: 
                    return i
            raise IndexError("layer " + str(key) + " cannot be found in LayerList.")
        else:
            raise TypeError("Index is wrong type " + str(type(key)) + " in LayerList")

    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            for i in range(0, len(self)):
                if self._list[i].key == key: 
                    return self._list.__setitem__(self, i, value)
            self._list.append(self, value)
        elif isinstance(key, str):
            for i in range(0, len(self)):
                if self._list[i].name == key: 
                    return self._list.__setitem__(self, i, value)
            self._list.append(self, value)
        else:
            raise TypeError("Index is wrong type " + str(type(key)) + " in LayerList")

    def __delitem__(self, key):
        if isinstance(key, tuple):
            for i in range(0, len(self)):
                if self._list.__getitem__(self, i).key == key: 
                    return self._list.__delitem__(self, i)
                return
            return self._list.__delitem__(self, key)
        if isinstance(key, str):
            for i in range(0, len(self)):
                if self._list.__getitem__(self, i).name == key: 
                    return self._list.__delitem__(self, i)
                return
            return self._list.__delitem__(self,key)
        else:
            raise TypeError("Index is wrong type " + str(type(key)) + " in LayerList")

    def __contains__(self, item):
        if isinstance(item, Layer):
            key = item.key
        elif isinstance(item, tuple):
            key = item
        elif isinstance(item, str):
            for i in self._list:
                if i.name == name: 
                    return True
            return False

        if isinstance(key, tuple):
            for i in self._list:
                if i.key == key:
                    return True
            return False

    def __eq__(self, other):
        return set(self) == set(other)

    # def __hash__(self):
    #     return do_hash(self)

    def __fast_get_layer__(self, key):
        for L in self._list:
            if L.key == key:
                return L
        return None

    def index(self, item):
        if isinstance(item, Layer):
            key = item.key
        elif isinstance(item, tuple):
            key = item

        if isinstance(key, tuple):
            for i in range(0, len(self)):
                if self._list.__getitem__(self, i).key == key:
                    return i
            raise ValueError("layer " + key + " is not in LayerList")

        if isinstance(item, str):
            for i in range(0, len(self)):
                if self._list.__getitem__(self, i).name == item:
                    return i
            raise ValueError("layer " + item + " is not in LayerList")
        else:
            raise ValueError("layer " + item + " is not in LayerList")

    def add(self, item, overwrite=False):
        if isinstance(item, Layer):
            if not item in self._list:
                self._list.append(item)
            elif overwrite:
                self._list[item.key] = item
                return
        elif isinstance(item, LayerList) or isinstance(item, list):
            for s in item:
                self.add(s, overwrite)
        elif isinstance(item, tuple):
            if overwrite or (not item in self):
                self.add(Layer(number=item[0], datatype=item[1]), overwrite)
        else:
            raise ValueError('Invalid layer list item type.')

    def append(self, other, overwrite=False):
        return self.add(other, overwrite)

    def extend(self, other, overwrite=False):
        return self.add(other, overwrite)

    def clear(self):
        del self._list[:]


class LayerListParameter(ParameterDescriptor):

    __type__ = LayerList

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


def LayerParameter(local_name=None, restriction=None, **kwargs):
    R = RestrictType(__Layer__) & restriction
    return RestrictedParameter(local_name, restriction=R, **kwargs)

