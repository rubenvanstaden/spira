import spira
from spira import param
from spira import shapes
from copy import deepcopy
from spira.rdd.technology import ProcessTree
from demo.pdks import ply
from spira.lpe.devices import Device
from demo.pdks.process.mitll_pdk.database import RDD


class Junction(Device):
    """ Josephon Junction component for the AIST process. """

    # connectors = param.ElementalListField()

    um = param.FloatField(default=1e+6)

    # def create_connectors(self, elems):
    #     return elems

    def create_metals(self, elems):
        elems += ply.Box(player=RDD.PLAYER.M5, center=(0*self.um, 2.55*self.um), w=2.3*self.um, h=7.4*self.um)
        elems += ply.Box(player=RDD.PLAYER.M6, center=(0*self.um, 4.55*self.um), w=1.6*self.um, h=3.1*self.um)
        elems += ply.Box(player=RDD.PLAYER.R5, center=(0*self.um, 2.8*self.um), w=0.5*self.um, h=3.5*self.um)
        elems += ply.Box(player=RDD.PLAYER.M6, center=(0*self.um, 0.775*self.um), w=2.0*self.um, h=3.55*self.um)

        # for e in self.connectors:
        #     elems += e

        return elems

    def create_contacts(self, elems):
        elems += ply.Box(player=RDD.PLAYER.C5R, center=(0*self.um, 3.86*self.um), w=0.9*self.um, h=0.7*self.um)
        elems += ply.Box(player=RDD.PLAYER.C5R, center=(0*self.um, 1.74*self.um), w=0.9*self.um, h=0.7*self.um)
        elems += ply.Box(player=RDD.PLAYER.I5, center=(0*self.um, 5.4*self.um), w=0.7*self.um, h=0.7*self.um)
        elems += ply.Box(player=RDD.PLAYER.I4, center=(0*self.um, 2.8*self.um), w=1.0*self.um, h=1.0*self.um)
        elems += ply.Circle(player=RDD.PLAYER.C5J, center=(0*self.um, 0*self.um), box_size=[1.0*self.um, 1.0*self.um])
        elems += ply.Circle(player=RDD.PLAYER.J5, center=(0*self.um, 0*self.um), box_size=[1.3*self.um, 1.3*self.um])
        return elems

    def create_ports(self, ports):
        """ Activate the edge ports to be used in
        the Device for metal connections. """
        for i, m in enumerate(self.metals):
            for j, p in enumerate(m.ports):
                layer = deepcopy(m.layer)
                layer.datatype = 80
                if isinstance(p, spira.Term):
                    name='P{}{}_{}'.format(i, j, m.player.layer.name)
                    ports += spira.Term(
                        name=name,
                        midpoint=p.midpoint,
                        orientation=p.orientation,
                        edgelayer=layer,
                        width=p.width,
                        length=p.length
                    )
                    # ports += p.modified_copy(
                    #     name=name,
                    #     edgelayer=layer
                    # )

        # # for m in self.metals:
        # #     for p in m.ports:
        # #         if p.name == 'West':
        # #             ports += p.modified_copy(
        # #                 name='P1',
        # #                 edgelayer=spira.Layer(number=80)
        # #             )
        # #         if p.name == 'East':
        # #             ports += p.modified_copy(
        # #                 name='P2',
        # #                 edgelayer=spira.Layer(number=80)
        # #             )

        # ports += spira.Term(name='Input', midpoint=(-1.0*self.um, 0.8*self.um), orientation=90, width=2*self.um)
        # ports += spira.Term(name='Output', midpoint=(1.0*self.um, 0.8*self.um), orientation=-90, width=2*self.um)

        return ports


if __name__ == '__main__':

    name = 'Junction PCell'
    spira.LOG.header('Running example: {}'.format(name))

    jj = Junction()

    jj.output(name=name)
    # jj.netlist

    # -------------------- Add to Unit Testing ----------------------------

    # cell = spira.Cell('Junction Test')

    # cell += spira.SRef(jj, midpoint=(50*1e6,0), rotation=0, reflection=True)
    # cell += spira.SRef(jj, midpoint=(50*1e6,0), rotation=90, reflection=True)
    # cell += spira.SRef(jj, midpoint=(50*1e6,0), rotation=180, reflection=True)
    # cell += spira.SRef(jj, midpoint=(50*1e6,0), rotation=270, reflection=True)
    # cell += spira.SRef(jj, midpoint=(50*1e6,0), rotation=360, reflection=True)

    # cell += spira.SRef(jj, midpoint=(50*1e6,0), rotation=0)
    # cell += spira.SRef(jj, midpoint=(50*1e6,0), rotation=90)
    # cell += spira.SRef(jj, midpoint=(50*1e6,0), rotation=180)
    # cell += spira.SRef(jj, midpoint=(50*1e6,0), rotation=270)
    # cell += spira.SRef(jj, midpoint=(50*1e6,0), rotation=360)

    # cell.output(name=name)

    spira.LOG.end_print('Junction example finished')








