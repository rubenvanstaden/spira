import spira
from spira import param
from spira.lgm.route.path import __Path__


class Route(__Path__):

    ports = param.ElementListField(fdef_name='create_ports')
    # ports = param.PortListField(fdef_name='create_ports')

    input_term = param.DataField(fdef_name='create_port_input')
    output_term = param.DataField(fdef_name='create_port_output')

    def create_port_input(self):
        return None

    def create_port_output(self):
        return None

    def create_ports(self, ports):
        return ports


class RouteToCell(spira.Cell):

    shape = param.DataField()

    def create_elementals(self, elems):
        elems += spira.Polygons(shape=self.shape.points,
                                gdslayer=spira.Layer(number=88))
        return elems

    def create_ports(self, ports):
        ports += self.shape.input_term
        ports += self.shape.output_term
        return ports

