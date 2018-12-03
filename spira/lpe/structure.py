import spira
from spira.kernel import parameters as param
from spira.lgm.booleans import merge
from spira.lpe.layers import *
from spira.lrc.rules import *
from spira.lrc.checking import Rules
from spira.lpe.containers import __CellContainer__

from spira.lne.graph import Graph
from spira.lne.mesh import Mesh
from spira.lne.geometry import Geometry


RDD = spira.get_rule_deck()


class ComposeMLayers(__CellContainer__):

    cell_elems = param.ElementListField()

    mlayers = param.DataField(fdef_name='create_mlayers')

    def _merged_layer(self, flat_metals):
        points = []
        elems = spira.ElementList()
        for p in flat_metals:
            for pp in p.polygons:
                points.append(pp)
        if points:
            merged_points = merge(points=points)
            for pts in merged_points:
                elems += spira.Polygons(polygons=[pts])
        return elems

    def create_mlayers(self):
        elems = spira.ElementList()
        for layer in (*RDD.METALS.layers, *RDD.GROUND.layers, RDD.MOAT.number):

            flat_elems = self.cell_elems.flat_copy()
            metal_elems = flat_elems.get_polygons(layer=layer)

            if metal_elems:
                c_mlayer = CMLayers(layer=spira.Layer(number=layer))

                for i, ply in enumerate(self._merged_layer(metal_elems)):
                    ml = MLayer(name='MLayer_{}_{}'.format(layer, i),
                                points=ply.polygons,
                                number=layer)
                    c_mlayer += spira.SRef(ml)

                elems += spira.SRef(c_mlayer)

        return elems

    def create_elementals(self, elems):

        for lcell in self.mlayers:
            elems += lcell

        return elems


class ComposeNLayer(ComposeMLayers):

    cell_elems = param.ElementListField()

    level = param.IntegerField()

    nlayers = param.DataField(fdef_name='create_nlayers')

    def create_nlayers(self):
        elems = ElementList()
        for layer in RDD.VIAS.layers:

            flat_elems = self.cell_elems.flat_copy()
            via_elems = flat_elems.get_polygons(layer=layer)

            if via_elems:
                c_nlayer = CNLayers(layer=spira.Layer(layer))

                for i, ply in enumerate(via_elems):
                    ml = NLayer(name='Via_NLayer_{}_{}'.format(layer, i),
                                points=ply.polygons,
                                midpoint=ply.center,
                                number=layer)
                    c_nlayer += spira.SRef(ml)

                elems += SRef(c_nlayer)

        return elems

    def create_elementals(self, elems):

        super().create_elementals(elems)

        # Only add it if its a Device.
        if self.level == 1:
            for lcell in self.nlayers:
                elems += lcell

        return elems


class ComposeGLayer(ComposeNLayer):

    plane_elems = param.ElementListField() # Elementals like skyplanes and groundplanes.
    ground_layer = param.DataField(fdef_name='create_merged_ground_layers')

    def create_merged_ground_layers(self):
        points = []
        for p in self.plane_elems.flat_copy():
            for pp in p.polygons:
                points.append(pp)
        if points:
            ll = Layer(number=RDD.GROUND.M4.LAYER, datatype=6)
            merged_ply = UnionPolygons(polygons=points, gdslayer=ll)
            return merged_ply
        return None

    def create_elementals(self, elems):

        super().create_elementals(elems)

        if self.level == 1:
            box = self.cell.bbox
            # box.move(origin=box.center, destination=(0,0))

            gnd_full = self.ground_layer

            if gnd_full:
                gnd = gnd_full | box

                c_glayer = CGLayers(layer=spira.Layer(gnd.gdslayer))
                name = 'GLayer_{}'.format(gnd.gdslayer.number)
                gnd_layer = GLayer(name=name, layer=gnd.gdslayer, player=gnd)
                c_glayer += spira.SRef(gnd_layer)
                elems += spira.SRef(c_glayer)

        return elems


class ConnectDesignRules(ComposeGLayer):

    metal_elems = param.ElementListField()

    def create_elementals(self, elems):

        super().create_elementals(elems)

        incorrect_elems = ElementList()
        correct_elems = ElementList()

        for rule in RDD.RULES.elementals:
            if not rule.apply(elems):
                for composed_lcell in elems:
                    for lcell in composed_lcell.ref.elementals.sref:
                        if lcell.ref.layer.number == rule.layer1.number:
                            correct_elems += lcell
        return elems


class __StructureCell__(ConnectDesignRules):
    """
    Add a GROUND bbox to Device for primitive and
    DRC detection, since GROUND is only in Mask Cell.
    """

    level = param.IntegerField(default=1)

    device_elems = param.ElementListField()

    devices = param.DataField(fdef_name='create_device_layers')
    terminals = param.DataField(fdef_name='create_terminal_layers')

    def create_device_layers(self):
        box = self.cell.bbox
        box.move(origin=box.center, destination=(0,0))

        B = DLayer(blayer=box, device_elems=self.cell.elementals)
        Bs = SRef(B)
        Bs.move(origin=(0,0), destination=self.cell.bbox.center)

        return Bs

    def create_terminal_layers(self):
        flat_elems = self.cell_elems.flat_copy()
        port_elems = flat_elems.get_polygons(layer=RDD.TERM)
        label_elems = flat_elems.labels

        elems = ElementList()
        for port in port_elems:
            for label in label_elems:

                lbls = label.text.split(' ')
                s_p1, s_p2 = lbls[1], lbls[2]
                p1, p2 = None, None

                if s_p1 in RDD.METALS.keys: 
                    layer = RDD.METALS[s_p1].LAYER
                    p1 = spira.Layer(name=lbls[0], number=layer, datatype=RDD.TEXT)

                if s_p2 in RDD.METALS.keys: 
                    layer = RDD.METALS[s_p2].LAYER
                    p2 = spira.Layer(name=lbls[0], number=layer, datatype=RDD.TEXT)

                if p1 and p2:
                    if label.point_inside(polygon=port.polygons[0]):
                        term = TLayer(points=port.polygons,
                                    layer1=p1,
                                    layer2=p2,
                                    number=RDD.TERM,
                                    midpoint=label.position)

                        term.ports[0].name = 'P1_{}'.format(label.text)
                        term.ports[1].name = 'P2_{}'.format(label.text)

                        elems += SRef(term)

        return elems

    def create_elementals(self, elems):

        super().create_elementals(elems)

        elems += self.devices

        for term in self.terminals:
            elems += term

        return elems




