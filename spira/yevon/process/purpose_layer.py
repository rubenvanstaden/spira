from spira.core.parameters.variables import StringParameter, IntegerParameter
from spira.core.parameters.initializer import ParameterInitializer, MetaInitializer
from spira.core.parameters.descriptor import RestrictedParameter, Parameter
from spira.core.parameters.restrictions import RestrictType


DEFINED_PURPOSE_LAYERS = {}


__all__ = ['PurposeLayer', 'PurposeLayerParameter']


class MetaPurposeLayer(MetaInitializer):
    """ Metaclass which creates unique pattern purposes """

    def __call__(cls, *params, **keyword_params):
        if 'symbol' in keyword_params:
            symbol = keyword_params['symbol']
        elif len(params) >= 1:
            symbol = params[1]
        else:
            symbol = "XX"
            raise AttributeError("Extension for a pattern purpose should not be empty. Reset to XX")
        
        # extract the name of the new structure based on the arguments of
        # the constructor. For default structures, the name is passed as the first argument

        L = type.__call__(cls, *params, **keyword_params)
        exist = DEFINED_PURPOSE_LAYERS.get(symbol, None)
        if exist:
            return exist
        else:
            DEFINED_PURPOSE_LAYERS[symbol] = L
            return L


class PurposeLayer(ParameterInitializer, metaclass=MetaPurposeLayer):
    """

    Examples
    --------
    >>> pp_layer = PurposeLayer()
    """

    doc = StringParameter()
    name = StringParameter()
    symbol = StringParameter()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        string = '[SPiRA: PurposeLayer] (\'{}\', symbol \'{}\')'
        return string.format(self.name, self.symbol)

    def __str__(self):
        return self.__repr__()
        
    def __hash__(self):
        return hash(self.__str__())

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

    # def __deepcopy__(self, memo):
    #     return self.__class__(name=self.name, symbol=self.symbol)

    @property
    def key(self):
        return (self.name, self.symbol, 'purpose_layer_key')


def PurposeLayerParameter(local_name=None, restriction=None, **kwargs):
    R = RestrictType(PurposeLayer) & restriction
    return RestrictedParameter(local_name, restrictions=R, **kwargs)
