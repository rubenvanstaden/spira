import spira.all as spira
from spira.yevon.vmodel.virtual import *
from tests._03_structures.jtl_bias import JtlBias
from tests._03_structures.jtl_bias_ports import JtlBiasPorts
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()





# -------------------------------------------------------------------------------------------------------------


D = JtlBiasPorts()
# D.output()
# D.write_gdsii_mask()

# vp = virtual_process_model(device=D, process_flow=RDD.VMODEL.PROCESS_FLOW)
# vp.write_gdsii_vmodel()

vp = virtual_process_intersection(device=D, process_flow=RDD.VMODEL.PROCESS_FLOW)
# vp.write_gdsii_vinter()

# E = D.expand_transform()
E = D.pcell.expand_flat_copy()

contacts = vp.contact_ports

for p in E.ports:
    if p.locked is False:
        contacts += p

nets = E.nets(contacts=contacts)

# --- Step 1:
g_cell = nets.disjoint()
E.plotly_netlist(G=g_cell, graphname='metal', labeltext='id')

# # --- Step 2:
# # g_cell = nets.disjoint_union_and_combine_nodes()
# # from spira.yevon.geometry.nets.net import CellNet

# # cn = CellNet(g=g_cell)
# cn = CellNet()
# cn.g = g_cell
# cn.generate_branches()
# E.plotly_netlist(G=cn.g, graphname='metal', labeltext='id')






