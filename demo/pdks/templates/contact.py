import spira
from spira import param
from copy import copy, deepcopy


RDD = spira.get_rule_deck()


class __TemplateCell__(spira.Cell):
    pass


class __TempatePrimitive__(__TemplateCell__):
    pass


class ViaTemplate(__TempatePrimitive__):

    layer1 = param.LayerField(number=3)
    layer2 = param.LayerField(number=8)
    via_layer = param.LayerField(number=9)

    def create_elementals(self, elems):
        M1 = spira.ElementList()
        M2 = spira.ElementList()
        contacts = spira.ElementList()

        for e in elems:
            if e.player.purpose == RDD.PURPOSE.METAL:
                if e.player.layer == self.layer1:
                    M1 += e
                elif e.player.layer == self.layer2:
                    M2 += e
            if e.player.purpose == RDD.PURPOSE.PRIM.VIA:
                if e.player.layer == self.via_layer:
                    contacts += e

        for D in contacts:
            for M in M1:
                if D.polygon | M.polygon:
                    pp = D.polygon | M.polygon
                    # TODO: Apply DRC enclosure rule here.
                    D.ports[0]._update(name=D.name, layer=M.player.layer)
            for M in M2:
                if D.polygon | M.polygon:
                    pp = D.polygon | M.polygon
                    # TODO: Apply DRC enclosure rule here.
                    D.ports[1]._update(name=D.name, layer=M.player.layer)
        return elems

