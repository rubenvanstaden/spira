import spira
from spira import param, shapes
from spira.lpe.circuits import Circuit
from demo.pdks.process.mitll_pdk.database import RDD
from spira.lgm.route.manhattan_base import Route

from demo.pdks.components.mitll.junction import Junction
from demo.pdks.components.mitll.via import ViaC5R, ViaI5


class __Ports__(Circuit):

    um = param.FloatField(default=1e+6)

    p1 = param.DataField(fdef_name='create_p1')
    p2 = param.DataField(fdef_name='create_p2')
    p3 = param.DataField(fdef_name='create_p3')

    def create_p1(self):
        return spira.Term(
            name='P1', 
            midpoint=(10*self.um, -5*self.um), 
            orientation=90, 
            width=1*self.um
        )

    def create_p2(self):
        return spira.Term(
            name='P2', 
            midpoint=self.jj3.ports['East']+[0,3*self.um],
            orientation=180, 
            width=1*self.um
        )

    def create_p3(self):
        return spira.Term(
            name='P3', 
            midpoint=(7*self.um, 10*self.um), 
            orientation=180, 
            width=1*self.um
        )


class __Devices__(__Ports__):

    jj1 = param.DataField(fdef_name='create_junction_one')
    jj2 = param.DataField(fdef_name='create_junction_two')
    jj3 = param.DataField(fdef_name='create_junction_three')
    via_c5r_1 = param.DataField(fdef_name='create_via_c5r_1')
    via_c5r_2 = param.DataField(fdef_name='create_via_c5r_2')
    via_i5 = param.DataField(fdef_name='create_via_i5')

    def create_junction_one(self):
        jj = Junction()
        jj.center = (0,0)
        jj.rotate(angle=180)
        return spira.SRef(jj, midpoint=(-3*self.um, -9*self.um), rotation=90)

    def create_junction_two(self):
        jj = Junction()
        jj.center = (0,0)
        jj.rotate(angle=180)
        return spira.SRef(jj, midpoint=(7*self.um, -13*self.um), rotation=0)

    def create_junction_three(self):
        jj = Junction()
        jj.center = (0,0)
        jj.rotate(angle=180)
        return spira.SRef(jj, midpoint=(-3*self.um, 2*self.um), rotation=90)

    def create_via_c5r_1(self):
        via = ViaC5R(w=2*1e6, h=1.4*1e6)
        via.center = (0,0)
        return spira.SRef(via, midpoint=(3.6*self.um, -3.4*self.um))

    def create_via_c5r_2(self):
        via = ViaC5R(w=2*1e6, h=1.4*1e6)
        via.center = (0,0)
        return spira.SRef(via, midpoint=(3.6*self.um, 6*self.um))

    def create_via_i5(self):
        via = ViaI5(w=2*1e6, h=1.4*1e6)
        via.center = (0,0)
        s1 = spira.SRef(via, midpoint=(3.6*self.um, 8*self.um))
        s1.connect(port=s1.ports['South'], destination=self.via_c5r_2.ports['North'])
        return s1


class __Routes__(__Devices__):

    connect_j1_to_j2 = param.DataField(fdef_name='create_connect_j1_to_j2')
    connect_j1_to_via1 = param.DataField(fdef_name='create_connect_j1_to_via1')
    connect_j3_to_via1 = param.DataField(fdef_name='create_connect_j3_to_via1')
    connect_j2_to_p1 = param.DataField(fdef_name='create_connect_j2_to_p1')
    connect_via1_to_via2 = param.DataField(fdef_name='create_connect_via1_to_via2')
    connect_j3_to_p2 = param.DataField(fdef_name='create_connect_j3_to_p2')
    connect_via3_to_p3 = param.DataField(fdef_name='create_connect_via3_to_p3')

    def create_connect_j3_to_p2(self):
        R1 = Route(
            port1=self.jj3.ports['East'],
            port2=self.p2,
            player=RDD.PLAYER.M6)
        r1 = spira.SRef(R1)
        return r1

    def create_connect_via1_to_via2(self):
        R1 = Route(
            port1=self.via_c5r_1.ports['North'],
            port2=self.via_c5r_2.ports['South'],
            player=RDD.PLAYER.R5)
        r1 = spira.SRef(R1)
        return r1

    def create_connect_via3_to_p3(self):
        R1 = Route(port1=self.via_i5.ports['Output'], port2=self.p3, gdslayer=RDD.M5.LAYER)
        r1 = spira.SRef(R1)
        return r1

    def create_connect_j2_to_p1(self):
        R1 = Route(port1=self.jj2.ports['South'], port2=self.p1, gdslayer=RDD.M6.LAYER)
        r1 = spira.SRef(R1)
        return r1

    def create_connect_j1_to_j2(self):
        s1 = self.jj1
        s2 = self.jj2

        t1 = s1.ports['West'].midpoint
        t2 = s2.ports['West'].midpoint

        dx = t2[0]-t1[0]
        dy = t2[1]-t1[1]

        R1 = Route(
            port1=s1.ports['West'],
            port2=s2.ports['West'],
            path=[t1,
                (t1[0], t1[1]-5*1e6),
                (t1[0]+dx-1.5*1e6, t1[1]-5*1e6),
                (t1[0]+dx-1.5*1e6, t1[1]+dy),
                t2],
            width=1*1e6,
            player=RDD.PLAYER.M6
        )
        r1 = spira.SRef(R1)
        return r1

    def create_connect_j1_to_via1(self):
        s1 = self.jj1
        s2 = self.via_c5r_1

        t1 = s1.ports['East'].midpoint
        t2 = s2.ports['Input'].midpoint

        d1 = 1.8 * self.um
        d2 = 2.5 * self.um
        d3 = 1.4 * self.um
        d4 = 4.5 * self.um
        d5 = 1.3 * self.um
        d6 = 3.2 * self.um
        d7 = t2[1] - (t1[1] + d1 + d3 - d5)

        R1 = Route(
            port1=s1.ports['East'],
            port2=s2.ports['Input'],
            path=[
                t1,
                (t1[0], t1[1] + d1),
                (t1[0] - d2, t1[1] + d1),
                (t1[0] - d2, t1[1] + d1 + d3),
                (t1[0] - d2 + d4, t1[1] + d1 + d3),
                (t1[0] - d2 + d4, t1[1] + d1 + d3 - d5),
                (t1[0] - d2 + d4 + d6, t1[1] + d1 + d3 - d5),
                (t1[0] - d2 + d4 + d6, t1[1] + d1 + d3 - d5 + d7),
                t2
            ],
            width=1*1e6,
            player=RDD.PLAYER.M6
        )
        r1 = spira.SRef(R1)
        return r1

    def create_connect_j3_to_via1(self):
        s1 = self.jj3
        s2 = self.via_c5r_1

        t1 = s1.ports['West']
        t2 = s2.ports['Input']

        p1 = spira.Term(name='D1', midpoint=(-8.3*self.um, -1.8*self.um), width=1*1e6, orientation=0)
        p2 = spira.Term(name='D1', midpoint=(-8.3*self.um, -1.8*self.um), width=1*1e6, orientation=180)

        R1 = Route(port1=t1, port2=p1, gdslayer=RDD.M6.LAYER)
        r1 = spira.SRef(R1)

        R2 = Route(port1=p2, port2=t2, gdslayer=RDD.M6.LAYER)
        r2 = spira.SRef(R2)

        return [r1, r2]


class Ptlrx(__Routes__):

    def create_elementals(self, elems):

        elems += self.jj1
        elems += self.jj2
        elems += self.jj3

        elems += self.via_c5r_1
        elems += self.via_c5r_2
        elems += self.via_i5

        for r in self.routes:
            elems += r

        return elems

    def create_routes(self, routes):

        routes += self.connect_j1_to_j2
        routes += self.connect_j1_to_via1
        routes += self.connect_j3_to_via1
        routes += self.connect_j2_to_p1
        routes += self.connect_via1_to_via2
        routes += self.connect_j3_to_p2
        routes += self.connect_via3_to_p3

        return routes

    def create_ports(self, ports):
        ports += self.p1
        ports += self.p2
        ports += self.p3
        return ports


if __name__ == '__main__':

    name = 'PtlRX PCell'
    spira.LOG.header('Running example: {}'.format(name))

    c = Ptlrx(level=2)
    # c.output()

    # c.netlist
    c.mask.output()

    spira.LOG.end_print('JTL example finished')


