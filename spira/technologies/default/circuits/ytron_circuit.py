import spira.all as spira
from spira.all import RDD
from tutorials.advanced._0_devices import YtronDevice, YtronShape


class YtronCircuit(spira.Circuit):

    ytron = spira.Parameter(fdef_name='create_ytron')

    @spira.cache()
    def get_io_ports(self):
        p1 = spira.Port(name='P1_M1', midpoint=(-10,10), orientation=0)
        p2 = spira.Port(name='P2_M1', midpoint=(5,10), width=0.5, orientation=270)
        p3 = spira.Port(name='P3_M1', midpoint=(0,-10), width=1, orientation=90)
        return [p1, p2, p3]

    def create_ytron(self):
        shape = YtronShape(rho=0.5, theta=5)
        D = YtronDevice(shape=shape)
        return spira.SRef(alias='ytron', reference=D)

    def create_elements(self, elems):
        p1, p2, p3 = self.get_io_ports()

        elems += self.ytron

        elems += spira.RouteManhattan(
            ports=[self.ytron.ports['Pl_M1'], p1],
            width=self.ytron.reference.shape.arm_widths[0],
            layer=RDD.PLAYER.M1.METAL,
            corners=self.corners)

        elems += spira.RouteStraight(p1=p2,
            p2=self.ytron.ports['Pr_M1'],
            layer=RDD.PLAYER.M1.METAL,
            path_type='sine', width_type='sine')

        elems += spira.RouteStraight(p1=p3,
            p2=self.ytron.ports['Psrc_M1'],
            layer=RDD.PLAYER.M1.METAL,
            path_type='sine', width_type='sine')

        return elems

    def create_ports(self, ports):
        ports += self.get_io_ports()
        return ports


# class YtronCircuit(spira.Circuit):

#     ytron = spira.CellParameter(restriction=spira.RestrictType([YtronDevice]))

#     def create_elements(self, elems):
#         return elems

#     def create_ports(self, ports):
#         return port


if __name__ == '__main__':

    D = YtronCircuit()
    # D.gdsii_output(name='YtronPCell')
    D.gdsii_output(name='YtronCircuit')

