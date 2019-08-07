from spira.core.parameters.restrictions import RestrictType
from spira.core.parameters.variables import StringParameter, IntegerParameter
from spira.core.parameters.initializer import ParameterInitializer, MetaInitializer
from spira.core.parameters.descriptor import RestrictedParameter, Parameter


DEFINED_PROCESS_LAYERS = {}


__all__ = ['ProcessLayer', 'ProcessParameter']


class MetaProcessLayer(MetaInitializer):
    """
    Metaclass which creates unique process layers. 
    It is called when a new object is created. 
    """

    def __call__(cls, *params, **keyword_params):
        if 'symbol' in keyword_params:
            symbol = keyword_params['symbol']
        elif len(params) >= 1:
            symbol = params[1]
        else:
            symbol = "XX"
            raise AttributeError("Extension for a process layer should not be empty. Reset to XX")

        # extract the name of the new structure based on the arguments of
        # the constructor. For default structures, the name is passed as the first argument

        L = type.__call__(cls, *params, **keyword_params)
        exist = DEFINED_PROCESS_LAYERS.get(symbol, None)
        if exist:
            return exist
        else:
            DEFINED_PROCESS_LAYERS[symbol] = L
            return L


class ProcessLayer(ParameterInitializer, metaclass=MetaProcessLayer):
    """  """

    name = StringParameter()
    symbol = StringParameter()

    def __init__(self, name, symbol, **kwargs):
        super().__init__(name = name, symbol = symbol, **kwargs)

    def __eq__(self, other):
        if not isinstance(other, ProcessLayer): return False
        return self.symbol == other.symbol

    def __ne__(self, other):
        return (not self.__eq__(other))    

    def __repr__(self):
        return "[SPiRA: Process] (name {}, symbol {})".format(self.name, self.symbol)

    def __str__(self):
        return self.__repr__()
        
    def __hash__(self):
        return hash(self.__str__())


def ProcessParameter(local_name=None, restriction=None, **kwargs):
    R = RestrictType(ProcessLayer) & restriction
    return RestrictedParameter(local_name, restriction=R, **kwargs)



