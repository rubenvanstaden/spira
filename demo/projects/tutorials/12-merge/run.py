import spira
from spira import RDD
from spira import param
from spira.core.default.templates import ViaTemplate
from spira.lpe.primitives import Device
from demo.projects.tutorials.pcell_contact.run import ViaPCell
from spira.lpe.primitives import SLayout
from spira.lgm.shapes.shape import __Shape__


"""
This example shows the automatic creation of a via
device using the set variables from the RDD.

Demonstrates:
1. How to automate a PCell from the RDD.
2. DRC values can be set as parameters.
"""


class WaveGuide(__Shape__):

    def create_points(self, points):

        points = [[[0,0], [3,0], [3,1], [0,1]],
                  [[2,0], [5,0], [5,1], [2,1]]]

        return points


# class Merge(spira.Cell):
# 
#     def create_elementals(self, elems):
# 
#         p1 = [[[0,0], [3,0], [3,1], [0,1]]]
#         elems += spira.Polygons(polygons=p1, gdslayer=spira.Layer(number=88))
# 
#         p2 = [[[2,0], [5,0], [5,1], [2,1]]]
#         elems += spira.Polygons(polygons=p2, gdslayer=spira.Layer(number=88))
# 
#         return elems


class Merge(spira.Cell):

    def create_elementals(self, elems):

        shape = WaveGuide()
        shape = shape.apply_merge

        elems += spira.Polygons(polygons=shape.points, gdslayer=spira.Layer(number=88))

        return elems


if __name__ == '__main__':

    c1 = Merge()
    c1.construct_gdspy_tree()

#     cell = SLayout(cell=c1, level=2)
#     cell.construct_gdspy_tree()











