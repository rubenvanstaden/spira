import spira
from spira import shapes
from spira.core.default.templates import ViaTemplate
from spira.lpe.primitives import Device


RDD = spira.get_rule_deck()


class ViaPCell(spira.Cell):

    def create_elementals(self, elems):
        points = [[[0,0], [3,0], [3,1], [0,1]]]

        ply_elems = spira.ElementList()

        shape = shapes.Shape(points=points)

        ply_elems += spira.Polygons(shape=shape, gdslayer=RDD.BAS.LAYER)
        # ply_elems += spira.Polygons(shape=points, gdslayer=RDD.COU.LAYER)
        # ply_elems += spira.Polygons(shape=points, gdslayer=RDD.BC.LAYER)

        # for ply in ply_elems:
        #     elems += ply

        # Creates a device by sending the created 
        # elementals to the container cell.
        # elems += spira.SRef(elementals=ply_elems)
        elems += spira.SRef(Device(cell_elems=ply_elems))
        return elems


# -------------------------------------------------------------------------------


via = ViaPCell()

# ViaTemplate().create_elementals(elems=via.elementals)

via.output()




