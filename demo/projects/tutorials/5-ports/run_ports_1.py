import spira
from spira import param
from spira import shapes


RDD = spira.get_rule_deck()


class PolygonGenerator(spira.Cell):

    width = param.FloatField(default=10)
    height = param.FloatField(default=1)

    def create_elementals(self, elems):
        shape = shapes.BoxShape(center=(5,0), width=self.width, height=self.height)
        elems += spira.Polygons(shape=shape)
        return elems


class TerminalExample(PolygonGenerator):

    def create_ports(self, ports):
        ports += spira.Term(name='P1', midpoint=(0,0), width=self.height)
        ports += spira.Term(name='P2', midpoint=(10,0), width=self.height, orientation=180)
        return ports


class PortExample(PolygonGenerator):

    def create_ports(self, ports):
        ports += spira.Port(name='P1', midpoint=(0,0))
        ports += spira.Port(name='P2', midpoint=(10,0))
        return ports


class TermPortExample(PolygonGenerator):

    def create_ports(self, ports):
        ports += spira.Port(name='P1', midpoint=(0,0))
        ports += spira.Term(name='P2', midpoint=(10,0), width=self.height, orientation=180)
        return ports


# -------------------------------------------------------------------


if __name__ == '__main__':

    topcell = spira.Cell('TopCell')

    t1 = spira.SRef(TerminalExample())
    p1 = spira.SRef(PortExample(), midpoint=(0, 10))
    tp = spira.SRef(TermPortExample(), midpoint=(0, 20))

    t1.rotate(angle=45)
    t1.translate(dx=-10, dy=0)
    t1.reflect()

    p1.rotate(angle=510)
    p1.translate(dx=5, dy=20)
    p1.reflect()

    topcell += t1
    topcell += p1
    topcell += tp

    topcell.output()











