import spira
from spira import param
from spira import shapes
from spira.core.default.templates import ViaTemplate
from spira.lpe.primitives import Device
from spira.lpe.primitives import SLayout


RDD = spira.get_rule_deck()


class ViaPCell(spira.Cell):

    spacing = param.FloatField(default=RDD.BC.SPACING)

    width = param.FloatField(default=RDD.BAS.WIDTH)
    height = param.FloatField(default=RDD.BAS.WIDTH)

    metal_layer_1 = param.DataField(default=RDD.BAS)
    metal_layer_2 = param.DataField(default=RDD.COU)
    contact_layer = param.DataField(default=RDD.BC)

    def validate_parameters(self):
        if self.width < self.metal_layer_1.WIDTH:
            return False
        if self.width < self.metal_layer_2.WIDTH:
            return False
        return True

    def create_elementals(self, elems):

        b1 = shapes.BoxShape(width=self.width,
                           height=self.height,
                           gdslayer=self.metal_layer_1.LAYER)
        elems += shapes.Box(shape=b1)

        b2 = shapes.BoxShape(width=self.width,
                           height=self.height,
                           gdslayer=self.metal_layer_2.LAYER)
        elems += shapes.Box(shape=b2)

        b3 = shapes.BoxShape(width=self.width - self.spacing,
                           height=self.width - self.spacing,
                           gdslayer=self.contact_layer.LAYER)
        elems += shapes.Box(shape=b3)

        return elems

    def create_ports(self, ports):

        ports += spira.Term(name='P1', midpoint=(-self.width/2, 0), width=self.width, orientation=0)
        ports += spira.Term(name='P2', midpoint=(self.width/2, 0), width=self.width, orientation=0)

        return ports


if __name__ == '__main__':

    cell = ViaPCell()

    # Before sending the cell to a template, we first
    # have to convert it to a SLayout.
    # sl = SLayout(cell=cell, level=2)
    # sl.construct_gdspy_tree()

    # ViaTemplate().create_elementals(elems=sl.elementals)
    cell.output()








