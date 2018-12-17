from spira.core.initializer import BaseElement
from spira import param


class __Layer__(BaseElement):
    pass


class PurposeLayer(__Layer__):

    name = param.StringField()
    datatype = param.IntegerField()
    symbol = param.StringField()

    def __init__(self, **kwargs):
        BaseElement.__init__(self, **kwargs)

    def __repr__(self):
        string = '[SPiRA: PurposeLayer] (\'{}\', datatype {}, symbol \'{}\')'
        return string.format(self.name, self.datatype, self.symbol)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if isinstance(other, PurposeLayer):
            return self.key == other.key
        else:
            raise ValueError('Not Implemented!')

    def __ne__(self, other):
        if isinstance(other, PurposeLayer):
            return self.key != other.key
        else:
            raise ValueError('Not Implemented!')

    def __add__(self, other):
        assert isinstance(other, int)
        self.number = self.number + other
        return self

    def __deepcopy__(self, memo):
        return PurposeLayer(name=self.name,
                            datatype=self.datatype,
                            symbol=self.symbol)

    @property
    def key(self):
        return (self.datatype, self.symbol)


from spira.core.descriptor import DataFieldDescriptor
def PurposeLayerField(name='', datatype=0, symbol=''):
    F = PurposeLayer(name=name, datatype=datatype, symbol='')
    return DataFieldDescriptor(default=F)


class PhysicalLayer(__Layer__):
    """

    """

    layer = param.LayerField()
    purpose = PurposeLayerField()

    def __init__(self, **kwargs):
        BaseElement.__init__(self, **kwargs)

    def __repr__(self):
        string = '[SPiRA: PhysicalLayer] (layer \'{}\', symbol \'{}\')'
        return string.format(self.layer.name, self.purpose.symbol)

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if isinstance(other, PhysicalLayer):
            return other.key == self.key
        elif isinstance(other, Layer):
            return other.number == self.layer.number
        elif isinstance(other, int):
            return other == self.layer.number
        else:
            raise ValueError('Not Implemented!')

    def __neq__(self, other):
        if isinstance(other, PhysicalLayer):
            return other.key != self.key
        elif isinstance(other, Layer):
            return other.number != self.layer.number
        elif isinstance(other, int):
            return other != self.layer.number
        else:
            raise ValueError('Not Implemented!')
    
    @property
    def key(self):
        return (self.layer.number, self.purpose.symbol)


from spira.core.descriptor import DataFieldDescriptor
def PhysicalLayerField(layer, purpose):
    F = PhysicalLayer(layer=layer, purpose=purpose)
    return DataFieldDescriptor(default=F)



    
