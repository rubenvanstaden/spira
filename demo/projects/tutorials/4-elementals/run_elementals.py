import spira
from spira import param
from spira import shapes
from spira import LOG


RDD = spira.get_rule_deck()


class PCell(spira.Cell):

    layer = param.LayerField(number=RDD.BAS.LAYER.number)
    width = param.FloatField(default=RDD.BAS.WIDTH)

    def create_elementals(self, elems):
        p1 = [[[0,0], [3,0], [3,1], [0,1]]]
        p2 = [[[4,0], [7,0], [7,1], [4,1]]]
        p3 = [[[8,0], [11,0], [11,1], [8,1]]]

        # Create polygon using class parameters.
        elems += spira.Polygons(p1, gdslayer=self.layer)

        # Create polygon using new layer number.
        elems += spira.Polygons(
            shape=p2,
            gdslayer=spira.Layer(number=77)
        )

        # Create polygon using new shape, number and datatype.
        elems += spira.Polygons(
            shape=shapes.Shape(points=p3),
            gdslayer=spira.Layer(number=51, datatype=1)
        )

        return elems


# --------------------------------------------------------------------------


if __name__ == '__main__':

    pcell = PCell()
    pcell.output()


