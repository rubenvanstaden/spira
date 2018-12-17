import spira
from spira import param
from copy import copy, deepcopy


RDD = spira.get_rule_deck()


class __TemplateCell__(spira.Cell):
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
