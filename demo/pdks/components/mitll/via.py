import spira
from spira import param
from spira import shapes
from spira.rdd.technology import ProcessTree
from demo.pdks import ply
from spira.lpe.devices import Device
from spira.visualization import color
from copy import copy, deepcopy
from demo.pdks.process.mitll_pdk.database import RDD


class Via(Device):
    color = param.ColorField(default=color.COLOR_LIGHT_GRAY)

    # def create_ports(self, ports):
    #     """ Activate the edge ports to be used in
    #     the Device for metal connections. """

    #     for m in self.metals:
    #         for p in m.ports:
    #             if isinstance(p, spira.Term):
    #                 edgelayer = deepcopy(p.gdslayer)
    #                 edgelayer.datatype = 80
    #                 arrowlayer = deepcopy(p.gdslayer)
    #                 arrowlayer.datatype = 81
    #                 term = spira.Term(
    #                     name=p.name,
    #                     gdslayer=deepcopy(m.player.layer),
    #                     midpoint=deepcopy(p.midpoint),
    #                     orientation=deepcopy(p.orientation)+90,
    #                     reflection=p.reflection,
    #                     edgelayer=edgelayer,
    #                     arrowlayer=arrowlayer,
    #                     local_connect=p.local_connect,
    #                     width=p.width,
    #                 )

    #                 ports += term

    #     return ports


class ViaC5R(Via):
    """ Via component for the AIST process. """

    __name_prefix__ = 'C5R'

    w = param.FloatField(default=2*1e6)
    h = param.FloatField(default=2*1e6)

    m1 = param.PhysicalLayerField(default=RDD.PLAYER.R5)
    m2 = param.PhysicalLayerField(default=RDD.PLAYER.M6)
    cc = param.PhysicalLayerField(default=RDD.PLAYER.C5R)

    def create_metals(self, elems):
        elems += ply.Box(player=self.m1, center=(0,0), w=self.w, h=self.h)
        elems += ply.Box(player=self.m2, center=(0,0), w=self.w, h=self.h)
        return elems

    def create_contacts(self, elems):
        elems += ply.Box(player=self.cc, center=(0,0), w=RDD.C5R.MIN_SIZE*1e6, h=RDD.C5R.MIN_SIZE*1e6)
        return elems

    def create_ports(self, ports):
        ports += spira.Term(name='Input', midpoint=(-self.w/2, 0), orientation=90, width=self.w/2)
        ports += spira.Term(name='Output', midpoint=(self.w/2, 0), orientation=-90, width=self.w/2)
        ports += spira.Term(name='North', midpoint=(0, self.h/2), orientation=0, width=self.w/2)
        ports += spira.Term(name='South', midpoint=(0, -self.h/2), orientation=180, width=self.w/2)
        return ports


class ViaI5(Via):
    """ Via component for the AIST process. """

    __name_prefix__ = 'I5'

    w = param.FloatField(default=2*1e6)
    h = param.FloatField(default=2*1e6)

    m1 = param.PhysicalLayerField(default=RDD.PLAYER.M5)
    m2 = param.PhysicalLayerField(default=RDD.PLAYER.M6)
    cc = param.PhysicalLayerField(default=RDD.PLAYER.I5)

    def create_metals(self, elems):
        elems += ply.Box(player=self.m1, center=(0,0), w=self.w, h=self.h)
        elems += ply.Box(player=self.m2, center=(0,0), w=self.w, h=self.h)
        return elems

    def create_contacts(self, elems):
        elems += ply.Box(player=self.cc, center=(0,0), w=RDD.I5.MIN_SIZE*self.um, h=RDD.I5.MIN_SIZE*self.um)
        return elems

    def create_ports(self, ports):
        ports += spira.Term(name='Input', midpoint=(-self.w/2, 0), orientation=90, width=self.w/2)
        ports += spira.Term(name='Output', midpoint=(self.w/2, 0), orientation=-90, width=self.w/2)
        ports += spira.Term(name='North', midpoint=(0, self.h/2), orientation=0, width=self.w/2)
        ports += spira.Term(name='South', midpoint=(0, -self.h/2), orientation=180, width=self.w/2)
        return ports


class ViaI6(Via):
    """ Via component for the AIST process. """

    __name_prefix__ = 'I6'

    w = param.FloatField(default=2*1e6)
    h = param.FloatField(default=2*1e6)

    m1 = param.PhysicalLayerField(default=RDD.PLAYER.M6)
    m2 = param.PhysicalLayerField(default=RDD.PLAYER.M7)
    cc = param.PhysicalLayerField(default=RDD.PLAYER.I6)

    def create_metals(self, elems):
        elems += ply.Box(player=self.m1, center=(0,0), w=self.w, h=self.h)
        elems += ply.Box(player=self.m2, center=(0,0), w=self.w, h=self.h)
        return elems

    def create_contacts(self, elems):
        elems += ply.Box(player=self.cc, center=(0,0), w=RDD.I6.MIN_SIZE*self.um, h=RDD.I6.MIN_SIZE*self.um)
        return elems

    def create_ports(self, ports):
        ports += spira.Term(name='Input', midpoint=(-self.w/2, 0), orientation=90, width=self.w/2)
        ports += spira.Term(name='Output', midpoint=(self.w/2, 0), orientation=-90, width=self.w/2)
        ports += spira.Term(name='North', midpoint=(0, self.h/2), orientation=0, width=self.w/2)
        ports += spira.Term(name='South', midpoint=(0, -self.h/2), orientation=180, width=self.w/2)
        return ports


if __name__ == '__main__':

    name = 'Via PCell'
    spira.LOG.header('Running example: {}'.format(name))

    via = ViaBC()
    via.output(name=name)

    spira.LOG.end_print('Junction example finished')

