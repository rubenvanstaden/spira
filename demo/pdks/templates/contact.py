from spira.kernel.cell import Cell
from spira.lgm.shape.basic import Rectangle
from spira.kernel.elemental.sref import SRef
from spira.kernel.cell import CellField
from spira.kernel.parameters.field.element_list import ElementList
from spira.kernel import parameters as param
from copy import copy, deepcopy
from spira.rdd.settings import get_rule_deck


RDD = get_rule_deck()


class __TemplateCell__(Cell):
    pass


class __TempatePrimitive__(__TemplateCell__):
    pass


class __TempateDevice__(__TemplateCell__):
    pass


class ViaTemplate(__TempatePrimitive__):
    """
    Via Template class to describe the boolean operations
    to be applied create a Device.
    """

    via_layer = param.LayerField()
    layer1 = param.LayerField()
    layer2 = param.LayerField()

    color = param.ColorField(default='#C0C0C0')

    def create_elementals(self, elems):

        NLayers = elems.get_dlayer(layer=self.via_layer)
        M1 = elems.get_mlayer(layer=self.layer1)
        M2 = elems.get_mlayer(layer=self.layer2)

        for D in NLayers:
            overlap_poly = deepcopy(D.ref.player)

            for M in M1:
                if overlap_poly | M.ref.player:
                    overlap_poly = overlap_poly | M.ref.player
                    D.ref.ports[0]._update(name=self.name, layer=M.ref.layer)

            for M in M2:
                if overlap_poly | M.ref.player:
                    overlap_poly = overlap_poly | M.ref.player
                    D.ref.ports[1]._update(name=self.name, layer=M.ref.layer)


if __name__ == '__main__':

    jj = JunctionTemplate(pcell=True)
    jj.construct_gdspy_tree()
