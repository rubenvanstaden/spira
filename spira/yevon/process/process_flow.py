from spira.core.parameters.initializer import FieldInitializer
from spira.core.parameters.descriptor import DataField, RestrictedParameter
from spira.core.parameters.restrictions import RestrictType


__all__ = ['VModelProcessFlow', 'VModelProcessFlowField']


class VModelProcessFlow(FieldInitializer):
    """  """

    active_processes = DataField(doc='Active process layers for virtual model creation.')


def VModelProcessFlowField(local_name=None, restriction=None, **kwargs):
    R = RestrictType(VModelProcessFlow) & restriction
    return RestrictedParameter(local_name, restriction=R, **kwargs)   

