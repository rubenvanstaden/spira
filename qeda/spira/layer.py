from core import param
from core.initializer import ElementalInitializer
from copy import deepcopy


class __Layer__(ElementalInitializer):
    pass


class Layer(__Layer__):

    doc = param.StringField()
    name = param.StringField()
    number = param.IntegerField(default=0)
    datatype = param.IntegerField(default=0)

    # def get_datatype(self):
    #     if not hasattr(self, '__datatype__'):
    #         self.__datatype__ = 0
    #     return self.__datatype__

    # def set_datatype(self, value):
    #     if isinstance(value, PurposeLayer):
    #         self.__datatype__ = int(value.datatype)
    #     elif isinstance(value, (int, float)):
    #         self.__datatype__ = int(value)
    #     else:
    #         raise ValueError("Cannot set 'dataype' parameter of type {}".format(type(value)))

    # datatype = param.FunctionField(get_datatype, set_datatype, doc='Set the datatype of the layer.')

    def __init__(self, **kwargs):
        ElementalInitializer.__init__(self, **kwargs)

    def __repr__(self):
        string = '[SPiRA: Layer] (\'{}\', layer {}, datatype {})'
        return string.format(self.name, self.number, self.datatype)

    def __eq__(self, other):
        from spira.rdd.layer import PurposeLayer
        if isinstance(other, Layer):
            return self.key == other.key
        elif isinstance(other, PurposeLayer):
            return self.number == other.datatype
        else:
            raise ValueError('Not Implemented!')

    def __neq__(self, other):
        from spira.rdd.layer import PurposeLayer
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



