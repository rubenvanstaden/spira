import spira.all as spira
from spira.core import param
from spira.netex.mesh import Mesh
from spira.netex.geometry import Geometry
from spira.core.initializer import FieldInitializer
from spira.core.param.variables import *
from spira.core.elem_list import ElementalListField
from spira.core.descriptor import DataField
from spira.yevon.layer import LayerField


class Net(FieldInitializer):
    """ Generates a graph from a list of polygon
    elementals with a given mesh size. """

    name = StringField()
    layer = LayerField()
    lcar = FloatField(default=0)
    level = IntegerField(default=1)
    dimension = IntegerField(default=2)
    algorithm = IntegerField(default=6)

    polygons = ElementalListField()
    primitives = ElementalListField()
    route_nodes = ElementalListField()
    bounding_boxes = ElementalListField()

    graph = DataField(fdef_name='create_netlist_graph')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_netlist_graph(self):

        geom = Geometry(
            name=self.name,
            layer=self.layer,
            lcar=self.lcar,
            polygons=self.polygons,
            algorithm=self.algorithm,
            dimension=self.dimension
        )

        mesh = Mesh(
            name='{}'.format(self.layer),
            level=self.level,
            layer=self.layer,
            polygons=self.polygons,
            primitives=self.primitives,
            route_nodes=self.route_nodes,
            bounding_boxes=self.bounding_boxes,
            data=geom.create_mesh
        )

        return mesh.g
