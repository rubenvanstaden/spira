import spira.all as spira

from tests._03_structures._02_jj import Junction
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


class Jtl(spira.Circuit):
    """  """

    def get_transforms(self):
        t1 = spira.Translation(translation=(0, 0))
        t2 = spira.Translation(translation=(150, 0))
        return [t1, t2]

    def create_routes(self, elems):
        elems += spira.Rectangle(p1=(4, -4), p2=(146, 4), layer=RDD.PLAYER.M2.METAL)
        elems += spira.Rectangle(p1=(-3, -4), p2=(-30, 4), layer=RDD.PLAYER.M2.METAL)
        elems += spira.Rectangle(p1=(153, -4), p2=(180, 4), layer=RDD.PLAYER.M2.METAL)
        return elems

    def create_elements(self, elems):
        t1, t2 = self.get_transforms()
        jj = Junction()
        elems += spira.SRef(alias='S1', reference=jj, transformation=t1)
        elems += spira.SRef(alias='S2', reference=jj, transformation=t2)
        return elems


# ----------------------------------------------------------------------------------------


if __name__ == '__main__':

    C = Jtl(pcell=True)
    
    D = C.expand_flat_copy()

    from spira.yevon.vmodel.virtual import virtual_connect
    v_model = virtual_connect(device=D)
    v_model.gdsii_output_virtual_connect()

    from spira.yevon.filters.boolean_filter import MetalConnectFilter
    D = MetalConnectFilter()(D)

    # D.gdsii_output()
    D.netlist_output()
    # C.netlist_output()

