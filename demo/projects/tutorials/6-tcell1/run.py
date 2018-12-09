import spira
from spira import RDD
from spira.default.templates import ViaTemplate
from spira.lpe.primitives import Device

"""
This example demonstrates creating a via device. 
Ports are automatically detected and added using
the StructureCell base class implicit in the framework.

Demonstrates:
1. Creating a via device.
2. A device is created using the Device class.
"""

class ViaPCell(spira.Cell):

    def create_elementals(self, elems):
        points = [[[0,0], [3,0], [3,1], [0,1]]]

        ply_elems = spira.ElementList()

        ply_elems += spira.Polygons(polygons=points, gdslayer=RDD.BAS.LAYER)
        ply_elems += spira.Polygons(polygons=points, gdslayer=RDD.COU.LAYER)
        ply_elems += spira.Polygons(polygons=points, gdslayer=RDD.BC.LAYER)

        # Creates a device by sending the created 
        # elementals to the container cell.
        elems += spira.SRef(Device(cell_elems=ply_elems))
        return elems

# ------------------------------ Scripts ------------------------------------

via = ViaPCell()

ViaTemplate().create_elementals(elems=via.elementals)

via.construct_gdspy_tree()

