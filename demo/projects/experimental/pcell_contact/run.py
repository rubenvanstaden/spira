import spira
from spira import RDD
from spira import param
from spira.core.default.templates import ViaTemplate
from spira.lpe.primitives import Device
from spira.lpe.primitives import SLayout
from spira.lgm.shapes.basic import Box, BoxShape

"""
This example shows the automatic creation of a via
device using the set variables from the RDD.

Demonstrates:
1. How to automate a PCell from the RDD.
2. DRC values can be set as parameters.
"""


# class Box(spira.Cell):
# 
#     shape = param.DataField()
# 
#     def create_elementals(self, elems):
#         elems += spira.Polygons(polygons=self.shape.points, 
#                                 gdslayer=spira.Layer(number=76))
#         return elems


class ViaPCell(spira.Cell):

    spacing = param.FloatField(default=RDD.BC.SPACING)

    width = param.FloatField(default=RDD.BAS.WIDTH)
    height = param.FloatField(default=RDD.BAS.WIDTH)

    metal_layer_1 = param.DataField(default=RDD.BAS)
    metal_layer_2 = param.DataField(default=RDD.COU)
    contact_layer = param.DataField(default=RDD.BC)

    def validate_parameters(self):
        if self.width < self.metal_layer_1.WIDTH:
            return False
        if self.width < self.metal_layer_2.WIDTH:
            return False
        return True

    def create_elementals(self, elems):

        elems += Box(shape=BoxShape(
            width=self.width,
            height=self.height,
            gdslayer=self.metal_layer_1.LAYER)
        )

        # elems += Box(shape=BoxShape(width=self.width,
        #                    height=self.height,
        #                    gdslayer=self.metal_layer_2.LAYER))

        elems += Box(shape=BoxShape(
            width=self.width - self.spacing,
            height=self.width - self.spacing,
            gdslayer=self.contact_layer.LAYER)
        )

        return elems


if __name__ == '__main__':

    via = ViaPCell()
    via.output()

    # sl = SLayout(cell=via, level=1)
    # # ViaTemplate().create_elementals(elems=sl.elementals)
    # sl.output()








