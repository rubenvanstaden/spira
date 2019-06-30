from spira.core.parameters.initializer import ParameterInitializer
from spira.yevon.geometry.ports.port import PortParameter


class PortConnection(ParameterInitializer):
    """  """

    source = PortParameter(doc='Source port for a connection.')
    target = PortParameter(doc='Target port for a connection.')




