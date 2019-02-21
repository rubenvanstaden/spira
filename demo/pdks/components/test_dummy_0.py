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


class TIntersection(Circuit):

    um = param.FloatField(default=1e+6)
    num = param.IntegerField(default=2)
    dx = param.FloatField(default=100*1e+6)
    dy = param.FloatField(default=10*1e+6)

    pos = param.DataField(fdef_name='get_position')

    def get_position(self):
        return (self.dx/(self.num+1))

    def create_routes(self, routes):

        R1 = Route(
            port1=self.term_ports['T1'],
            port2=self.term_ports['T2'],
            player=RDD.PLAYER.BAS
        )
        routes += spira.SRef(R1)

        for i in range(self.num):
            R2 = Route(
                port1=self.term_ports['T{}'.format(i+3)],
                port2=self.term_ports['D{}'.format(i)],
                player=RDD.PLAYER.BAS
            )
            routes += spira.SRef(R2)

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

        for i in range(self.num):
            ports += spira.Term(name='T{}'.format(i+3), midpoint=[(i+1)*self.pos, self.dy], orientation=180)
            ports += spira.Dummy(name='D{}'.format(i), midpoint=[(i+1)*self.pos, 0])

        return ports


if __name__ == '__main__':

    import time
    start = time.time()

    name = 'JTL PCell'
    spira.LOG.header('Running example: {}'.format(name))

    jj = TIntersection(num=1, level=2)

    jj.netlist
    jj.mask.output()

    spira.LOG.end_print('JTL example finished')

    end = time.time()
    print(end - start)


