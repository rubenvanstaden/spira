import spira.all as spira

from tests._03_structures._02_jj import Junction
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


class VirtualBias(spira.Cell):

    def create_elementals(self, elems):

        elems += spira.Rectangle(p1=(60, 45), p2=(80, 80), layer=RDD.PLAYER.M2.METAL)

        c1 = spira.Cell(name='ply1')
        c1 += spira.Rectangle(p1=(60, 80), p2=(80, 100), layer=RDD.PLAYER.M2.METAL)
        c1 += spira.Rectangle(p1=(70, 60), p2=(100, 70), layer=RDD.PLAYER.M2.METAL)
        elems += spira.SRef(c1)
        
        return elems


class JtlBiasPorts(spira.Circuit):

    def get_transforms(self):
        t1 = spira.Translation(translation=(0, 0))
        t2 = spira.Translation(translation=(150, 0))
        return [t1, t2]

    def create_routes(self, elems):
        elems += spira.Rectangle(p1=(4, -4), p2=(146, 4), layer=RDD.PLAYER.M2.METAL)
        elems += spira.Rectangle(p1=(-3, -4), p2=(-30, 4), layer=RDD.PLAYER.M2.METAL)
        elems += spira.Rectangle(p1=(153, -4), p2=(180, 4), layer=RDD.PLAYER.M2.METAL)
        elems += spira.Rectangle(p1=(60, 0), p2=(80, 50), layer=RDD.PLAYER.M2.METAL)
        return elems

    def create_elementals(self, elems):
        t1, t2 = self.get_transforms()

        jj = Junction()

        elems += spira.SRef(alias='S1', reference=jj, transformation=t1)
        elems += spira.SRef(alias='S2', reference=jj, transformation=t2)

        elems += spira.SRef(reference=VirtualBias())

        return elems

    def create_ports(self, ports):
        ports += spira.Port(name='P1', process=RDD.PROCESS.M2, midpoint=(-28, 0), orientation=180, width=8)
        ports += spira.Port(name='P2', process=RDD.PROCESS.M2, midpoint=(180, 0), orientation=0, width=8)
        ports += spira.Port(name='P3', process=RDD.PROCESS.M2, midpoint=(100, 65), orientation=0, width=20)
        ports += spira.Port(name='P4', process=RDD.PROCESS.M2, midpoint=(70, 100), orientation=90, width=20)
        return ports


# -------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':

    D = JtlBiasPorts(pcell=False)

    # from spira.yevon.filters.boolean_filter import MetalConnectFilter
    # F = MetalConnectFilter()
    # D = F(D)
    
    D.gdsii_output()
    D.netlist_output()


