import spira
import numpy as np
from spira import param, shapes
from spira.lpe import mask
from demo.pdks import ply
from spira.lpe.containers import __CellContainer__
from spira.lne.net import Net
from copy import copy, deepcopy


RDD = spira.get_rule_deck()


class __Mask__(__CellContainer__):
    level = param.IntegerField(default=1)

    alias = param.StringField()
    player = param.PhysicalLayerField()
    level = param.IntegerField(default=1)
    lcar = param.IntegerField(default=0.1)
    algorithm = param.IntegerField(default=6)

    metals = param.DataField(fdef_name='create_flatten_metals')
    merged_layers = param.DataField(fdef_name='create_merged_layers')

    def create_flatten_metals(self):
        metal_elems = spira.ElementList()
        R = self.cell.routes.flat_copy()
        B = self.cell.boxes.flat_copy()
        Rm = R.get_polygons(layer=self.player.layer)
        Bm = B.get_polygons(layer=self.player.layer)
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
        player = None
        for k, v in RDD.PLAYER.items:
            if v.layer == self.player.layer:
                player = v

        for i, poly in enumerate(self.merged_layers):
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
