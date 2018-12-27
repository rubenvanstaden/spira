import spira
from spira import param
from spira import shapes


RDD = spira.get_rule_deck()


class TerminalExample(spira.Cell):

    width = param.FloatField(default=10)
    height = param.FloatField(default=1)

    def create_elementals(self, elems):
        shape = shapes.BoxShape(center=(5,0), width=self.width, height=self.height)
        elems += spira.Polygons(shape=shape)
        return elems

    def create_ports(self, ports):
        t1 = spira.Term(name='P1', midpoint=(0,0), width=self.height)
        ports += t1
        ports += spira.Term(name='P2', midpoint=(10,0), width=self.height, orientation=180)
        return ports


class PortExample(spira.Cell):

    width = param.FloatField(default=10)
    height = param.FloatField(default=1)

    def create_elementals(self, elems):
        shape = shapes.BoxShape(center=(5,0), width=self.width, height=self.height)
        elems += spira.Polygons(shape=shape)
        return elems

    def create_ports(self, ports):
        p1 = spira.Port(name='P1', midpoint=(0,0))
        ports += p1
        p2 = spira.Port(name='P2', midpoint=(10,0))
        ports += p2
        print(p1)
        print(p2)
        return ports


# -----------------------------------------------------------------------------------


if __name__ == '__main__':

    topcell = spira.Cell('TopCell')

    t1 = spira.SRef(TerminalExample())
    p1 = spira.SRef(PortExample(), midpoint=(0, 10))

    t1.rotate(angle=45)
    t1.translate(dx=-10, dy=0)
    t1.reflect()

    topcell += t1
    topcell += p1

    topcell.output()






