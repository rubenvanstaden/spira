import spira
from spira import param
from spira import LOG
from spira import RDD


"""
This examples defines the creation of a basic parameterized cell.
This example shows the following:

1. How to add elementals to a cell using the `create_elementals` method.
2. Create a polygon using the framework and add it to the cell.
3. How to use the parameters when creating elementals.
4. How to write to a GDSII file.
"""


class PCell(spira.Cell):

    layer = param.LayerField(number=RDD.BAS.LAYER.number)
    width = param.FloatField(default=RDD.BAS.WIDTH)

    def create_elementals(self, elems):
        points = [[[0,0], [3,0], [3,1], [0,1]]]
        elems += spira.Polygons(polygons=points, gdslayer=self.layer)
        return elems


# --------------------------------------------------------------------------


if __name__ == '__main__':

    pcell = PCell()
    pcell.construct_gdspy_tree()


