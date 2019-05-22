from spira.yevon.properties.base import __Property__
from spira.yevon.netlist.net_list import NetListField


class NetProperties(__Property__):
    """ Defines the nets from the defined elementals. """

    nets = NetListField(fdef_name='create_nets', doc='List of nets to be added to the cell instance.')

    def create_nets(self, nets):
        return nets

