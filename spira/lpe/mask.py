import spira
from spira import param, shapes
from demo.pdks import ply
from spira.rdd import get_rule_deck
from spira.lpe.containers import __CellContainer__
from copy import copy, deepcopy

from spira.gdsii.utils import scale_polygon_down as spd
from spira.gdsii.utils import scale_polygon_up as spu


RDD = get_rule_deck()


class __Mask__(__CellContainer__):

    alias = param.StringField()
    player = param.PhysicalLayerField()
    level = param.IntegerField(default=1)

    metals = param.DataField(fdef_name='create_flatten_metals')
    merged_layers = param.DataField(fdef_name='create_merged_layers')

    # def create_boxes(self, boxes):
    #     return boxes

    def create_flatten_metals(self):
        # E = self.cell.elementals.flat_copy()
        R = self.cell.routes.flat_copy()
        B = self.cell.boxes.flat_copy()
        # Em = E.get_polygons(layer=self.player.layer)
        Rm = R.get_polygons(layer=self.player.layer)
        Bm = B.get_polygons(layer=self.player.layer)
        metal_elems = spira.ElementList()
        # for e in Em:
        #     metal_elems += e
        for e in Rm:
            metal_elems += e
        for e in Bm:
            metal_elems += e
        return metal_elems

    def create_merged_layers(self):
        points = []
        elems = spira.ElementList()
        for p in self.metals:
            assert isinstance(p, spira.Polygons)
            for pp in p.polygons:
                points.append(pp)
        if points:
            shape = shapes.Shape(points=points)
            shape.apply_merge
            for pts in shape.points:
                elems += spira.Polygons(shape=[pts])
        return elems

    def create_elementals(self, elems):
        # TODO: Map the gdslayer to a physical layer in the RDD.
        player = None
        for k, v in RDD.PLAYER.items:
            if v.layer == self.player.layer:
                player = v

        for i, poly in enumerate(self.merged_layers):
        # for i, poly in enumerate(self.metals):

        # R = self.cell.routes.flat_copy()
        # Rm = R.get_polygons(layer=self.player.layer)
        # for i, poly in enumerate(Rm):

        # R = self.cell.elementals.flat_copy()
        # Rm = R.get_polygons(layer=self.player.layer)
        # for i, poly in enumerate(Rm):
            assert isinstance(poly, spira.Polygons)
            if player is not None:
                ml = ply.Polygon(
                    name='ply_{}_{}'.format(self.alias, i),
                    player=player,
                    points=poly.polygons,
                    level=self.level
                )
                elems += ml
        return elems


class Metal(__Mask__):
    pass


class Native(__Mask__):
    pass






