import spira
from spira import param, shapes, io
from spira.lpe.circuits import Circuit
from spira.lpe.mask import Mask
from demo.pdks.process.mitll_pdk.database import RDD
from spira.lgm.route.manhattan_base import Route

from demo.pdks.components.mitll.junction import Junction
from demo.pdks.components.mitll.via import ViaC5R, ViaI5


class __Devices__(Circuit):

    jj1 = param.DataField(fdef_name='create_junction_one')
    jj2 = param.DataField(fdef_name='create_junction_two')

    def create_junction_one(self):
        jj = Junction()
        # jj.center = (0,0)
        return spira.SRef(jj, midpoint=(5*self.um, 0*self.um), rotation=180)

    def create_junction_two(self):
        jj = Junction()
        # jj.center = (0,0)
        return spira.SRef(jj, midpoint=(15*self.um, 0*self.um), rotation=180)


class __Ports__(__Devices__):

    p1 = param.DataField(fdef_name='create_p1')
    p2 = param.DataField(fdef_name='create_p2')
    p3 = param.DataField(fdef_name='create_p3')

    def create_p1(self):
        # midpoint = self.jj1.ports['West'] + [-5*self.um, 0*self.um]
        midpoint = self.jj1.ports['e3'] + [-5*self.um, 0*self.um]
        return spira.Term(name='P1', midpoint=midpoint, orientation=-90, width=1*self.um)

    def create_p2(self):
        # midpoint = self.jj2.ports['East'] + [5*self.um, 0*self.um]
        midpoint = self.jj2.ports['e1'] + [5*self.um, 0*self.um]
        return spira.Term(name='P2', midpoint=midpoint, orientation=90, width=1*self.um)


class __Routes__(__Ports__):

    p1_jj1 = param.DataField(fdef_name='create_p1_jj1')
    jj1_jj2 = param.DataField(fdef_name='create_jj1_jj2')
    jj2_p2 = param.DataField(fdef_name='create_jj2_p2')

    def create_p1_jj1(self):
        R1 = Route(
            port1=self.p1,
            # port2=self.jj1.ports['West'],
            port2=self.jj1.ports['e3'],
            player=RDD.PLAYER.M6)
        r1 = spira.SRef(R1)
        return r1

    def create_jj1_jj2(self):
        R1 = Route(
            # port1=self.jj1.ports['East'],
            # port2=self.jj2.ports['West'],
            port1=self.jj1.ports['e1'],
            port2=self.jj2.ports['e3'],
            player=RDD.PLAYER.M6)
        r1 = spira.SRef(R1)
        return r1
        
    def create_jj2_p2(self):
        R1 = Route(
            # port1=self.jj2.ports['East'],
            port1=self.jj2.ports['e1'],
            port2=self.p2,
            player=RDD.PLAYER.M6)
        r1 = spira.SRef(R1)
        return r1


class Jtl(__Routes__):
    """ Parameterized Cell for JTL circuit. """

    def create_structures(self, elems):
        elems += self.jj1
        elems += self.jj2
        return elems

    def create_routes(self, elems):
        elems += self.p1_jj1
        elems += self.jj1_jj2
        elems += self.jj2_p2
        return elems

    def create_ports(self, ports):
        ports = super().create_ports(ports)
        ports += self.p1
        ports += self.p2
        return ports


if __name__ == '__main__':

    name = 'JTL PCell'
    spira.LOG.header('Running example: {}'.format(name))

    input_cell = Jtl()
    # input_cell.netlist
    # input_cell.output()
    
    mask = Mask(name=input_cell.name, cell=input_cell)
    mask.netlist
    mask.output()

    spira.LOG.end_print('JTL example finished')



