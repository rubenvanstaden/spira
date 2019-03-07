import spira
from spira import param
from spira.lgm.route.path import __Path__
from demo.pdks import ply


RDD = spira.get_rule_deck()


class Route(__Path__):

    ports = param.ElementalListField(fdef_name='create_ports')
    # ports = param.PortListField(fdef_name='create_ports')

    input_term = param.DataField(fdef_name='create_port_input')
    output_term = param.DataField(fdef_name='create_port_output')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_port_input(self):
        return None

    def create_port_output(self):
        return None

    def create_ports(self, ports):
        return ports


class RouteToCell(spira.Cell):

    shape = param.ShapeField()
    player = param.PhysicalLayerField(default=RDD.DEF.PDEFAULT)

    def create_elementals(self, elems):
        # elems += spira.Polygons(
        #     shape=self.shape,
        #     gdslayer=self.shape.gdslayer
        # )
        elems += ply.Polygon(
            points=self.shape.points,
            player=self.player
        )
        return elems

    def create_ports(self, ports):
        ports += self.shape.input_term
        ports += self.shape.output_term
        return ports

