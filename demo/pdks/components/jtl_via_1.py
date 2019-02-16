import spira
import numpy as np
from copy import copy, deepcopy
from spira import param, shapes
from spira.rdd import get_rule_deck
from demo.pdks.components.junction import Junction
from spira.lgm.route.manhattan_base import RouteManhattan
from spira.lgm.route.basic import RouteShape, RouteBasic, Route
from spira.lpe.containers import __CellContainer__
from spira.lpe.circuits import Circuit
from demo.pdks.components.via import ViaBC


RDD = get_rule_deck()


class JtlVia(Circuit):

    um = param.FloatField(default=1e+6)

    m1 = param.MidPointField(default=(0,0))
    m2 = param.MidPointField(default=(0,0))
    # m3 = param.MidPointField(default=(0,0))
    dx = param.FloatField(default=10*1e6)
    rotation = param.FloatField(default=0)

    jj1 = param.DataField(fdef_name='create_junction_one')
    jj2 = param.DataField(fdef_name='create_junction_two')

    via = param.DataField(fdef_name='create_via')
    via2 = param.DataField(fdef_name='create_via_two')

    def create_junction_one(self):
        jj = Junction()
        jj.center = (0,0)
        return spira.SRef(jj, midpoint=self.m1, rotation=self.rotation)

    def create_junction_two(self):
        jj = Junction()
        jj.center = (0,0)
        return spira.SRef(jj, midpoint=self.m2, rotation=-self.rotation)

    def create_via(self):
        via = ViaBC()
        via.center = (0,0)
        midpoint = np.array(self.jj1.ports['Output'].midpoint) + np.array([self.dx, 0])
        return spira.SRef(via, midpoint=midpoint)

    def create_via_two(self):
        via = ViaBC()
        via.center = (0,0)
        midpoint = np.array(self.jj1.ports['Output'].midpoint) + np.array([2*self.dx, -2*self.dx])
        return spira.SRef(via, midpoint=midpoint, rotation=-90)

    def create_elementals(self, elems):
        elems += self.jj1
        elems += self.jj2
        elems += self.via
        elems += self.via2

        for r in self.routes:
            elems += r

        return elems

    def create_routes(self, routes):

        s1 = self.jj1
        s2 = self.jj2

        R0 = RouteManhattan(
            port1=self.via.ports['Output'],
            port2=self.via2.ports['Input'],
            radius=3*self.um, length=1*self.um,
            gdslayer=RDD.BAS.LAYER
        )
        s3 = spira.SRef(R0)
        routes += s3

        R1 = RouteManhattan(
            port1=self.via2.ports['Output'],
            port2=s2.ports['Input'],
            radius=3*self.um, length=1*self.um,
            gdslayer=RDD.BAS.LAYER
        )
        r4 = spira.SRef(R1)
        routes += r4

        R2 = RouteManhattan(
            port1=s1.ports['Output'],
            port2=self.via.ports['Input'],
            player=RDD.PLAYER.COU
        )
        routes += spira.SRef(R2)

        r1 = RouteManhattan(
            port1=self.term_ports['T1'],
            port2=s1.ports['Input'],
            player=RDD.PLAYER.BAS
        )
        routes += spira.SRef(r1)

        r2 = RouteManhattan(
            port1=self.term_ports['T2'],
            port2=s2.ports['Output'],
            player=RDD.PLAYER.BAS
        )
        routes += spira.SRef(r2)

        return routes

    def create_ports(self, ports):

        ports += spira.Term(
            name='T1',
            midpoint=self.jj1.ports['Input'] + [-10*self.um,0],
            orientation=-90
        )
        ports += spira.Term(
            name='T2',
            midpoint=self.jj2.ports['Output'] + [10*self.um,0],
            orientation=90
        )

        return ports


if __name__ == '__main__':

    name = 'JTL with a Via connection.'
    spira.LOG.header('Running example: {}'.format(name))

    jtl = JtlVia(m2=(50*1e6,-50*1e6), rotation=0, level=2)

    jtl.netlist
    jtl.mask.output()

    spira.LOG.end_print('JTL example finished')



