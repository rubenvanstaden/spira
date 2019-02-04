import spira
from spira import param
from spira import shapes
from spira.lpe.layers import *
from spira.lrc.rules import *
from spira.lrc.checking import Rules
from spira.lpe.containers import __CellContainer__

from spira.lne.graph import Graph
from spira.lne.mesh import Mesh
from spira.lne.geometry import Geometry


RDD = spira.get_rule_deck()


class ComposeMLayers(__CellContainer__):
    """
    Decorates all elementals with purpose metal with
    LCells and add them as elementals to the new class.
    """

    cell_elems = param.ElementListField()

    mlayers = param.DataField(fdef_name='create_mlayers')

    def _merge_layers(self, flat_metals):
        points = []
        elems = spira.ElementList()
        for p in flat_metals:
            for pp in p.polygons:
                points.append(pp)
        if points:
            from spira.gdsii.utils import scale_polygon_down as spd
            points = spd(points)
            shape = shapes.Shape(points=points)
            shape.apply_merge
            for pts in shape.points:
                pts = spd([pts])
                elems += spira.Polygons(shape=pts)
        return elems

    def create_mlayers(self):
        elems = spira.ElementList()
        # players = RDD.PLAYER.get_physical_layers(purpose_symbol=['METAL', 'GROUND', 'MOAT'])
        flat_elems = self.cell_elems.flat_copy()
        for pl in RDD.PLAYER.get_physical_layers(purposes='METAL'):

            metal_elems = flat_elems.get_polygons(layer=pl.layer)

            if metal_elems:
                c_mlayer = CMLayers(layer=pl.layer)
                for i, ply in enumerate(self._merge_layers(metal_elems)):
                    ml = MLayer(name='MLayer_{}_{}_{}_{}'.format(pl.layer.number,
                                                                 self.cell.name,
                                                                 self.cell.id, i),
                                points=ply.polygons,
                                number=pl.layer.number)
                    c_mlayer += spira.SRef(ml)
                elems += spira.SRef(c_mlayer)
        return elems

    def create_elementals(self, elems):

        # TODO: Apply DRC checking between metals, before being placed.

        for lcell in self.mlayers:
            elems += lcell

        # FIXME: Allow this operation.
        # elems += self.mlayers

        return elems


class ComposeNLayer(ComposeMLayers):
    """
    Decorates all elementas with purpose via with
    LCells and add them as elementals to the new class.
    """

    cell_elems = param.ElementListField()

    level = param.IntegerField(default=1)

    nlayers = param.DataField(fdef_name='create_nlayers')

    def create_nlayers(self):
        elems = ElementList()
        flat_elems = self.cell_elems.flat_copy()
        for pl in RDD.PLAYER.get_physical_layers(purposes='VIA'):

            via_elems = flat_elems.get_polygons(layer=pl.layer)

            if via_elems:
                c_nlayer = CNLayers(layer=pl.layer)
                for i, ply in enumerate(via_elems):
                    ml = NLayer(name='Via_NLayer_{}_{}_{}'.format(pl.layer.number, self.cell.name, i),
                                points=ply.polygons,
                                midpoint=ply.center,
                                number=pl.layer.number)
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
            ll = Layer(number=RDD.GDSII.GPLAYER, datatype=6)
            merged_ply = UnionPolygons(polygons=points, gdslayer=ll)
            return merged_ply
        return None

    def create_elementals(self, elems):

        super().create_elementals(elems)

        if self.level == 1:
            if self.ground_layer:
                box = self.cell.bbox
                # box.move(midpoint=box.center, destination=(0,0))

                gnd = self.ground_layer | box
                if gnd:
                    c_glayer = CGLayers(layer=gnd.gdslayer)
                    name = 'GLayer_{}_{}'.format(self.cell.name, gnd.gdslayer.number)
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
        box.move(midpoint=box.center, destination=(0,0))

        B = DLayer(blayer=box, device_elems=self.cell.elementals)
        Bs = SRef(B)
        Bs.move(midpoint=(0,0), destination=self.cell.bbox.center)

        return Bs

    def create_terminal_layers(self):
#         flat_elems = self.cell_elems.flat_copy()
#         port_elems = flat_elems.get_polygons(layer=RDD.PURPOSE.TERM)
#         label_elems = flat_elems.labels
# 
#         elems = ElementList()
#         for port in port_elems:
#             for label in label_elems:
# 
#                 lbls = label.text.split(' ')
#                 s_p1, s_p2 = lbls[1], lbls[2]
#                 p1, p2 = None, None
# 
#                 if s_p1 in RDD.METALS.keys: 
#                     layer = RDD.METALS[s_p1].LAYER
#                     p1 = spira.Layer(name=lbls[0], number=layer, datatype=RDD.GDSII.TEXT)
# 
#                 if s_p2 in RDD.METALS.keys: 
#                     layer = RDD.METALS[s_p2].LAYER
#                     p2 = spira.Layer(name=lbls[0], number=layer, datatype=RDD.GDSII.TEXT)
# 
#                 if p1 and p2:
#                     if label.point_inside(polygon=port.polygons[0]):
#                         term = TLayer(points=port.polygons,
#                                     layer1=p1,
#                                     layer2=p2,
#                                     number=RDD.GDSII.TERM,
#                                     midpoint=label.position)
# 
#                         term.ports[0].name = 'P1_{}'.format(label.text)
#                         term.ports[1].name = 'P2_{}'.format(label.text)
# 
#                         elems += SRef(term)

        elems = ElementList()

        for p in self.cell.ports:
            if isinstance(p, spira.Term):
                term = TLayer(points=p.polygon.polygons,
#                               layer1=p1,
#                               layer2=p2,
                              number=RDD.PURPOSE.TERM.datatype,
                              midpoint=p.label.position)

                term.ports[0].name = 'P1_{}'.format(1)
                term.ports[1].name = 'P2_{}'.format(2)

                elems += SRef(term)
        return elems

    def create_elementals(self, elems):

        super().create_elementals(elems)

#         elems += self.devices

        # for term in self.terminals:
        #     elems += term

        return elems

    def create_ports(self, ports):

#         for t in self.cell.terms:
#             ports += t

        return ports












