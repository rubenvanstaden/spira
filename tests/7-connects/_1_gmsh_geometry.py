import spira.all as spira
from spira.yevon.vmodel.virtual import *
from tests._03_structures.jtl_bias import JtlBias
from tests._03_structures.jtl_bias_ports import JtlBiasPorts
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


# class JtlGeometry(JtlBias):
class JtlGeometry(JtlBiasPorts):
    """ Extend the JTL cell to construct a netlist by first
    generating a Gmsh geometry using the virtual polygon model. """

    def create_nets(self, nets):

        # elems = virtual_process_model(self.process_elementals)
        vp = virtual_process_model(device=self, process_flow=RDD.VMODEL.PROCESS_FLOW)

        for process, geom in vp.geometry.items():

            pp = spira.ElementalList()
            for e in self.process_elementals:
                if e.layer.process == process:
                    pp += e

            bp = spira.ElementalList()
            for e in self.block_elementals:
                if e.layer.process == process:
                    bp += e

            net = spira.Net(geom=geom)

            Fs = spira.NetProcessLabelFilter(process_polygons=pp)
            Fs += spira.NetBlockLabelFilter(references=self.elementals.sref)
            Fs += spira.NetDeviceLabelFilter(device_ports=self.ports)

            net = Fs(net)

            nets += net

            return nets


# -------------------------------------------------------------------------------------------------------------


D = JtlGeometry()
# D.write_gdsii_vmodel()
# D.write_gdsii_blocks()

# vp = virtual_process_model(device=D, process_flow=RDD.VMODEL.PROCESS_FLOW)
# vp.geometry
# vp.write_gdsii_vmodel()

g = D.nets[0].g
D.plotly_netlist(G=g, graphname='metal', labeltext='id')

# D.output()




