import spira
import numpy as np
from spira import param, shapes
from spira.lpe import mask
from demo.pdks import ply
from spira.lpe.containers import __CellContainer__
from spira.lne.net import Net
from copy import copy, deepcopy
from spira.lpe.mask_layers import Metal
# from spira.lpe.devices import __Device__


RDD = spira.get_rule_deck()


class __PCell__(__CellContainer__):
    """
    Decorates all elementas with purpose metal with
    LCells and add them as elementals to the new class.
    """

    metals = param.ElementalListField()
    contacts = param.ElementalListField()

    level = param.IntegerField(default=2)
    lcar = param.IntegerField(default=0.1)
    algorithm = param.IntegerField(default=6)

    metal_layers = param.DataField(fdef_name='create_metal_layers')
    merged_layers = param.DataField(fdef_name='create_merged_layers')
    get_primitives = param.DataField(fdef_name='get_primitives_function')

    boxes = param.ElementalListField(fdef_name='create_boxes')

    def get_metal_polygons(self, pl):
        elems = self.merged_layers
        ply_elems = spira.ElementList()
        for M in elems:
            if M.layer.is_equal_number(pl.layer):
                ply_elems += M.polygon
        return ply_elems

    def create_metals(self, elems):
        return elems

    def create_contacts(self, elems):
        return elems

    def create_merged_layers(self):

        params = {}
        elems = spira.ElementList()
        for M in self.metals:
            if M.player not in params.keys():
                params[M.player] = M.polygon.polygons
            else:
                for pp in M.polygon.polygons:
                    params[M.player].append(pp)

        for player, points in params.items():
            shape = shapes.Shape(points=points)
            shape.apply_merge

            # Have to enumerate over all merged points,
            # to create unique polyogn IDs.
            for i, pts in enumerate(shape.points):
                elems += ply.Polygon(
                    name='box_{}_{}_{}'.format(player, i, self.name),
                    player=player,
                    points=[pts],
                    level=self.level
                )

        return elems

    def create_nets(self, nets):
        for pl in RDD.PLAYER.get_physical_layers(purposes='METAL'):
            metal_elems = self.get_metal_polygons(pl)
            if metal_elems:
                net = Net(
                    name='{}'.format(pl.layer.number),
                    lcar=self.lcar,
                    level=self.level,
                    algorithm=self.algorithm,
                    layer=pl.layer,
                    polygons=metal_elems,
                    primitives=self.get_primitives,
                    bounding_boxes=self.boxes
                )
                nets += net.graph
        return nets
