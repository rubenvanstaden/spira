import spira.all as spira
from spira.yevon.vmodel.virtual import *
from tests._03_structures.jtl_bias import JtlBias
from tests._03_structures.jtl_bias_ports import JtlBiasPorts
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


class A(spira.Cell):
    """ Cell with boxes to stretch a SRef containing two polygons. """

    def get_polygons(self):
        p1 = spira.Rectangle(p1=(0, 0), p2=(10*1e6, 2*1e6), layer=RDD.PLAYER.M1.METAL)
        p2 = spira.Rectangle(p1=(10*1e6, 0), p2=(20*1e6, 2*1e6), layer=RDD.PLAYER.M1.METAL)
        return [p1, p2]

    def create_elementals(self, elems):
        elems += self.get_polygons()
        return elems

    # def create_ports(self, ports):
    #     p1, p2 = self.get_polygons()
    #     ports = p1.ports & p2
    #     return ports


class B(spira.Cell):
    """ Cell with boxes to stretch a SRef containing two polygons. """

    def get_polygons(self):
        p1 = spira.Rectangle(alias='M0', p1=(0,0), p2=(12*1e6, 2*1e6), layer=RDD.PLAYER.M1.METAL)
        c = spira.Cell(name='Cs1')
        # c += spira.Rectangle(alias='M1', p1=(0,0), p2=(10*1e6, 2*1e6), layer=RDD.PLAYER.M1.METAL)
        c += spira.Wedge(begin_coord=(1*1e6, 0), end_coord=(10*1e6, 0), layer=RDD.PLAYER.M1.METAL)
        S = spira.SRef(c, midpoint=(10*1e6, 0))
        return [p1, S]

    def create_elementals(self, elems):
        elems += self.get_polygons()
        return elems


class C(spira.Cell):
    """ Cell with boxes to stretch a SRef containing two polygons. """

    def create_elementals(self, elems):
        p1 = spira.Rectangle(alias='P0', p1=(0,0), p2=(12*1e6, 2*1e6), layer=RDD.PLAYER.M1.METAL)

        c1 = spira.Cell(name='Cs1')
        c1 += spira.Rectangle(alias='P1', p1=(0,0), p2=(10*1e6, 3*1e6), layer=RDD.PLAYER.M1.METAL)

        c2 = spira.Cell(name='Cs2')
        c2 += spira.Rectangle(alias='P2', p1=(0,0), p2=(10*1e6, 4*1e6), layer=RDD.PLAYER.M1.METAL)

        c1 += spira.SRef(c2, midpoint=(8*1e6, 0))

        D = spira.Cell(name='D2')

        D += spira.SRef(c1, midpoint=(10*1e6, 0))

        elems += p1
        elems += spira.SRef(reference=D)

        return elems

    def create_ports(self, ports):

        ports += spira.Port(name='P1', midpoint=(0, 1*1e6), orientation=180, process=RDD.PROCESS.M3)
        ports += spira.Port(name='P2', midpoint=(28*1e6, 2*1e6), orientation=0, process=RDD.PROCESS.M3)

        return ports

    # def create_nets(self, nets):

    #     # nets += self.net

    #     for e in self.elementals.sref:
    #         nets += e.ref.net

    #     print(nets)

    #     return nets


# -------------------------------------------------------------------------------------------------------------


# D = A()
# D = B()
D = C()
# D.output()

# vp = virtual_process_model(device=D, process_flow=RDD.VMODEL.PROCESS_FLOW)
# vp.write_gdsii_vmodel()

vp = virtual_process_intersection(device=D, process_flow=RDD.VMODEL.PROCESS_FLOW)
# vp.write_gdsii_vinter()

E = D.expand_transform()
E = D.flat_expand_transform_copy()

contacts = vp.__make_contact_ports__()
contacts += E.ports

nets = E.nets(contacts=contacts)

# print('\n\n[*] Nets:')
# for n in nets:
#     print(n)
# print('')

# g_cell = nets.disjoint()
g_cell = nets.disjoint_union_and_combine_nodes()

from spira.yevon.geometry.nets.net import CellNet

# cn = CellNet(g=g_cell)
cn = CellNet()
cn.g = g_cell

cn.generate_branches()

# E.plotly_netlist(G=g_cell, graphname='metal', labeltext='id')
E.plotly_netlist(G=cn.g, graphname='metal', labeltext='id')
# E.output()






