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


RDD = get_rule_deck()


class TIntersection(Circuit):

    um = param.FloatField(default=1e+6)
    num = param.IntegerField(default=2)
    dx = param.FloatField(default=100*1e+6)
    dy = param.FloatField(default=20*1e+6)

    pos = param.DataField(fdef_name='get_position')

    def get_position(self):
        return (self.dx/(self.num+1))

    def create_routes(self, routes):

        R1 = RouteManhattan(
            port1=self.term_ports['T1'],
            port2=self.term_ports['T2'],
            player=RDD.PLAYER.BAS
        )
        routes += spira.SRef(R1)

        R2 = RouteManhattan(
            port1=self.term_ports['D0'],
            port2=self.term_ports['T3'],
            player=RDD.PLAYER.BAS
        )
        routes += spira.SRef(R2)

        R3 = RouteManhattan(
            port1=self.term_ports['D1'],
            port2=self.term_ports['T4'],
            player=RDD.PLAYER.BAS
        )
        routes += spira.SRef(R3)

        return routes

    def create_elementals(self, elems):

        for r in self.routes:
            elems += r

        return elems

    def create_ports(self, ports):

        ports += spira.Term(
            name='T1',
            midpoint=[0, 0],
            orientation=-90
        )
        ports += spira.Term(
            name='T2',
            midpoint=[self.dx, 0],
            orientation=90
        )

        ports += spira.Term(
            name='T3',
            midpoint=[45*1e6, self.dy],
            width=10*1e6,
            orientation=180
        )
        ports += spira.Dummy(name='D0', midpoint=[45*1e6, 0*1e6], width=10*1e6, orientation=0)

        ports += spira.Term(
            name='T4',
            midpoint=[50*1e6, -self.dy],
            width=10*1e6,
            orientation=180
        )
        ports += spira.Dummy(name='D1', midpoint=[50*1e6, 0*1e6], width=10*1e6, orientation=0)

        return ports


if __name__ == '__main__':

    name = 'JTL PCell'
    spira.LOG.header('Running example: {}'.format(name))

    jj = TIntersection(num=3, level=2)

    jj.netlist
    jj.mask.output()

    spira.LOG.end_print('JTL example finished')



