import spira
from spira import param, shapes
from demo.pdks import ply
from spira.rdd import get_rule_deck
from spira.lpe.containers import __CellContainer__


RDD = get_rule_deck()


class __Mask__(__CellContainer__):

    m_name = param.StringField()
    player = param.PhysicalLayerField()
    level = param.IntegerField(default=1)
    cell_elems = param.ElementListField()

    metals = param.DataField(fdef_name='create_flatten_metals')
    merged_layers = param.DataField(fdef_name='create_merged_layers')

    def create_flatten_metals(self):
        flat_elems = self.cell_elems.flat_copy()
        metal_elems = flat_elems.get_polygons(layer=self.player.layer)
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
            assert isinstance(poly, spira.Polygons)
            if player is not None:
                ml = ply.Polygon(
                    name='ply_{}_{}'.format(self.m_name, i),
                    layer1=player.layer,
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






