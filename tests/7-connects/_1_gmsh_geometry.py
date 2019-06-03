import spira.all as spira
from spira.yevon.vmodel.virtual import *
from tests._03_structures.jtl_bias import JtlBias


class JtlGeometry(JtlBias):
    """ Extend the JTL cell to construct a netlist by first
    generating a Gmsh geometry using the virtual polygon model. """

    def create_nets(self, nets):

        # elems = virtual_process_model(self.process_elementals)

        # for e in self.process_elementals:
        #     geom = generate_simulation_geometry(cell=self)
        #     net = spira.Net(gmsh_geometry=geom, ports=ports)
        #     nets += net

        return nets


# -------------------------------------------------------------------------------------------------------------


D = JtlGeometry()
# D.write_gdsii_vmodel()
D.write_gdsii_blocks()

# vp = virtual_process_model(device=D)
# vp.geometry

    



