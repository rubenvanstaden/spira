import spira
from spira import param
from spira import shapes
from spira import RDD
from spira.core.default.templates import ViaTemplate
from spira.lpe.primitives import Device


"""
In this example a basic transmissionline is created
with two ports connected to the endpoints.

Demonstrates:
1. How ports are added to a PCell.
"""


class TransmissionLine(spira.Cell):

    width = param.FloatField(default=10)
    height = param.FloatField(default=1)

    def create_elementals(self, elems):
        shape = shapes.BoxShape(center=(5,0), width=self.width, height=self.height)
        elems += shapes.Box(shape=shape)
        return elems

    def create_ports(self, ports):
        ports += spira.Term(name='P1', midpoint=(0,0), width=self.height)
        ports += spira.Term(name='P2', midpoint=(10,0), width=1)
        return ports


# -------------------------------------------------------------------


if __name__ == '__main__':

    cell = TransmissionLine()
    cell.construct_gdspy_tree()






