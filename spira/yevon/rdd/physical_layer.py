from spira.core.parameters.variables import StringField, IntegerField
from spira.yevon.rdd.gdsii_layer import Layer
from spira.yevon.rdd.technology import ProcessTree
from spira.yevon.rdd.process_layer import ProcessField
from spira.yevon.rdd.purpose_layer import PurposeLayerField
from spira.core.parameters.initializer import FieldInitializer
from spira.core.parameters.descriptor import RestrictedParameter
from spira.core.parameters.restrictions import RestrictType
from spira.yevon.rdd.gdsii_layer import Layer


__all__ = ['PhysicalLayer', 'PhysicalLayerField']


class PhysicalLayer(Layer):
    """ Object that maps a layer and purpose.

    Examples
    --------
    >>> ps_layer = PhysicalLayer()
    """

    process = ProcessField()
    purpose = PurposeLayerField()
    # parameters = ParameterDatabaseField()

    def __init__(self, process, purpose, **kwargs):
        super().__init__(process=process, purpose=purpose, **kwargs)

    def __repr__(self):
        string = '[SPiRA: PhysicalLayer] (layer \'{}\', symbol \'{}\')'
        return string.format(self.number, self.purpose.symbol)

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
    def key(self):
        return (self.number, self.purpose.symbol, 'physical_layer_key')


def PhysicalLayerField(local_name=None, restriction=None, **kwargs):
    R = RestrictType(PhysicalLayer) & restriction
    return RestrictedParameter(local_name, restrictions=R, **kwargs)


    
