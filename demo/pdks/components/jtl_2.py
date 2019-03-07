import spira
import numpy as np
from copy import copy, deepcopy
from spira import param, shapes
from demo.pdks.components.junction import Junction
from spira.lgm.route.manhattan_base import Route
from spira.lpe.containers import __CellContainer__
from spira.lpe.circuits import Circuit


RDD = spira.get_rule_deck()


class Jtl(Circuit):

    um = param.FloatField(default=1e+6)

    m1 = param.MidPointField(default=(0, 0))
    m2 = param.MidPointField(default=(50*1e6, -50*1e6))
    m3 = param.MidPointField(default=(100*1e6, -100*1e6))
    rotation = param.FloatField(default=0)

    jj1 = param.DataField(fdef_name='create_junction_one')
    jj2 = param.DataField(fdef_name='create_junction_two')
    jj3 = param.DataField(fdef_name='create_junction_three')
    term_routes = param.DataField(fdef_name='create_terminal_routes')
    device_routes = param.DataField(fdef_name='create_device_routes')

    def create_junction_one(self):
        jj = Junction()
        jj.center = (0,0)
        return spira.SRef(jj, midpoint=self.m1, rotation=self.rotation)

    def create_junction_two(self):
        jj = Junction()
        jj.center = (0,0)
        return spira.SRef(jj, midpoint=self.m2, rotation=-self.rotation)

    def create_junction_three(self):
        jj = Junction()
        jj.center = (0,0)
        return spira.SRef(jj, midpoint=self.m3, rotation=-self.rotation)

    def create_elementals(self, elems):
        elems += self.jj1
        elems += self.jj2
        elems += self.jj3

        for r in self.routes:
            elems += r

        return elems

    def create_terminal_routes(self):
        s1 = self.jj1
        s3 = self.jj3

        route = Route(port1=self.term_ports['T1'], port2=s1.ports['Input'], player=RDD.PLAYER.BAS)
        r1 = spira.SRef(route)

        route = Route(port1=self.term_ports['T2'], port2=s3.ports['Output'], player=RDD.PLAYER.BAS)
        r2 = spira.SRef(route)

        return [r1, r2]

    def create_device_routes(self):
        s1 = self.jj1
        s2 = self.jj2
        s3 = self.jj3

        R1 = Route(port1=s1.ports['Output'], port2=s2.ports['Input'], radius=3*self.um, length=1*self.um, gdslayer=RDD.BAS.LAYER)
        r1 = spira.SRef(R1)
        r1.move(midpoint=r1.ports['T1'], destination=R1.port1)

        R2 = Route(port1=s2.ports['Output'], port2=s3.ports['Input'], radius=3*self.um, length=1*self.um, gdslayer=RDD.BAS.LAYER)
        r2 = spira.SRef(R2)
        r2.move(midpoint=r2.ports['T1'], destination=R2.port1)

        return [r1, r2]

    def create_routes(self, routes):

        routes += self.term_routes
        routes += self.device_routes

        return routes

    def create_ports(self, ports):

        m1 = self.jj1.ports['Input'] + [-10*self.um,0]
        m2 = self.jj3.ports['Output'] + [10*self.um,0]
        ports += spira.Term(name='T1', midpoint=m1, orientation=-90)
        ports += spira.Term(name='T2', midpoint=m2, orientation=90)

        return ports


if __name__ == '__main__':

    name = 'JTL PCell'
    spira.LOG.header('Running example: {}'.format(name))

    jj = Jtl(level=2)

    # jj.output()
    jj.netlist
    jj.mask.output()

    spira.LOG.end_print('JTL example finished')


