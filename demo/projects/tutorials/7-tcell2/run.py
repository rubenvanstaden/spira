import spira
from spira import RDD
from spira import param
from spira.default.templates import ViaTemplate
from spira.lpe.primitives import Device

"""
This example shows the automatic creation of a via
device using the set variables from the RDD.

Demonstrates:
1. How to automate a PCell from the RDD.
2. DRC values can be set as parameters.
"""

class ViaPCell(spira.Cell):

    spacing = param.FloatField(default=RDD.BC.SPACING)

    def create_elementals(self, elems):
         
        ply_elems = spira.ElementList()

        ply_elems += spira.Box(center=(0,0), 
                               width=RDD.BAS.WIDTH,
                               height=RDD.BAS.WIDTH,
                               gdslayer=RDD.BAS.LAYER)
        ply_elems += spira.Box(center=(0,0), 
                               width=RDD.COU.WIDTH,
                               height=RDD.COU.WIDTH,
                               gdslayer=RDD.COU.LAYER)
        ply_elems += spira.Box(center=(0,0), 
                               width=RDD.BAS.WIDTH - self.spacing,
                               height=RDD.BAS.WIDTH - self.spacing,
                               gdslayer=RDD.BC.LAYER)
        elems += spira.SRef(Device(cell_elems=ply_elems))
        return elems

# ------------------------------ Scripts ------------------------------------

via = ViaPCell()

ViaTemplate().create_elementals(elems=via.elementals)

via.construct_gdspy_tree()




