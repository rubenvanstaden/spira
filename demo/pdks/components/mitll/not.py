import spira
from spira import param, shapes, io
from spira.lpe.circuits import Circuit
from demo.pdks.process.mitll_pdk.database import RDD
from spira.lgm.route.manhattan_base import Route

from demo.pdks.components.mitll.junction import Junction
from demo.pdks.components.mitll.via import ViaC5R, ViaI5
from demo.pdks.components.mitll.resistor import Resistor
from spira.lpe.mask import Mask


class __Ports__(Circuit):

    p1 = param.DataField(fdef_name='create_p1')
    p2 = param.DataField(fdef_name='create_p2')
    p3 = param.DataField(fdef_name='create_p3')
    p4 = param.DataField(fdef_name='create_p4')

    def create_p1(self):
        # return spira.Term(name='P1', midpoint=(-13*self.um, 15*self.um), orientation=90, width=1*self.um)
        m = [-13*self.um, self.jjsg126.ports['e1'].midpoint[1]]
        # m = [-13*self.um, 0] + self.jjsg126.ports['e1'].midpoint
        return spira.Term(name='P1', midpoint=m, orientation=-90, width=1*self.um)

    def create_p2(self):
        m = [-13*self.um, self.jjsg125.ports['e1'].midpoint[1]]
        # return spira.Term(name='P2', midpoint=(-13*self.um, -25*self.um), orientation=90, width=1*self.um)
        return spira.Term(name='P2', midpoint=m, orientation=-90, width=1*self.um)

    def create_p3(self):
        # m = [-13*self.um, self.jjsg125.ports['e1'].midpoint[1]]
        return spira.Term(name='P3', midpoint=(45*self.um, -17*self.um), orientation=0, width=1*self.um)

    def create_p4(self):
        return spira.Term(name='P4', midpoint=(45*self.um, 20*self.um), orientation=0, width=1*self.um)


class __Devices__(__Ports__):

    jjs122 = param.DataField(fdef_name='create_jjs122')
    jjs135 = param.DataField(fdef_name='create_jjs135')
    jjs77 = param.DataField(fdef_name='create_jjs77')
    jjsg104 = param.DataField(fdef_name='create_jjsg104')
    jjsg122 = param.DataField(fdef_name='create_jjsg122')
    jjsg125 = param.DataField(fdef_name='create_jjsg125')
    jjsg126 = param.DataField(fdef_name='create_jjsg126')
    jjsg141 = param.DataField(fdef_name='create_jjsg141')
    jjsg142 = param.DataField(fdef_name='create_jjsg142')
    jjsg172 = param.DataField(fdef_name='create_jjsg172')
    jjsg221 = param.DataField(fdef_name='create_jjsg221')
    jjsg285 = param.DataField(fdef_name='create_jjsg285')

    def create_jjs122(self):
        jj = Junction()
        jj.center = (0,0)
        return spira.SRef(jj, midpoint=(10.1*self.um, -5.525*self.um), rotation=90, reflection=True)

    def create_jjs135(self):
        jj = Junction()
        jj.center = (0,0)
        return spira.SRef(jj, midpoint=(21.2*self.um, -2.025*self.um), rotation=90, reflection=True)

    def create_jjs77(self):
        jj = Junction()
        jj.center = (0,0)
        return spira.SRef(jj, midpoint=(9.95*self.um, -1.975*self.um), rotation=270)

    def create_jjsg104(self):
        jj = Junction()
        jj.center = (0,0)
        return spira.SRef(jj, midpoint=(18.475*self.um, -5.25*self.um), rotation=270)

    def create_jjsg122(self):
        jj = Junction()
        jj.center = (0,0)
        return spira.SRef(jj, midpoint=(21.4*self.um, 9.7*self.um), rotation=270)

    def create_jjsg125(self):
        jj = Junction()
        jj.center = (0,0)
        return spira.SRef(jj, midpoint=(-6.775*self.um, -25.125*self.um))

    def create_jjsg126(self):
        jj = Junction()
        jj.center = (0,0)
        return spira.SRef(jj, midpoint=(-8.85*self.um, 15*self.um), reflection=True)

    def create_jjsg141(self):
        jj = Junction()
        jj.center = (0,0)
        return spira.SRef(jj, midpoint=(29.125*self.um, -19.4*self.um), reflection=True)

    def create_jjsg142(self):
        jj = Junction()
        jj.center = (0,0)
        return spira.SRef(jj, midpoint=(5.75*self.um, -25.425*self.um), rotation=270)

    def create_jjsg172(self):
        jj = Junction()
        jj.center = (0,0)
        return spira.SRef(jj, midpoint=(7.125*self.um, -11.025*self.um), rotation=270, reflection=True)

    def create_jjsg221(self):
        jj = Junction()
        jj.center = (0,0)
        return spira.SRef(jj, midpoint=(5.7*self.um, 7.825*self.um))

    def create_jjsg285(self):
        jj = Junction()
        jj.center = (0,0)
        return spira.SRef(jj, midpoint=(40.4*self.um, -12.225*self.um), rotation=270)
        

class __Circuits__(__Devices__):

    res_0  = param.DataField(fdef_name='create_res_0')

    def create_res_0(self):
        res = Resistor()
        return spira.SRef(res, midpoint=(46*self.um, 0.5*self.um), rotation=90)


class __Routes__(__Circuits__):

    w1 = param.FloatField(default=1*1e6)

    route_p1_jjsg126 = param.DataField(fdef_name='create_route_p1_jjsg126')
    route_p2_jjsg125 = param.DataField(fdef_name='create_route_p2_jjsg125')
    route_p3_jjsg285 = param.DataField(fdef_name='create_route_p3_jjsg285')

    route_res0_jjsg285 = param.DataField(fdef_name='create_route_res0_jjsg285')

    route_jjsg104_jjsg141 = param.DataField(fdef_name='create_route_jjsg104_jjsg141')
    route_jjsg285_jjsg141 = param.DataField(fdef_name='create_route_jjsg285_jjsg141')

    def create_route_p1_jjsg126(self):
        R1 = Route(port1=self.p1, port2=self.jjsg126.ports['e1'], player=RDD.PLAYER.M6)
        r1 = spira.SRef(R1)
        return r1

    def create_route_p2_jjsg125(self):
        R1 = Route(port1=self.p2, port2=self.jjsg125.ports['e1'], player=RDD.PLAYER.M6)
        r1 = spira.SRef(R1)
        return r1

    def create_route_p3_jjsg285(self):
        R1 = Route(port1=self.p3, port2=self.jjsg285.ports['e3'], player=RDD.PLAYER.M6)
        r1 = spira.SRef(R1)
        return r1
        
    def create_route_res0_jjsg285(self):
        R1 = Route(port1=self.res_0.ports['vl_Input'], port2=self.jjsg285.ports['e1'], player=RDD.PLAYER.M6)
        r1 = spira.SRef(R1)
        return r1

    def create_route_jjsg285_jjsg141(self):

        cm1 = (33*self.um, -21.5*self.um)
        cm2 = (35*self.um, -23.5*self.um)
        cm3 = (37*self.um, -18*self.um)

        ports = [
            self.jjsg141.ports['e3'],
            spira.Term(midpoint=cm1, width=self.w1, orientation=0),
            spira.Term(midpoint=cm1, width=self.w1, orientation=0-180),
            spira.Term(midpoint=cm2, width=self.w1, orientation=90),
            spira.Term(midpoint=cm2, width=self.w1, orientation=90-180),
            spira.Term(midpoint=cm3, width=self.w1, orientation=180),
            spira.Term(midpoint=cm3, width=self.w1, orientation=180-180),
            self.jjsg285.ports['e2']
        ]

        R1 = Route(port_list=ports, player=RDD.PLAYER.M6)
        r1 = spira.SRef(R1)

        return [r1]

    def create_route_jjsg104_jjsg141(self):

        cm1 = (22*self.um, -11*self.um)
        cm2 = (23.7*self.um, -9.7*self.um)
        cm3 = (26.3*self.um, -8*self.um)

            # spira.Connector(midpoint=cm1, width=self.w1, orientation=90),
            # spira.Connector(midpoint=cm2, width=self.w1, orientation=180),

        ports = [
            self.jjsg104.ports['e3'],
            spira.Term(midpoint=cm1, width=self.w1, orientation=90),
            spira.Term(midpoint=cm1, width=self.w1, orientation=90-180),
            spira.Term(midpoint=cm2, width=self.w1, orientation=180),
            spira.Term(midpoint=cm2, width=self.w1, orientation=180-180),
            spira.Term(midpoint=cm3, width=self.w1, orientation=90),
            spira.Term(midpoint=cm3, width=self.w1, orientation=90-180),
            self.jjsg141.ports['e2']
        ]

        R1 = Route(port_list=ports, player=RDD.PLAYER.M6)
        r1 = spira.SRef(R1)

        # # cm1 = (23.75*self.um, -9.7*self.um)
        # cm1 = (21*self.um, -11*self.um)
        # R1 = Route(
        #     port1=self.jjsg104.ports['e3'],
        #     port2=spira.Term(midpoint=cm1, width=self.w1, orientation=90),
        #     player=RDD.PLAYER.M6
        # )
        # r1 = spira.SRef(R1)

        return [r1]

    # def create_connect_j3_to_via1(self):
    #     s1 = self.jj3
    #     s2 = self.via_c5r_1

    #     # t1 = s1.ports['West']
    #     t2 = s2.ports['Input']
    #     t1 = s1.ports['e3']
    #     # t2 = s2.ports['e0']

    #     p1 = spira.Term(name='D1', midpoint=(-9*self.um, -3.2*self.um), width=1*1e6, orientation=0)
    #     p2 = spira.Term(name='D2', midpoint=(-9*self.um, -3.2*self.um), width=1*1e6, orientation=180)

    #     R1 = Route(port1=t1, port2=p1, player=RDD.PLAYER.M6, radius=0.5*self.um)
    #     r1 = spira.SRef(R1)

    #     R2 = Route(port1=p2, port2=t2, player=RDD.PLAYER.M6, radius=0.5*self.um)
    #     r2 = spira.SRef(R2)

    #     return [r1, r2]


class Not(__Routes__):

    def create_structures(self, elems):

        elems += self.res_0

        elems += self.jjs122
        elems += self.jjs135
        elems += self.jjs77
        elems += self.jjsg104
        elems += self.jjsg122
        elems += self.jjsg125
        elems += self.jjsg126
        elems += self.jjsg141
        elems += self.jjsg142
        elems += self.jjsg172
        elems += self.jjsg221
        elems += self.jjsg285

        return elems

    def create_routes(self, routes):
        routes += self.route_p1_jjsg126
        routes += self.route_p2_jjsg125
        routes += self.route_p3_jjsg285

        routes += self.route_res0_jjsg285

        routes += self.route_jjsg104_jjsg141
        routes += self.route_jjsg285_jjsg141
        return routes

    def create_ports(self, ports):
        ports += self.p1
        ports += self.p2
        ports += self.p3
        ports += self.p4
        return ports


if __name__ == '__main__':

    name = 'NOT PCell'
    spira.LOG.header('Running example: {}'.format(name))

    input_cell = Not()
    # input_cell.netlist
    input_cell.output()

    # mask = Mask(name=input_cell.name, cell=input_cell)
    # mask.netlist
    # mask.output()

    spira.LOG.end_print('Not Gate example finished')


