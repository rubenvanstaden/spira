import spira
from spira import param, shapes, io
from spira.lpe.circuits import Circuit
from demo.pdks.process.mitll_pdk.database import RDD
from spira.lgm.route.manhattan_base import Route

from demo.pdks.components.mitll.junction import Junction
from demo.pdks.components.mitll.via import ViaC5R, ViaI5
from spira.lpe.mask import Mask


class __Ports__(Circuit):

    p1 = param.DataField(fdef_name='create_p1')
    p2 = param.DataField(fdef_name='create_p2')
    p3 = param.DataField(fdef_name='create_p3')

    def create_p1(self):
        m = self.via_i5.ports['North'] + [0, 3*self.um]
        return spira.Term(name='P1', midpoint=m, orientation=180, width=1*self.um)

    def create_p2(self):
        m = self.jj1.ports['e1'] + [0, 3*self.um]
        return spira.Term(name='P2', midpoint=m, orientation=180, width=1*self.um)

    def create_p3(self):
        m = (10*self.um, -26.37*self.um)
        return spira.Term(name='P3', midpoint=m, orientation=90, width=1*self.um)


class __Devices__(__Ports__):

    jj1 = param.DataField(fdef_name='create_jj_100sg_top')
    jj2 = param.DataField(fdef_name='create_jj_100sg_left')
    jj3 = param.DataField(fdef_name='create_jj_100sg_right')

    via_c5r_1 = param.DataField(fdef_name='create_via_c5r_1')
    via_c5r_2 = param.DataField(fdef_name='create_via_c5r_2')
    via_i5 = param.DataField(fdef_name='create_via_i5')

    def create_jj_100sg_top(self):
        jj = Junction()
        m = (-5*self.um, -13.4*self.um)
        return spira.SRef(jj, midpoint=m, rotation=270)

    def create_jj_100sg_left(self):
        jj = Junction()
        m = (-5.11*self.um, -30.72*self.um)
        return spira.SRef(jj, midpoint=m, rotation=180)

    def create_jj_100sg_right(self):
        jj = Junction()
        m = (4.63*self.um, -30.45*self.um)
        return spira.SRef(jj, midpoint=m, rotation=180)

    def create_via_c5r_1(self):
        via = ViaC5R(w=2*1e6, h=1.4*1e6)
        return spira.SRef(via, midpoint=(5*self.um, -16*self.um), reflection=True)

    def create_via_c5r_2(self):
        via = ViaC5R(w=2*1e6, h=1.4*1e6)
        return spira.SRef(via, midpoint=(5*self.um, -8.75*self.um))

    def create_via_i5(self):
        via = ViaI5(w=2*1e6, h=1.4*1e6)
        s1 = spira.SRef(via)
        s1.connect(port=s1.ports['South'], destination=self.via_c5r_2.ports['North'])
        # s1.connect(port=s1.ports['e2'], destination=self.via_c5r_2.ports['North'])
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
            # port1=self.jj3.ports['East'],
            port1=self.jj3.ports['e1'],
            port2=self.p2,
            player=RDD.PLAYER.M6)
        r1 = spira.SRef(R1)
        return r1

    def create_connect_via1_to_via2(self):
        R1 = Route(
            port1=self.via_c5r_1.ports['North'],
            port2=self.via_c5r_2.ports['South'],
            # port1=self.via_c5r_1.ports['e2'],
            # port2=self.via_c5r_2.ports['e0'],
            player=RDD.PLAYER.R5)
        r1 = spira.SRef(R1)
        return r1

    def create_connect_via3_to_p3(self):
        # R1 = Route(port1=self.via_i5.ports['Output'], port2=self.p3, gdslayer=RDD.M5.LAYER)
        R1 = Route(port1=self.via_i5.ports['Output'], port2=self.p3, player=RDD.PLAYER.M5, radius=0.5*self.um)
        r1 = spira.SRef(R1)
        return r1

    def create_connect_j2_to_p1(self):
        R1 = Route(port1=self.jj2.ports['e2'], port2=self.p1, player=RDD.PLAYER.M6, radius=0.5*self.um)
        # R1 = Route(port1=self.jj2.ports['South'], port2=self.p1, player=RDD.PLAYER.M6, radius=0.5*self.um)
        r1 = spira.SRef(R1)
        return r1

    def create_connect_j1_to_j2(self):
        s1 = self.jj1
        s2 = self.jj2

        # t1 = s1.ports['West'].midpoint
        # t2 = s2.ports['West'].midpoint
        t1 = s1.ports['e3'].midpoint
        t2 = s2.ports['e3'].midpoint

        dx = t2[0]-t1[0]
        dy = t2[1]-t1[1]

        R1 = Route(
            # port1=s1.ports['West'],
            # port2=s2.ports['West'],
            port1=s1.ports['e3'],
            port2=s2.ports['e3'],
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

        # t1 = s1.ports['East'].midpoint
        t2 = s2.ports['Input'].midpoint
        t1 = s1.ports['e1'].midpoint
        # t2 = s2.ports['e0'].midpoint

        d1 = 1.8 * self.um
        d2 = 2.5 * self.um
        d3 = 1.4 * self.um
        d4 = 4.5 * self.um
        d5 = 1.3 * self.um
        d6 = 3.2 * self.um
        d7 = t2[1] - (t1[1] + d1 + d3 - d5)

        R1 = Route(
            # port1=s1.ports['East'],
            port2=s2.ports['Input'],
            port1=s1.ports['e1'],
            # port2=s2.ports['e0'],
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

        # t1 = s1.ports['West']
        t2 = s2.ports['Input']
        t1 = s1.ports['e3']
        # t2 = s2.ports['e0']

        p1 = spira.Term(name='D1', midpoint=(-9*self.um, -3.2*self.um), width=1*1e6, orientation=0)
        p2 = spira.Term(name='D2', midpoint=(-9*self.um, -3.2*self.um), width=1*1e6, orientation=180)

        R1 = Route(port1=t1, port2=p1, player=RDD.PLAYER.M6, radius=0.5*self.um)
        r1 = spira.SRef(R1)

        R2 = Route(port1=p2, port2=t2, player=RDD.PLAYER.M6, radius=0.5*self.um)
        r2 = spira.SRef(R2)

        return [r1, r2]


class Ptlrx(__Routes__):

    def create_structures(self, elems):
        elems += self.jj1
        elems += self.jj2
        elems += self.jj3
        elems += self.via_c5r_1
        elems += self.via_c5r_2
        elems += self.via_i5
        return elems

    def create_routes(self, routes):
        # routes += self.connect_j1_to_j2
        # routes += self.connect_j1_to_via1
        # routes += self.connect_via1_to_via2
        # routes += self.connect_j3_to_p2
        # routes += self.connect_j2_to_p1
        # routes += self.connect_via3_to_p3
        # routes += self.connect_j3_to_via1
        return routes

    def create_ports(self, ports):
        # ports = super().create_ports(ports)
        ports += self.p1
        ports += self.p2
        ports += self.p3
        return ports


if __name__ == '__main__':

    name = 'PtlRX PCell'
    spira.LOG.header('Running example: {}'.format(name))

    input_cell = Ptlrx(level=2)
    # input_cell.netlist
    # input_cell.output()

    mask = Mask(name=input_cell.name, cell=input_cell)
    # mask.netlist
    mask.output()

    spira.LOG.end_print('JTL example finished')


