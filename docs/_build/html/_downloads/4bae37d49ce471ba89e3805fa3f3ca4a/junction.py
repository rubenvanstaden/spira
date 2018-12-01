import spira
from spira import param
from spira import Rectangle
from spira.rdd import get_rule_deck


RDD = get_rule_deck()


class PhysicalLayer(spira.Cell):

      points = param.ListField()
      layer = param.LayerField()

      def create_elementals(self, elems):
            for pp in self.points:
                  elems += Rectangle(point1=pp[0],
                                     point2=pp[1],
                                     layer=self.layer)
            return elems


class Junction(spira.Cell):

      def create_elementals(self, elems):

            p0 = [[[0.5, -1.4], [3.4, -0.3]]]
            elems += PhysicalLayer(points=p0, layer=RDD.M6)

            p1 = [[[0.3, 0.3], [3.6, 3]],
                  [[1.45, 2.8], [2.45, 5]],
                  [[1.25, 4.75], [2.65, 6]]]
            elems += PhysicalLayer(points=p1, layer=RDD.M5)

            p2 = [[[0, -2], [3.8, 3.2]],
                  [[1, 4.6], [2.9, 7.3]]]
            elems += PhysicalLayer(points=p2, layer=RDD.I5)

            p3 = [[[0.3, -1.6], [3.6, 3]],
                  [[1.3, 4.8], [2.6, 6]]]
            elems += PhysicalLayer(points=p3, layer=RDD.I4)

            p4 = [[[1, 1], [2.9, 2.3]]]
            elems += PhysicalLayer(points=p4, layer=RDD.J5)

            p5 = [[[1, 1], [2.9, 2.3]]]
            elems += PhysicalLayer(points=p5, layer=RDD.C5)

            p6 = [[[1.3, 6.3], [2.6, 7]]]
            elems += PhysicalLayer(points=p6, layer=RDD.R5)

            p7 = [[[1, 0.5], [2.9, 7.3]]]
            elems += PhysicalLayer(points=p7, layer=RDD.M7)

            # p8 = [[[1.3, 1.3], [2.6, 2]]]
            # elems += PhysicalLayer(points=p8, layer=10)

            return elems


if __name__ == '__main__':

    from spira import settings
    from spira.templates.library import library

    settings.set_library(library)

    name = 'Junction_PCell'

    spira.LOG.header('Running example: {}'.format(name))

    jj = Junction()
    print(jj.center)
    jj.output(name=name)

    spira.LOG.end_print('Junction example finished')
