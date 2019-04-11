from spira import shapes
from core import param
from spira.properties.base import __Properties__


class PortProperties(__Properties__):
    """ Port properties that connects to layout structures. """

    ports = param.PortListField(fdef_name='create_ports', doc='List of ports to be added to the cell instance.')

    def create_ports(self, ports):
        return ports

 

