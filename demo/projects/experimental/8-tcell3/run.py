import spira
from spira import RDD
from spira import param
from spira import shapes
from spira.core.default.templates import ViaTemplate
from spira.lpe.primitives import Device


class TwoLayerRoute(spira.Cell):

    spacing = param.FloatField(default=RDD.BC.SPACING)

    wires = param.DataField(fdef_name='create_wires')
    vias = param.DataField(fdef_name='create_contacts')

    def create_wires(self):
        elems = spira.ElementList()
        b1 = shapes.BoxShape(center=[7.5, 0], width=15, height=5, gdslayer=RDD.CTL.LAYER)
        elems += shapes.Box(shape=b1)
        b2 = shapes.BoxShape(center=[32.5, 0], width=15, height=5, gdslayer=RDD.CTL.LAYER)
        elems += shapes.Box(shape=b2)
        b3 = shapes.BoxShape(center=[20, 0], width=20, height=5, gdslayer=RDD.COU.LAYER)
        elems += shapes.Box(shape=b3)
        return elems

    def create_contacts(self):
        elems = spira.ElementList()
        b1 = shapes.BoxShape(center=[12.5, 0], width=3, height=3, gdslayer=RDD.CC.LAYER)
        elems += shapes.Box(shape=b1)
        b2 = shapes.BoxShape(center=[27.5, 0], width=3, height=3, gdslayer=RDD.CC.LAYER)
        elems += shapes.Box(shape=b2)
        return elems

    def create_elementals(self, elems):

        for e in self.wires:
            elems += e

        for e in self.vias:
            elems += e

        return elems

    def create_ports(self, ports):

        ports += spira.Term(name='P1', midpoint=(0, 0), width=5)
        ports += spira.Term(name='P2', midpoint=(40, 0), width=5)

        return ports


# --------------------------------------------------------------------------------


if __name__ == '__main__':

    cell = TwoLayerRoute()

    # ViaTemplate().create_elementals(elems=via.elementals)

    cell.output()







