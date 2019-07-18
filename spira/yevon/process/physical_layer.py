from spira.core.parameters.variables import StringParameter, IntegerParameter
from spira.yevon.process.gdsii_layer import Layer
from spira.yevon.process.technology import ProcessLayerDatabase
from spira.yevon.process.process_layer import ProcessParameter
from spira.yevon.process.purpose_layer import PurposeLayerParameter
from spira.core.parameters.initializer import ParameterInitializer
from spira.core.parameters.descriptor import RestrictedParameter
from spira.core.parameters.restrictions import RestrictType
from spira.yevon.process.gdsii_layer import Layer


__all__ = ['PhysicalLayer', 'PLayer']


class PhysicalLayer(Layer):
    """ Object that maps a layer and purpose.

    Examples
    --------
    >>> layer = PhysicalLayer()
    """

    process = ProcessParameter()
    purpose = PurposeLayerParameter()

    def __init__(self, process, purpose, **kwargs):
        super().__init__(process=process, purpose=purpose, **kwargs)

    def __repr__(self):
        string = '[SPiRA: PhysicalLayer] (name {}, process \'{}\', purpose \'{}\')'
        return string.format(self.name, self.process.symbol, self.purpose.symbol)

    def __str__(self):
        return 'PLayer {}-{}'.format(self.process.symbol, self.purpose.symbol)

    def __hash__(self):
        return hash(self.__str__())

    def __eq__(self, other):
        if not isinstance(other, PhysicalLayer):
            return False
        return self.key == other.key

    def __neq__(self, other):
        return not self.__eq__()
    
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

    # def __deepcopy__(self, memo):
    #     from copy import deepcopy
    #     return self.__class__(
    #         name=self.name,
    #         number=deepcopy(self.number),
    #         datatype=deepcopy(self.datatype),
    #         process=deepcopy(self.process),
    #         purpose=deepcopy(self.purpose)
    #     )

    @property
    def key(self):
        return (self.process.symbol, self.purpose.symbol)


PLayer = PhysicalLayer

    
