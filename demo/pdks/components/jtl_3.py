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
    rotation = param.FloatField(default=0)

    jj = param.DataField(fdef_name='create_junction')

    def create_junction(self):
        elems = spira.ElementList()
        jj = Junction()
        jj.center = (0,0)

        for i in range(0, 10, 1):
            elems += spira.SRef(jj, midpoint=(20*i*self.um, 0))

        return elems

    def create_elementals(self, elems):
        for e in self.jj:
            elems += e
        for r in self.routes:
            elems += r
        return elems

    def create_routes(self, routes):

        junctions = self.jj

        for i in range(len(junctions)-1):
            s1 = junctions[i]
            s2 = junctions[i+1]

            R1 = Route(
                port1=s1.ports['Output'],
                port2=s2.ports['Input'],
                player=RDD.PLAYER.BAS
            )
            r1 = spira.SRef(R1)
            routes += r1

        R2 = Route(
            port1=self.term_ports['T1'],
            port2=self.jj[0].ports['Input'],
            player=RDD.PLAYER.BAS
        )
        routes += spira.SRef(R2)

        R3 = Route(
            port1=self.jj[-1].ports['Output'],
            port2=self.term_ports['T2'],
            player=RDD.PLAYER.BAS
        )
        routes += spira.SRef(R3)

        return routes

    def create_ports(self, ports):

        ports += spira.Term(
            name='T1',
            midpoint=self.jj[0].ports['Input'] + [-10*self.um,0],
            orientation=-90
        )
        ports += spira.Term(
            name='T2',
            midpoint=self.jj[-1].ports['Output'] + [10*self.um,0],
            orientation=90
        )

        return ports


if __name__ == '__main__':

    import time
    start = time.time()

    name = 'JTL PCell'
    spira.LOG.header('Running example: {}'.format(name))

    jj = Jtl(level=2)

    # jj.output()
    jj.netlist
    # jj.mask.output()

    spira.LOG.end_print('JTL example finished')

    end = time.time()
    print(end - start)

