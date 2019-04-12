from spira.core import param
from spira.yevon.properties.base import __Properties__
from spira.core.port_list import PortListField


class PortProperties(__Properties__):
    """ Port properties that connects to layout structures. """

    # ports = param.PortListField(fdef_name='create_ports', doc='List of ports to be added to the cell instance.')
    ports = PortListField(fdef_name='create_ports', doc='List of ports to be added to the cell instance.')

    def create_ports(self, ports):
        return ports

 

