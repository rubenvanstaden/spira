import spira
import numpy as np
from copy import copy, deepcopy
from spira import param, shapes
from spira.rdd import get_rule_deck
from demo.pdks.components.junction import Junction
from spira.lgm.route.manhattan_base import Route
from spira.lgm.route.basic import RouteShape, RouteBasic, Route
from spira.lpe.containers import __CellContainer__
from spira.lpe.circuits import Circuit


RDD = get_rule_deck()


class Jtl(Circuit):

    um = param.FloatField(default=1e+6)

    m1 = param.MidPointField(default=(0, 0))
    m2 = param.MidPointField(default=(50*1e6, 0*1e6))
    rotation = param.FloatField(default=0)

    jj1 = param.DataField(fdef_name='create_junction_one')
    jj2 = param.DataField(fdef_name='create_junction_two')

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

    def create_elementals(self, elems):
        elems += self.jj1
        elems += self.jj2

        for r in self.routes:
            elems += r

        return elems

    def create_terminal_routes(self):
        s1 = self.jj1
        s2 = self.jj2

        route = Route(
            port1=self.term_ports['T1'],
            port2=s1.ports['Input'],
            player=RDD.PLAYER.BAS
        )
        r1 = spira.SRef(route)

        route = Route(
            port1=self.term_ports['T2'],
            port2=s2.ports['Output'],
            player=RDD.PLAYER.BAS
        )
        r2 = spira.SRef(route)

        route = Route(
            port1=self.term_ports['T3'],
            port2=self.term_ports['D1'],
            player=RDD.PLAYER.BAS
        )
        r3 = spira.SRef(route)

        return [r1, r2, r3]

    def create_device_routes(self):
        s1 = self.jj1
        s2 = self.jj2

        R1 = Route(
            port1=s1.ports['Output'],
            port2=s2.ports['Input'],
            player=RDD.PLAYER.BAS
            # radius=3*self.um, length=1*self.um,
            # gdslayer=RDD.BAS.LAYER
        )
        r1 = spira.SRef(R1)

        return [r1]

    def create_routes(self, routes):

        routes += self.term_routes
        routes += self.device_routes

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
        ports += spira.Term(
            name='T3',
            midpoint=[25*1e6, 25*1e6],
            orientation=180
        )

        ports += spira.Dummy(name='D1', midpoint=[25*1e6, -1*1e6])

        return ports


if __name__ == '__main__':

    name = 'JTL PCell'
    spira.LOG.header('Running example: {}'.format(name))

    jj = Jtl(level=2)

    jj.netlist
    jj.mask.output()

    spira.LOG.end_print('JTL example finished')


