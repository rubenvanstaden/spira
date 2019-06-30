from spira.yevon.aspects.base import __Aspects__
from spira.core.parameters.descriptor import Parameter
from spira.yevon.geometry.nets.net import Net
from spira.yevon.geometry.nets.net_list import NetListParameter


class NetlistAspects(__Aspects__):
    """ Defines the nets from the defined elements. """

    netlist = Parameter(fdef_name='create_netlist')

    def create_netlist(self):
        net = Net()
        return net

