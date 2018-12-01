import spira

from spira.kernel import field as param

from spira import ElementList
from spira import Cell
from spira import SRef
from spira import Circle
from spira import Rectangle
from spira import Port


class VerticalRoute(spira.Cell):

      points = param.ListField()
      layer = param.IntegerField()

      def create_elementals(self, elems):
            width = 1
            for pp in self.points:
                  elems += Rectangle(point1=pp[0],
                                     point2=pp[1],
                                     layer=self.layer)

            port1 = Port(name='VR_Port_1',
                        midpoint=[5, 0.5],
                        width=width,
                        orientation=0)

            port2 = Port(name='VR_Port_2',
                        midpoint=[0, 0.5],
                        width=width,
                        orientation=0)

            elems += port1
            elems += port2

            return elems


class HorizontalRoute(spira.Cell):

      points = param.ListField()
      layer = param.IntegerField()

      def create_elementals(self, elems):
            width = 1
            for pp in self.points:
                  elems += Rectangle(point1=pp[0],
                                     point2=pp[1],
                                     layer=self.layer)

            port1 = Port(name='Port_1',
                        midpoint=[2, 0],
                        width=width,
                        orientation=0)

            port2 = Port(name='Port_2',
                        midpoint=[-2, 0],
                        width=width,
                        orientation=0)

            elems += port1
            elems += port2

            return elems


class Reflection(spira.Cell):

    def create_elementals(self, elems):

        width = 1

        p0 = [[[0, 0], [5, width]]]
        p1 = [[[-2, -0.5], [2, 0.5]]]

        vr = VerticalRoute(points=p0, layer=99)
        hr = HorizontalRoute(points=p1, layer=44)

        s1 = SRef(vr)
        s2 = SRef(hr)

        # s1.reflect(p1=[0,0], p2=[1,1])

        # s1.connect(port='VR_Port_1', destination=s2.ports['Port_1'])
        # s2.rotate(angle=-180, center=s2._local_ports['Port_2'])
        # s2.move(origin=s2.origin, destination=[20,20])

        elems += s1
        elems += s2

        return elems


if __name__ == '__main__':
    rr = Reflection()
    # rr.reflect(p1=[0,0], p2=[1,1])
    rr.write_gds(name='test_reflection', collect_elements=True)

