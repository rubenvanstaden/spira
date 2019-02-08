import spira
import numpy as np
from copy import copy, deepcopy
from spira import param, shapes
from spira.rdd import get_rule_deck
from demo.pdks.components.junction import Junction
from spira.lgm.route.manhattan_base import RouteManhattan
from spira.lgm.route.basic import RouteShape, RouteBasic, Route
from spira.lpe.primitives import SLayout
from spira.lpe.containers import __CellContainer__
from spira.lpe.circuits import Circuit


RDD = get_rule_deck()


class Jtl(Circuit):

    um = param.FloatField(default=1e+6)
    rotation = param.FloatField(default=0)

    jj = param.DataField(fdef_name='create_junction')
    # term_routes = param.DataField(fdef_name='create_terminal_routes')
    # device_routes = param.DataField(fdef_name='create_device_routes')

    def create_junction(self):
        elems = spira.ElementList()
        jj = Junction()
        jj.center = (0,0)

        for i in range(0, 50, 1):
            elems += spira.SRef(jj, midpoint=(20*i*self.um, 0))
            # elems += spira.SRef(jj, midpoint=(20*i*self.um, -20*i*self.um))

        return elems

    def create_elementals(self, elems):
        # for i in range(0, 100, 20):
        #     elems += spira.SRef(self.jj, midpoint=(i*self.um, 0))

        for e in self.jj:
            elems += e

        # for r in self.routes:
        #     elems += r

        return elems

    # def create_terminal_routes(self):
    #     s1 = self.jj1
    #     s3 = self.jj3

    #     route = Route(
    #         port1=self.term_ports['T1'],
    #         port2=s1.ports['Input'],
    #         player=RDD.PLAYER.BAS
    #     )
    #     r1 = spira.SRef(route)

    #     route = Route(
    #         port1=self.term_ports['T2'],
    #         port2=s3.ports['Output'],
    #         player=RDD.PLAYER.BAS
    #     )
    #     r2 = spira.SRef(route)

    #     return [r1, r2]

    # def create_device_routes(self):
        

    #     s1 = self.jj1
    #     s2 = self.jj2
    #     s3 = self.jj3

    #     R1 = RouteManhattan(
    #         port1=s1.ports['Output'],
    #         port2=s2.ports['Input'],
    #         radius=3*self.um, length=1*self.um,
    #         gdslayer=RDD.BAS.LAYER
    #     )
    #     r1 = spira.SRef(R1)
    #     r1.move(midpoint=r1.ports['T1'], destination=R1.port1)

    #     R2 = RouteManhattan(
    #         port1=s2.ports['Output'],
    #         port2=s3.ports['Input'],
    #         radius=3*self.um, length=1*self.um,
    #         gdslayer=RDD.BAS.LAYER
    #     )
    #     r2 = spira.SRef(R2)
    #     r2.move(midpoint=r2.ports['T1'], destination=R2.port1)

    #     return [r1, r2]

    def create_routes(self, routes):

        # for i in range(0, 100, 20):
        #     D = spira.SRef(self.jj, midpoint=(i*self.um, 0))

        junctions = self.jj

        # for i in range(len(junctions)-1):
        #     s1 = junctions[i]
        #     s2 = junctions[i+1]

        #     R1 = RouteManhattan(
        #         port1=s1.ports['Output'],
        #         port2=s2.ports['Input'],
        #         radius=3*self.um, length=1*self.um,
        #         gdslayer=RDD.BAS.LAYER
        #     )
        #     r1 = spira.SRef(R1)
        #     r1.move(midpoint=r1.ports['T1'], destination=R1.port1)
        #     routes += r1

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



        # routes += self.term_routes
        # routes += self.device_routes

        # for r in self.term_routes:
        #     routes += r
        # for r in self.device_routes:
        #     routes += r

        return routes

    # def create_ports(self, ports):

    #     ports += spira.Term(
    #         name='T1',
    #         midpoint=self.jj1.ports['Input'] + [-10*self.um,0],
    #         orientation=-90
    #     )
    #     ports += spira.Term(
    #         name='T2',
    #         midpoint=self.jj3.ports['Output'] + [10*self.um,0],
    #         orientation=90
    #     )

    #     return ports


if __name__ == '__main__':

    name = 'JTL PCell'
    spira.LOG.header('Running example: {}'.format(name))

    jj = Jtl(level=2)

    print(jj.routes)

    # jj.output()
    # jj.netlist
    jj.mask.output()

    spira.LOG.end_print('JTL example finished')


