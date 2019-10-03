import spira.all as spira

from spira.yevon.geometry.line import *
from spira.yevon.geometry.vector import *

from spira.technologies.waterloo.process.database import RDD


class BoschVia(spira.Device):

    __name_prefix__ = 'Bosch_Standard'

    radius = spira.NumberParameter(default=RDD.B0.MIN_SIZE)

    m0_radius = spira.Parameter(fdef_name='create_m0_radius', doc='Radius of the ground layer around the via.')
    al_radius = spira.Parameter(fdef_name='create_al_radius', doc='Radius of the aluminum layer around the via.')

    def create_m0_radius(self):
        return (self.radius + 2*RDD.Al.B0_MIN_SURROUND)

    def create_al_radius(self):
        return (self.radius + 2*RDD.Al.B0_MIN_SURROUND)

    def create_elements(self, elems):
        elems += spira.Circle(box_size=(self.radius, self.radius), layer=RDD.PLAYER.B0.VIA)
        elems += spira.Circle(box_size=(self.m0_radius, self.m0_radius), layer=RDD.PLAYER.M0.METAL)
        elems += spira.Circle(box_size=(self.al_radius, self.al_radius), layer=RDD.PLAYER.Al.METAL)
        return elems

    def create_ports(self, ports):

        return ports


class ThroughSiliconVia(spira.Circuit):
    """ Basic 2 TSV bosch via layout. """

    width = spira.NumberParameter(default=1000)
    length = spira.NumberParameter(default=2000)

    via = spira.CellParameter(
        default=BoschVia,
        restriction=spira.RestrictType([BoschVia]),
        doc='TSV component for connecting M0 to Al.')

    via_left = spira.Parameter(fdef_name='create_via_left')
    via_right = spira.Parameter(fdef_name='create_via_right')

    p1 = spira.Parameter(fdef_name='create_p1')
    p2 = spira.Parameter(fdef_name='create_p2')

    def validate_parameters(self):
        if self.length < self.width:
            raise ValueError('Length cannot be less than width.')
        return True

    def create_p1(self):
        return spira.Port(name='Al:T1', midpoint=(-2000, 0), orientation=0, width=20)

    def create_p2(self):
        return spira.Port(name='Al:T2', midpoint=(2000, 0), orientation=180, width=20)

    def create_via_left(self):
        via = self.via(radius=300)
        return spira.SRef(via, midpoint=(-1000, 0))

    def create_via_right(self):
        via = self.via(radius=300)
        return spira.SRef(via, midpoint=(1000, 0))

    def create_elements(self, elems):
        elems += [self.via_left, self.via_right]

        d1 = spira.Port(name='Al:D1', midpoint=(-1000, 0), orientation=180, width=20)
        d11 = spira.Port(name='M0:D3', midpoint=(-1000, 0), orientation=0, width=20)
        d2 = spira.Port(name='Al:D2', midpoint=(1000, 0), orientation=0, width=20)
        d12 = spira.Port(name='M0:D4', midpoint=(1000, 0), orientation=180, width=20)
        d3 = spira.Port(name='M0:D5', midpoint=(0, 0), orientation=90, width=20)

        # FIXME: Throughs out with a wierd angle.
        # elems += spira.RouteManhattan(
        #     ports=[self.p1, d1],
        #     width=5, layer=RDD.PLAYER.Al.METAL)

        elems += spira.RouteStraight(p1=self.p1, p2=d1, layer=RDD.PLAYER.Al.METAL)
        elems += spira.RouteStraight(p1=d11, p2=d12, layer=RDD.PLAYER.M0.METAL)
        elems += spira.RouteStraight(p1=self.p2, p2=d2, layer=RDD.PLAYER.Al.METAL)

        return elems

    def create_ports(self, ports):
        ports += [self.p1, self.p2]
        return ports
        

class Row(spira.Circuit):
    """ Test circuit created for TSV fabrication. """

    def create_elements(self, elems):

        D1 = ThroughSiliconVia()
        D2 = ThroughSiliconVia()

        s1 = spira.SRef(reference=D1)
        s2 = spira.SRef(reference=D1, transformation=spira.Rotation(90))

        s1.connect(port='Al:T1', destination=s2.ports['Al:T2'])

        elems += s1
        elems += s2

        return elems

    def create_ports(self, ports):

        p1 = self.elements[0].ports['Al:T2']
        p1.rotate(rotation=180, rotation_center=p1.midpoint)
        ports += p1
        
        p1 = self.elements[0].ports['Al:T1']
        p1.rotate(rotation=180, rotation_center=p1.midpoint)
        ports += p1

        # ports += self.elements[0].ports['Al:T2']
        # ports += self.elements[1].ports['Al:T1']
        return ports


class TsvCircuit(spira.Circuit):
    """ Test circuit created for TSV fabrication. """
    
    d2 = spira.Parameter(fdef_name='create_d2')
    
    def create_d2(self):
        return spira.Port(name='Al:D2', midpoint=(-1000, -5000), orientation=0, width=20)

    def create_elements(self, elems):

        r1 = Row()

        s1 = spira.SRef(r1)
        # s2 = spira.SRef(r1, midpoint=(2000, -1000))
        s2 = spira.SRef(r1, transformation=spira.Translation((2000, -1000)))

        elems += s1
        elems += s2

        print(s1.ports['Al:T2'])
        print(s2.ports['Al:T2'])
        
        d1 = spira.Port(name='Al:D1', midpoint=(1000, 7000), orientation=180, width=20)
        # d2 = spira.Port(name='Al:D2', midpoint=(-1000, -5000), orientation=0, width=20)

        elems += spira.RouteManhattan(
            ports=[s1.ports['Al:T2'], d1, s2.ports['Al:T2']],
            width=20, layer=RDD.PLAYER.Al.METAL)

        elems += spira.RouteManhattan(
            ports=[s1.ports['Al:T1'], self.d2],
            width=20, layer=RDD.PLAYER.Al.METAL)

        return elems

    def create_ports(self, ports):

        print(self.elements)

        ports += self.d2

        return ports
        

class TsvArray(spira.Circuit):
    """ Test circuit created for TSV fabrication. """

    def create_elements(self, elems):

        D1 = TsvCircuit()

        s1 = spira.SRef(D1)
        s2 = spira.SRef(D1, midpoint=(6000, 2000))

        s2.connect(port='Al:D2', destination=s1.ports['Al:D2'])

        elems += s1
        elems += s2

        return elems


if __name__ == '__main__':

    # ------------------------------------------------------------------

    # D = BoschVia()
    # D = ThroughSiliconVia()
    # D = TsvCircuit()
    D = TsvArray()

    # D = D.flat_copy()
    
    # from spira.yevon import filters
    # F = filters.ToggledCompositeFilter(filters=[])
    # F += filters.ProcessBooleanFilter(name='boolean', metal_purpose=RDD.PURPOSE.METAL)

    # D = F(D)

    D.gdsii_view()

    # from spira.yevon.vmodel.virtual import virtual_connect
    # v_model = virtual_connect(device=D)

    # v_model.view_virtual_connect(show_layers=True)
    # v_model.view_derived_contacts()
    # v_model.view_derived_edges()



