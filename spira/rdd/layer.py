from spira import param
from spira.rdd.technology import ProcessTree
from spira.core.initializer import ElementalInitializer


class __Layer__(ElementalInitializer):
    pass


class PurposeLayer(__Layer__):

    doc = param.StringField()
    name = param.StringField()
    datatype = param.IntegerField(default=0)
    symbol = param.StringField()

    def __init__(self, **kwargs):
        ElementalInitializer.__init__(self, **kwargs)

    # def __repr__(self):
    #     string = '[SPiRA: PurposeLayer] (\'{}\', datatype {}, symbol \'{}\')'
    #     return string.format(self.name, self.datatype, self.symbol)

    def __eq__(self, other):
        # print(other)
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
        if isinstance(other, PurposeLayer):
            d = self.datatype + other.datatype
        elif isinstance(other, int):
            d = self.datatype + other
        else:
            raise ValueError('Not Implemented')
        return PurposeLayer(datatype=d)

    def __iadd__(self, other):
        if isinstance(other, PurposeLayer):
            self.datatype += other.datatype
        elif isinstance(other, int):
            self.datatype += other
        else:
            raise ValueError('Not Implemented')
        return self

    def __deepcopy__(self, memo):
        return PurposeLayer(
            name=self.name,
            datatype=self.datatype,
            symbol=self.symbol
        )

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

    doc = param.StringField()
    layer = param.LayerField()
    purpose = PurposeLayerField()
    data = param.DataField(default=ProcessTree())

    def __init__(self, **kwargs):
        ElementalInitializer.__init__(self, **kwargs)

    def __repr__(self):
        string = '[SPiRA: PhysicalLayer] (layer \'{}\', symbol \'{}\')'
        return string.format(self.layer.name, self.purpose.symbol)

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if isinstance(other, PhysicalLayer):
            return other.key == self.key
        # elif isinstance(other, Layer):
        #     return other.number == self.layer.number
        elif isinstance(other, int):
            return other == self.layer.number
        else:
            raise ValueError('Not Implemented!')

    def __neq__(self, other):
        if isinstance(other, PhysicalLayer):
            return other.key != self.key
        # elif isinstance(other, Layer):
        #     return other.number != self.layer.number
        elif isinstance(other, int):
            return other != self.layer.number
        else:
            raise ValueError('Not Implemented!')
    
    # def __add__(self, other):
    #     if isinstance(other, PhysicalLayer):
    #         d = self.datatype + other.datatype
    #     elif isinstance(other, int):
    #         d = self.datatype + other
    #     else:
    #         raise ValueError('Not Implemented')
    #     return PurposeLayer(datatype=d)

    # def __iadd__(self, other):
    #     if isinstance(other, PhysicalLayer):
    #         self.datatype += other.datatype
    #     elif isinstance(other, int):
    #         self.datatype += other
    #     else:
    #         raise ValueError('Not Implemented')
    #     return self

    @property
    def key(self):
        return (self.layer.number, self.purpose.symbol)


# from spira.core.descriptor import DataFieldDescriptor
# def PhysicalLayerField(layer, purpose):
#     F = PhysicalLayer(layer=layer, purpose=purpose)
#     return DataFieldDescriptor(default=F)



    
