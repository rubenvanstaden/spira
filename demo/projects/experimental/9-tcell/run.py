import spira
from spira import RDD
from spira import param
from spira import shapes
from spira.core.default.templates import ViaTemplate
from spira.lpe.primitives import Device
from demo.projects.tutorials.pcell_contact.run import ViaPCell
from spira.lpe.primitives import SLayout


class TwoLayerRoute(spira.Cell):

    spacing = param.FloatField(default=RDD.BC.SPACING)

    wires = param.DataField(fdef_name='create_wires')

    def create_wires(self):
        elems = spira.ElementList()
        b1 = shapes.BoxShape(center=[7.5, 0], width=15, height=5, gdslayer=RDD.CTL.LAYER)
        elems += shapes.Box(shape=b1)
        b2 = shapes.BoxShape(center=[32.5, 0], width=15, height=5, gdslayer=RDD.CTL.LAYER)
        elems += shapes.Box(shape=b2)
        b3 = shapes.BoxShape(center=[20, 0], width=20, height=5, gdslayer=RDD.COU.LAYER)
        elems += shapes.Box(shape=b3)
        return elems

    def create_elementals(self, elems):

        via = ViaPCell(width=5, height=5,
                       metal_layer_1=RDD.COU,
                       metal_layer_2=RDD.CTL,
                       contact_layer=RDD.CC)

        elems += spira.SRef(structure=via, origin=[12.5, 0])
        elems += spira.SRef(structure=via, origin=[27.5, 0])

        for e in self.wires:
            elems += e

        return elems

    def create_ports(self, ports):

        ports += spira.Term(name='P1', midpoint=(0, 0), width=5, orientation=90)
        ports += spira.Term(name='P2', midpoint=(40, 0), width=5, orientation=90)

        return ports


# ------------------------------------------------------------------------------------------


if __name__ == '__main__':

    c1 = TwoLayerRoute()
    c1.output()

    # cell = SLayout(cell=c1, level=2)

    # cell.output()







