import spira
from spira import param
from spira import shapes
from spira.rdd import get_rule_deck
from spira.rdd.technology import ProcessTree
from demo.pdks import ply
from spira.lpe.devices import __Device__


RDD = get_rule_deck()


class ViaBC(__Device__):
    """ Via component for the AIST process. """

    __name_prefix__ = 'BC'

    um = param.FloatField(default=1e+6)
    w = param.FloatField(default=2*1e6)
    h = param.FloatField(default=2*1e6)

    m1 = param.PhysicalLayerField(default=RDD.PLAYER.COU)
    m2 = param.PhysicalLayerField(default=RDD.PLAYER.BAS)
    cc = param.PhysicalLayerField(default=RDD.PLAYER.BC)

    def create_metals(self, elems):
        elems += ply.Box(player=self.m1, center=(0,0), w=self.w, h=self.h)
        elems += ply.Box(player=self.m2, center=(0,0), w=self.w, h=self.h)
        return elems

    def create_contacts(self, elems):
        elems += ply.Box(player=self.cc, center=(0,0), w=RDD.BC.WIDTH*1e6, h=RDD.BC.WIDTH*1e6)
        return elems

    def create_ports(self, ports):
        ports += spira.Term(name='Input', midpoint=(-self.w/2, 0), orientation=90, width=self.w)
        ports += spira.Term(name='Output', midpoint=(self.w/2, 0), orientation=-90)
        return ports


# class Via(__Device__):
#     """ Via component for the AIST process. """

#     um = param.FloatField(default=1e+6)
#     w = param.FloatField(default=2*1e6)
#     h = param.FloatField(default=2*1e6)

#     m1 = param.PhysicalLayerField(default=RDD.PLAYER.COU)
#     m2 = param.PhysicalLayerField(default=RDD.PLAYER.BAS)
#     cc = param.PhysicalLayerField(default=RDD.PLAYER.BC)

#     def create_metals(self, elems):
#         elems += ply.Box(player=self.m1, center=(0,0), w=self.w, h=self.h)
#         elems += ply.Box(player=self.m2, center=(0,0), w=self.w, h=self.h)
#         return elems

#     def create_contacts(self, elems):
#         elems += ply.Box(player=self.cc, center=(0,0), w=, h=1.0*self.um)
#         return elems

#     def create_ports(self, ports):
#         ports += spira.Term(name='Input', midpoint=(-self.w/2, 0), orientation=90, width=self.w)
#         ports += spira.Term(name='Output', midpoint=(self.w/2, 0), orientation=-90)
#         return ports


if __name__ == '__main__':

    name = 'Via PCell'
    spira.LOG.header('Running example: {}'.format(name))

    via = ViaBC()
    print(via)
    via.output(name=name)

    spira.LOG.end_print('Junction example finished')

