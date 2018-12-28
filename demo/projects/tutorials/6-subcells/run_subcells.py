import spira
from spira import param
from spira import shapes
from spira import LOG


RDD = spira.get_rule_deck()


class PolygonPCell(spira.Cell):

    layer = param.LayerField(number=RDD.BAS.LAYER.number)
    width = param.FloatField(default=RDD.BAS.WIDTH)

    def create_elementals(self, elems):
        p0 = [[[0.3, 0.3], [3.6, 3]],
              [[1.45, 2.8], [2.45, 5]],
              [[1.25, 4.75], [2.65, 6]]]
        for points in p0:
            shape = shapes.RectangleShape(
                p1=points[0],
                p2=points[1],
                gdslayer=self.layer
            )
            ply = spira.Polygons(shape=shape)
            elems += ply
        return elems


class PCell(spira.Cell):

    def create_elementals(self, elems):

        ply = PolygonPCell()

        elems += spira.SRef(ply)

        return elems


# ---------------------------------------------------------------------


if __name__ == '__main__':

    pcell = PCell()
    pcell.output()


