import spira
from spira import param
from spira.lne.mesh import Mesh
from spira.lne.geometry import Geometry
from spira.core.initializer import ElementalInitializer


class Net(ElementalInitializer):
    """ Generates a graph from a list of polygon 
    elementals with a given mesh size. """

    name = param.StringField()
    layer = param.LayerField()
    lcar = param.FloatField(default=0)
    level = param.IntegerField(default=1)
    dimension = param.IntegerField(default=2)
    algorithm = param.IntegerField(default=6)

    polygons = param.ElementalListField()
    primitives = param.ElementalListField()
    route_nodes = param.ElementalListField()
    bounding_boxes = param.ElementalListField()

    graph = param.DataField(fdef_name='create_netlist_graph')

    def __init__(self, **kwargs):
        ElementalInitializer.__init__(self, **kwargs)

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
