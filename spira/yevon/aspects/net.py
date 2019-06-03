from spira.yevon.aspects.base import __Aspects__
from spira.yevon.netlist.net_list import NetListField


class NetAspects(__Aspects__):
    """ Defines the nets from the defined elementals. """

    nets = NetListField(fdef_name='create_nets', doc='List of nets to be added to the cell instance.')

    def create_nets(self, nets):
        return nets

