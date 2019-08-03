from spira.yevon.aspects.base import __Aspects__
from spira.yevon.geometry.ports.port_list import PortListParameter
from spira.core.transformable import Transformable
from spira.yevon.gdsii.elem_list import ElementListParameter
from spira.core.parameters.variables import *
from spira.yevon.geometry import shapes
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


class PortAspects(__Aspects__):
    """ Port properties that connects to layout structures. """

    ports = PortListParameter(fdef_name='__create_ports__', doc='List of ports to be added to the cell instance.')

    def __create_ports__(self, ports):
        return self.create_ports(ports)

    def create_ports(self, ports):
        return ports


class CellPortAspects(PortAspects):

    def __create_ports__(self, ports):
        for e in self.elements.polygons:
            ports += e.ports
        return self.create_ports(ports)


class TransformablePortAspects(PortAspects, Transformable):
    def __create_ports__(self, ports):
        ports = self.create_ports(ports)
        ports = ports.transform_copy(self.transformation)
        return ports


class SRefPortAspects(TransformablePortAspects):
    def create_ports(self, ports):
        ports = self.reference.ports
        ports = ports.transform_copy(self.transformation)
        ports = ports.move(self.midpoint)
        ports = ports.transform(-self.transformation)
        return ports


class PolygonPortAspects(TransformablePortAspects):
# class PolygonPortAspects(PortAspects):

    edge_ports = ElementListParameter()

    def create_edge_ports(self, edges):
        # shape = self.shape
        # FIXME: Cannot apply transforms when stretching.
        shape = self.shape.transform_copy(self.transformation)
        return shapes.shape_edge_ports(shape, self.layer, self.id_string(), center=shape.bbox_info.center, loc_name=self.location_name)

    def create_ports(self, ports):
        layer = RDD.GDSII.IMPORT_LAYER_MAP[self.layer]
        if layer.purpose.symbol == 'METAL':
            for edge in self.edge_ports:
                ports += edge
        # FIXME: This fails with CompoundTransforms, i.e. when stretching.
        # ports.transform(-self.transformation)
        return ports


