from spira.core.parameters.variables import StringField, IntegerField
from spira.core.parameters.initializer import FieldInitializer
from copy import deepcopy
from spira.core.parameters.descriptor import DataFieldDescriptor, DataField
from spira.core.parameters.restrictions import RestrictType


__all__ = ['Layer', 'LayerField']


class Layer(FieldInitializer):

    doc = StringField()
    name = StringField()
    number = IntegerField(default=0)
    datatype = IntegerField(default=0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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


def LayerField(name='noname', number=0, datatype=0, **kwargs):
    from spira.yevon.layer import Layer
    if 'default' not in kwargs:
        kwargs['default'] = Layer(name=name, number=number, datatype=datatype, **kwargs)
    R = RestrictType(Layer)
    return DataFieldDescriptor(restrictions=R, **kwargs)
