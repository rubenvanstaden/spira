# from spira.core import param
from spira.core.param.variables import StringField, IntegerField
from spira.yevon.layer import LayerField
from spira.yevon.rdd.technology import ProcessTree
from spira.core.initializer import FieldInitializer
from spira.core.descriptor import DataFieldDescriptor, DataField
from spira.core.param.restrictions import RestrictType


class PurposeLayer(FieldInitializer):
    """

    Examples
    --------
    >>> pp_layer = PurposeLayer()
    """

    # doc = param.StringField()
    # name = param.StringField()
    # datatype = param.IntegerField(default=0)
    # symbol = param.StringField()
    
    doc = StringField()
    name = StringField()
    datatype = IntegerField(default=0)
    symbol = StringField()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
        return (self.datatype, self.symbol, 'purpose_layer_key')


def PurposeLayerField(name='', datatype=0, symbol='', **kwargs):
    from spira.yevon.rdd.layer import PurposeLayer
    if 'default' not in kwargs:
        kwargs['default'] = PurposeLayer(name=name, datatype=datatype, symbol='')
    R = RestrictType(PurposeLayer)
    return DataFieldDescriptor(restrictions=R, **kwargs)


class PhysicalLayer(FieldInitializer):
    """ Object that maps a layer and purpose.

    Examples
    --------
    >>> ps_layer = PhysicalLayer()
    """

    # doc = param.StringField()
    # layer = param.LayerField()
    # purpose = param.PurposeLayerField()
    # data = param.DataField(default=ProcessTree())
    
    doc = StringField()
    layer = LayerField()
    purpose = PurposeLayerField()
    data = DataField(default=ProcessTree())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        string = '[SPiRA: PhysicalLayer] (layer \'{}\', symbol \'{}\')'
        return string.format(self.layer.name, self.purpose.symbol)

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        # return hash(self.node_id)
        return hash(self.__str__())

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
    
    def __add__(self, other):
        if isinstance(other, PhysicalLayer):
            d = self.datatype + other.datatype
        elif isinstance(other, int):
            d = self.datatype + other
        else:
            raise ValueError('Not Implemented')
        return PurposeLayer(datatype=d)

    def __iadd__(self, other):
        if isinstance(other, PhysicalLayer):
            self.datatype += other.datatype
        elif isinstance(other, int):
            self.datatype += other
        else:
            raise ValueError('Not Implemented')
        return self

    @property
    def name(self):
        return self.layer.name

    @property
    def number(self):
        return self.layer.number

    @property
    def datatype(self):
        return self.layer.datatype

    @property
    def key(self):
        return (self.layer.number, self.purpose.symbol, 'physical_layer_key')


def PhysicalLayerField(layer=None, purpose=None, **kwargs):
    from spira.yevon.rdd.layer import PhysicalLayer
    if 'default' not in kwargs:
        kwargs['default'] = PhysicalLayer(layer=layer, purpose=purpose)
    R = RestrictType(PhysicalLayer)
    return DataFieldDescriptor(restrictions=R, **kwargs)


    
