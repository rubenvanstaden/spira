from spira.core.parameters.initializer import FieldInitializer
from spira.yevon.geometry.ports.port import PortField


class PortConnection(FieldInitializer):
    """  """

    source = PortField(doc='Source port for a connection.')
    target = PortField(doc='Target port for a connection.')




