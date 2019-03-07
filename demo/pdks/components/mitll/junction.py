import spira
import numpy as np
from spira import param
from spira import shapes
from copy import deepcopy
from spira.rdd.technology import ProcessTree
from demo.pdks import ply
from spira.lpe.devices import Device
from spira.visualization import color
from demo.pdks.process.mitll_pdk.database import RDD


class Junction(Device):
    """ Josephon Junction component for the AIST process. """

    __name_prefix__ = 'Junction'

    color = param.ColorField(default=color.COLOR_PLUM)

    def create_metals(self, elems):
        elems += ply.Box(player=RDD.PLAYER.M5, center=(0*self.um, 2.55*self.um), w=2.3*self.um, h=7.4*self.um)
        elems += ply.Box(name='i5', player=RDD.PLAYER.M6, center=(0*self.um, 4.55*self.um), w=1.6*self.um, h=3.1*self.um)
        elems += ply.Box(player=RDD.PLAYER.R5, center=(0*self.um, 2.8*self.um), w=0.5*self.um, h=3.5*self.um)
        elems += ply.Box(name='jj', player=RDD.PLAYER.M6, center=(0*self.um, 0.775*self.um), w=2.0*self.um, h=3.55*self.um)
        return elems

    def create_contacts(self, elems):
        elems += ply.Box(player=RDD.PLAYER.C5R, center=(0*self.um, 3.86*self.um), w=0.9*self.um, h=0.7*self.um)
        elems += ply.Box(player=RDD.PLAYER.C5R, center=(0*self.um, 3.86*self.um), w=0.9*self.um, h=0.7*self.um)
        elems += ply.Box(player=RDD.PLAYER.C5R, center=(0*self.um, 1.74*self.um), w=0.9*self.um, h=0.7*self.um)
        # elems += ply.Box(player=RDD.PLAYER.C5J, center=(0*self.um, 1.74*self.um), w=0.9*self.um, h=0.7*self.um)
        elems += ply.Box(player=RDD.PLAYER.I5, center=(0*self.um, 5.4*self.um), w=0.7*self.um, h=0.7*self.um)
        elems += ply.Circle(player=RDD.PLAYER.J5, center=(0*self.um, 0*self.um), box_size=[1.3*self.um, 1.3*self.um])
        # elems += ply.Box(player=RDD.PLAYER.I4, center=(0*self.um, 2.8*self.um), w=1.0*self.um, h=1.0*self.um)
        return elems

    def create_ports(self, ports):
        """ Activate the edge ports to be used in
        the Device for metal connections. """

        for p in self.metals['jj'].ports:
            ports += p.modified_copy(name=p.name, width=1*self.um)

        return ports


class GJunction(Junction):
    """ Josephon Junction component for the AIST process. """

    __name_prefix__ = 'GroundedJunction'

    def create_contacts(self, elems):
        elems = super().create_contacts(elems)
        elems += ply.Box(player=RDD.PLAYER.I4, center=(0*self.um, 2.8*self.um), w=1.0*self.um, h=1.0*self.um)
        return elems


class SJunction(Junction):
    """ Josephon Junction component for the AIST process. """

    __name_prefix__ = 'SkyJunction'

    def create_contacts(self, elems):
        elems = super().create_contacts(elems)
        elems += ply.Box(player=RDD.PLAYER.I6, center=(0*self.um, 2.8*self.um), w=1.0*self.um, h=1.0*self.um)
        return elems


class SGJunction(Junction):
    """ Josephon Junction component for the AIST process. """

    __name_prefix__ = 'SkyGroundedJunction'

    def create_contacts(self, elems):
        elems = super().create_contacts(elems)
        elems += ply.Box(player=RDD.PLAYER.I4, center=(0*self.um, 2.8*self.um), w=1.0*self.um, h=1.0*self.um)
        elems += ply.Box(player=RDD.PLAYER.I6, center=(0*self.um, 2.8*self.um), w=1.0*self.um, h=1.0*self.um)
        return elems


if __name__ == '__main__':

    name = 'Junction PCell'
    spira.LOG.header('Running example: {}'.format(name))

    jj = Junction()

    # jj.center = (10*1e6,0)

    # cell = spira.Cell('Junction Test')
    # cell += spira.SRef(jj, midpoint=(0*1e6,0), rotation=0, reflection=True)
    # cell += spira.SRef(jj, midpoint=(20*1e6,0), rotation=90, reflection=True)
    # cell += spira.SRef(jj, midpoint=(40*1e6,0), rotation=180, reflection=True)
    # cell += spira.SRef(jj, midpoint=(60*1e6,0), rotation=270, reflection=True)
    # cell += spira.SRef(jj, midpoint=(80*1e6,0), rotation=360, reflection=True)

    # cell += spira.SRef(jj, midpoint=(0*1e6,-20*1e6), rotation=0)
    # cell += spira.SRef(jj, midpoint=(20*1e6,-20*1e6), rotation=90)
    # cell += spira.SRef(jj, midpoint=(40*1e6,-20*1e6), rotation=180)
    # cell += spira.SRef(jj, midpoint=(60*1e6,-20*1e6), rotation=270)
    # cell += spira.SRef(jj, midpoint=(80*1e6,-20*1e6), rotation=360)

    jj.netlist
    jj.output()

    # cell.output(name=name)

    spira.LOG.end_print('Junction example finished')








