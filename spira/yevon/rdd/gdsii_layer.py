import inspect
from copy import deepcopy
from spira import settings
from spira.core.parameters.restrictions import RestrictType
from spira.core.parameters.variables import StringField, IntegerField
from spira.core.parameters.descriptor import RestrictedParameter
from spira.core.parameters.initializer import FieldInitializer, MetaInitializer


__all__ = ['Layer', 'LayerField']


class MetaLayer(MetaInitializer):
    """
    Called when a new layer object is created.
    First check is layer already exists in current 
    layer list. If it does, retreive it and return it.
    Otherwise, add this layer to the list and return it. 
    """

    def __call__(cls, *params, **keyword_params):

        # p, a, k, d = inspect.getargspec(cls.__init__)
        # if d is None:
        #     d = []
        # kwargs = {}
        # for k, v in zip(p[-len(d):], d):
        #     kwargs[k] = v
        # kwargs.update(keyword_params)
        # for k, v in zip(p[1:len(params)+1], params):
        #     kwargs[k] = v

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


class __Layer__(FieldInitializer, metaclass=MetaLayer):
    """  """

    doc = StringField()

    def __and__(self, other):
        pass

    def __iand__(self, other):
        pass

    def __or__(self, other):
        pass

    def __ior__(self, other):
        pass

    def __xor__(self, other):
        pass

    def __ixor__(self, other):
        pass

    def __invert__(self):
        pass


class Layer(__Layer__):

    name = StringField()
    number = IntegerField(default=0)
    datatype = IntegerField(default=0)

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)

    def __init__(self, number=0, datatype=0, name=None, layerlist=None, **kwargs):
        if name is None:
            name = 'layer' + str(number)
        super().__init__(number=number, datatype=datatype, name=name, **kwargs)

    def __repr__(self):
        string = '[SPiRA: Layer] (\'{}\', layer {}, datatype {})'
        return string.format(self.name, self.number, self.datatype)

    def __eq__(self, other):
        from spira.yevon.rdd.layer import PurposeLayer
        if isinstance(other, Layer):
            return self.key == other.key
        elif isinstance(other, PurposeLayer):
            return self.number == other.datatype
        else:
            raise ValueError('Not Implemented!')

    def __neq__(self, other):
        from spira.yevon.rdd.layer import PurposeLayer
        if isinstance(other, Layer):
            return self.key != other.key
        elif isinstance(other, PurposeLayer):
            return self.number != other.datatype
        else:
            raise ValueError('Not Implemented!')

    def __add__(self, other):
        if isinstance(other, Layer):
            d = self.number + other.number
        elif isinstance(other, int):
            d = self.number + other
        else:
            raise ValueError('Not Implemented')
        return Layer(datatype=d)

    def __iadd__(self, other):
        if isinstance(other, Layer):
            self.number += other.number
        elif isinstance(other, int):
            self.number += other
        else:
            raise ValueError('Not Implemented')
        return self

    def __deepcopy__(self, memo):
        return Layer(
            name=self.name,
            number=deepcopy(self.number),
            datatype=deepcopy(self.datatype)
        )

    @property
    def key(self):
        return (self.number, self.datatype, 'layer_key')

    def is_equal_number(self, other):
        if self.number == other.number:
            return True
        return False


def LayerField(local_name=None, restriction=None, **kwargs):
    R = RestrictType(__Layer__) & restriction
    return RestrictedParameter(local_name, restriction=R, **kwargs)

