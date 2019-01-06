import spira
from spira import param
from spira import shapes
from spira.rdd import get_rule_deck
from spira.rdd.technology import ProcessTree
from demo.pdks import ply


RDD = get_rule_deck()


class Junction(spira.Cell):
    """ Josephon Junction component for the AIST process. """

    metals = param.DataField(fdef_name='create_metal_layers')
    contacts = param.DataField(fdef_name='create_contact_layers')

    def create_metal_layers(self):
        metals = spira.ElementList()
        metals += ply.Box(player=RDD.PLAYER.COU, center=(1.95, 5.76), w=1.9, h=6.7)
        metals += ply.Box(player=RDD.PLAYER.BAS, center=(1.95, 2.6), w=3.9, h=5.2)
        metals += ply.Box(player=RDD.PLAYER.BAS, center=(1.95, 7.7), w=1.9, h=2.8)
        metals += ply.Box(player=RDD.PLAYER.RES, center=(1.95, 7.2), w=1.5, h=1.5)
        metals += ply.Box(player=RDD.PLAYER.RES, center=(1.95, 5.76), w=1.5, h=2.0)
        metals += ply.Box(player=RDD.PLAYER.RES, center=(1.95, 3.55), w=3.4, h=2.8)
        return metals

    def create_contact_layers(self):
        elems = spira.ElementList()
        elems += ply.Box(player=RDD.PLAYER.GC, center=(1.95, 1.1), w=2.9, h=1.2)
        elems += ply.Box(player=RDD.PLAYER.BC, center=(1.95, 8.5), w=1.4, h=1.0)
        elems += ply.Box(player=RDD.PLAYER.RC, center=(1.95, 7.2), w=0.9, h=1.0)
        elems += ply.Box(player=RDD.PLAYER.RC, center=(1.95, 3.55), w=2.9, h=2.3)
        elems += ply.Box(player=RDD.PLAYER.JC, center=(1.95, 3.55), w=1.4, h=1.0)
        elems += ply.Box(player=RDD.PLAYER.JJ, center=(1.95, 3.55), w=1.9, h=1.3)
        return elems

    def create_elementals(self, elems):
        if len(elems) == 0:
            for e in self.metals:
                elems += e
            for e in self.contacts:
                elems += e

        for key in RDD.VIAS.keys:
            RDD.VIAS[key].PCELL.create_elementals(elems)

        return elems

    def create_ports(self, ports):
        ports += spira.Term(name='Input', midpoint=(3.6, 3.5), orientation=180)
        ports += spira.Term(name='Output', midpoint=(0.25, 3.5), width=1)
        return ports


if __name__ == '__main__':

    name = 'Junction PCell'
    spira.LOG.header('Running example: {}'.format(name))

    jj = Junction()
    jj.output(name=name)

    spira.LOG.end_print('Junction example finished')








