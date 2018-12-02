from spira.kernel.cell import Cell
from spira.kernel.elemental.sref import SRef
from spira.kernel.cell import CellField
from spira.kernel import parameters as param
from copy import copy, deepcopy
from spira.rdd.mitll import RDD


class __TemplateCell__(Cell):
    pass


class __TempatePrimitive__(__TemplateCell__):
    pass


class __TempateDevice__(__TemplateCell__):
    pass


class JunctionTemplate(__TempateDevice__):

    gdsdatatype = param.IntegerField(default=3)

    def create_elementals(self, elems):

        i4 = SRef(RDD.VIAS.I4.PCELL, origin=(0,0))
        i5 = SRef(RDD.VIAS.I5.PCELL, origin=(0,0))
        j5 = SRef(RDD.VIAS.J5.PCELL, origin=(0,0))
        c5 = SRef(RDD.VIAS.C5.PCELL, origin=(0,0))

        elems += i4
        elems += i5
        elems += j5
        elems += c5

        return elems


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
                    D.ref.ports[0].update(name=self.name, layer=M.ref.layer)

            for M in M2:
                if overlap_poly | M.ref.player:
                    overlap_poly = overlap_poly | M.ref.player
                    D.ref.ports[1].update(name=self.name, layer=M.ref.layer)


# class DeviceTemplate(__TempateDevice__):

#     device_elems = param.ElementListField()

#     def create_elementals(self, elems):

#         super().create_elementals(elems)

#         # TODO: Do DRC and ERC checking here.
#         sref_elems = self.device_elems[0].ref.get_srefs()
#         for S in sref_elems:
#             if isinstance(S.ref, DLayer):
#                 elems += S

#         # for S in self.device_elems:
#         #     for S_prim in S.ref.elementals:
#         #         if isinstance(S_prim.ref, DLayer):
#         #             elems += S_prim

#         return elems

