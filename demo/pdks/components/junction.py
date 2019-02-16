import spira
from spira import param
from spira import shapes
from spira.rdd.technology import ProcessTree
from demo.pdks import ply
from spira.lpe.devices import Device


RDD = spira.get_rule_deck()


class Junction(Device):
    """ Josephon Junction component for the AIST process. """

    um = param.FloatField(default=1e+6)

    def create_metals(self, elems):
        elems += ply.Box(player=RDD.PLAYER.COU, center=(1.95*self.um, 5.76*self.um), w=1.9*self.um, h=6.7*self.um)
        elems += ply.Box(player=RDD.PLAYER.BAS, center=(1.95*self.um, 2.6*self.um), w=3.9*self.um, h=5.2*self.um)
        elems += ply.Box(player=RDD.PLAYER.BAS, center=(1.95*self.um, 7.7*self.um), w=1.9*self.um, h=2.8*self.um)
        elems += ply.Box(player=RDD.PLAYER.RES, center=(1.95*self.um, 7.2*self.um), w=1.5*self.um, h=1.5*self.um)
        elems += ply.Box(player=RDD.PLAYER.RES, center=(1.95*self.um, 5.76*self.um), w=1.5*self.um, h=2.0*self.um)
        elems += ply.Box(player=RDD.PLAYER.RES, center=(1.95*self.um, 3.55*self.um), w=3.4*self.um, h=2.8*self.um)
        return elems

    def create_contacts(self, elems):
        elems += ply.Box(player=RDD.PLAYER.GC, center=(1.95*self.um, 1.1*self.um), w=2.9*self.um, h=1.2*self.um)
        elems += ply.Box(player=RDD.PLAYER.BC, center=(1.95*self.um, 8.5*self.um), w=1.4*self.um, h=1.0*self.um)
        elems += ply.Box(player=RDD.PLAYER.RC, center=(1.95*self.um, 7.2*self.um), w=0.9*self.um, h=1.0*self.um)
        elems += ply.Box(player=RDD.PLAYER.RC, center=(1.95*self.um, 3.55*self.um), w=2.9*self.um, h=2.3*self.um)
        elems += ply.Box(player=RDD.PLAYER.JC, center=(1.95*self.um, 3.55*self.um), w=1.4*self.um, h=1.0*self.um)
        elems += ply.Box(player=RDD.PLAYER.JJ, center=(1.95*self.um, 3.55*self.um), w=1.9*self.um, h=1.3*self.um)
        return elems

    def create_ports(self, ports):
        # ports += spira.Term(name='Input', midpoint=(0.25*self.um, 3.5*self.um), orientation=90, width=2*self.um)
        # ports += spira.Term(name='Output', midpoint=(3.6*self.um, 3.5*self.um), orientation=-90)
        return ports


if __name__ == '__main__':

    name = 'Junction PCell'
    spira.LOG.header('Running example: {}'.format(name))

    jj = Junction()

    jj.center = (0,0)

    cell = spira.Cell('Junction Test')
    cell += spira.SRef(jj, midpoint=(0*1e6,0), rotation=0, reflection=True)
    cell += spira.SRef(jj, midpoint=(20*1e6,0), rotation=90, reflection=True)
    cell += spira.SRef(jj, midpoint=(40*1e6,0), rotation=180, reflection=True)
    cell += spira.SRef(jj, midpoint=(60*1e6,0), rotation=270, reflection=True)
    cell += spira.SRef(jj, midpoint=(80*1e6,0), rotation=360, reflection=True)

    cell += spira.SRef(jj, midpoint=(0*1e6,-20*1e6), rotation=0)
    cell += spira.SRef(jj, midpoint=(20*1e6,-20*1e6), rotation=90)
    cell += spira.SRef(jj, midpoint=(40*1e6,-20*1e6), rotation=180)
    cell += spira.SRef(jj, midpoint=(60*1e6,-20*1e6), rotation=270)
    cell += spira.SRef(jj, midpoint=(80*1e6,-20*1e6), rotation=360)

    cell.output(name=name)

    spira.LOG.end_print('Junction example finished')








