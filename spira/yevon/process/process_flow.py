from spira.core.parameters.initializer import ParameterInitializer
from spira.core.parameters.descriptor import Parameter, RestrictedParameter
from spira.core.parameters.restrictions import RestrictType


__all__ = ['VModelProcessFlow', 'VModelProcessFlowParameter']


class VModelProcessFlow(ParameterInitializer):
    """  """

    active_processes = Parameter(doc='Active process layers for virtual model creation.')


def VModelProcessFlowParameter(local_name=None, restriction=None, **kwargs):
    R = RestrictType(VModelProcessFlow) & restriction
    return RestrictedParameter(local_name, restriction=R, **kwargs)   

