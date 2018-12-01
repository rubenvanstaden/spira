import spira
import spira.kernel.parameters as param
from spira.rdd import get_rule_deck
from spira.kernel import utils
from spira import settings
from copy import copy, deepcopy

from .templates import __TempatePrimitive__

from spira.kernel.layer import Layer
from spira.kernel.elemental.polygons import Polygons
from spira.kernel.elemental.label import Label
from spira.kernel.elemental.port import Port
from spira.kernel.elemental.sref import SRef
from spira.kernel.parameters.field.element_list import ElementList


RDD = get_rule_deck()


class Via(__TempatePrimitive__):
    """
    Via Template class to describe the boolean operations
    to be applied create a Device.
    """

    surround = param.SurroundField(doc='I4 minimum surround by M5', min=1.0)
    width = param.WidthField(doc='Minimum contact width', min=0.8, max=1.2)
    length = param.FloatField(doc='Minimum contact length', default=0.30)

    via_layer = param.LayerField()
    layer1 = param.LayerField()
    layer2 = param.LayerField()

    color = param.ColorField(default='#C0C0C0')

    rule_polygons = param.FunctionField(fget_name='get_polygons')

    def create_primitive(self, D, M):
        from spira.lpe.primitives import ELayer

        el = ElementList()
        el += D
        el += M

        if self.surround.apply(el):
            name = 'ELayer_{}'.format(RDD.ERRORS.SPACING)
            ll = Layer(name='ERROR', number=M.ref.player.gdslayer.number, datatype=RDD.ERRORS.SPACING)
            epolygon = deepcopy(M.ref.player)
            epolygon.gdslayer = ll
            E = ELayer(name=name, layer=ll, player=epolygon)
            M.ref += SRef(E)
            D.ref.player.gdslayer.datatype = 101

    def create_elementals(self, elems):
        print('\n------ ViaTemplate ------')

        DLayers = elems.get_dlayer(layer=self.via_layer)
        M1 = elems.get_mlayer(layer=self.layer1)
        M2 = elems.get_mlayer(layer=self.layer2)

        for D in DLayers:
            overlap_poly = deepcopy(D.ref.player)

            for M in M1:
                if overlap_poly | M.ref.player:
                    overlap_poly = overlap_poly | M.ref.player
                    self.create_primitive(D, M)

            for M in M2:
                if overlap_poly | M.ref.player:
                    overlap_poly = overlap_poly | M.ref.player
                    self.create_primitive(D, M)


