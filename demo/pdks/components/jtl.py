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

    m1 = param.MidPointField(default=(0,0))
    m2 = param.MidPointField(default=(0,0))
    rotation = param.FloatField(default=0)
    # level = param.IntegerField(default=2)

    jj1 = param.DataField(fdef_name='create_junction_one')
    jj2 = param.DataField(fdef_name='create_junction_two')
    quadrant = param.DataField(fdef_name='create_quadrant')

    def create_quadrant(self):
        quadrant = None
        if (self.m2[1] > self.m1[1]) and (self.m2[0] > self.m1[0]):
            quadrant = 'Q1'
        if (self.m2[1] > self.m1[1]) and (self.m2[0] < self.m1[0]):
            quadrant = 'Q2'
        if (self.m2[1] < self.m1[1]) and (self.m2[0] < self.m1[0]):
            quadrant = 'Q3'
        if (self.m2[1] < self.m1[1]) and (self.m2[0] > self.m1[0]):
            quadrant = 'Q4'
        return quadrant

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

    def create_routes(self, routes):

        s1 = self.jj1
        s2 = self.jj2

        if self.quadrant in ['Q1', 'Q4']:
            route = RouteManhattan(
                port1=s1.ports['Output'],
                port2=s2.ports['Input'],
                radius=3*self.um, length=1*self.um,
                gdslayer=RDD.BAS.LAYER
            )
        if self.quadrant in ['Q2', 'Q3']:
            route = RouteManhattan(
                port1=s2.ports['Output'],
                port2=s1.ports['Input'],
                radius=3*self.um, length=1*self.um,
                gdslayer=RDD.BAS.LAYER
            )

        s3 = spira.SRef(route)
        s3.move(midpoint=s3.ports['T1'], destination=route.port1)
        routes += s3

        r1 = Route(
            port1=self.term_ports['T1'],
            port2=s1.ports['Input'],
            player=RDD.PLAYER.BAS
        )
        routes += spira.SRef(r1)

        r2 = Route(
            port1=s2.ports['Output'],
            port2=self.term_ports['T2'],
            player=RDD.PLAYER.BAS
        )
        routes += spira.SRef(r2)

        return routes

    def create_ports(self, ports):

        if self.quadrant in ['Q1', 'Q4']:
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

        if self.quadrant in ['Q2', 'Q3']:
            ports += spira.Term(
                name='T1',
                midpoint=self.jj1.ports['Input'] + [10*self.um,0],
                orientation=-90
            )
            ports += spira.Term(
                name='T2',
                midpoint=self.jj2.ports['Output'] + [-10*self.um,0],
                orientation=90
            )

        return ports


if __name__ == '__main__':

    name = 'JTL PCell'
    spira.LOG.header('Running example: {}'.format(name))

    jtl = spira.Cell(name='JTL')

    # jj_q1 = Jtl(m2=(30,30), rotation=0)
    # jj_q2 = Jtl(m2=(-30,30), rotation=0)
    # jj_q3 = Jtl(m2=(-30,-30), rotation=0)
    jj_q4 = Jtl(m2=(30*1e6,-30*1e6), rotation=0, level=2)

    # print(jj_q4.mask)

    jj_q4.netlist
    jj_q4.mask.output()

    # jj_q4.routes

    # jtl += spira.SRef(jj_q4)
    # jtl.output(name=name)

    # # layout = SLayout(cell=jj_q4, level=1)
    # layout = SLayout(cell=jj_q4, level=2)
    # layout.output(name=name)

    # # jtl += spira.SRef(jj_q1, midpoint=(0,0))
    # # jtl += spira.SRef(jj_q2, midpoint=(100,0))
    # # jtl += spira.SRef(jj_q3, midpoint=(100,0))
    # jtl += spira.SRef(jj_q4, midpoint=(100,0))
    # jtl.output(name=name)

    spira.LOG.end_print('JTL example finished')


