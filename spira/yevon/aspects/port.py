from spira.yevon.aspects.base import __Aspects__
from spira.yevon.geometry.ports.port_list import PortListParameter
from spira.core.transformable import Transformable
from spira.core.transformation import ReversibleTransform
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
    """ Factory class that gets all cell instance 
    ports and related polygon ports, such as edges. """

    def __create_ports__(self, ports):
        for e in self.elements.polygons:
            ports += e.edge_ports
        # for e in self.elements.polygons:
        #     ports += e.ports
        for e in self.elements.sref:
            ports += e.ports
        return self.create_ports(ports)


class TransformablePortAspects(PortAspects, Transformable):
    """ Factory class that automatically transform ports. """

    def __create_ports__(self, ports):
        ports = self.create_ports(ports)
        ports = ports.transform_copy(self.transformation)
        return ports


class SRefPortAspects(TransformablePortAspects):
    """ Factory class that moves cell reference
    ports into position when they are accesse. """

    def create_ports(self, ports):
        ports = self.reference.ports
        ports = ports.transform_copy(self.transformation)
        ports = ports.move(self.midpoint)
        ports = ports.transform(-self.transformation)
        return ports


# FIXME: Run when stretching.
class PolygonPortAspects(TransformablePortAspects):

    edge_ports = ElementListParameter()

    def create_edge_ports(self, edge_ports):
        # shape = self.shape
        shape = self.shape.transform_copy(self.transformation)
        layer = RDD.GDSII.IMPORT_LAYER_MAP[self.layer]
        if layer.purpose.symbol in ['METAL', 'DEVICE_METAL', 'CIRCUIT_METAL']:
            edge_ports = shapes.shape_edge_ports(shape, self.layer, self.id_string(), center=shape.bbox_info.center, loc_name=self.alias + ':')
        # if isinstance(self.transformation, ReversibleTransform):
        #     edge_ports.reverse_transform(self.transformation)
        return edge_ports

    # def create_ports(self, ports):
    #     layer = RDD.GDSII.IMPORT_LAYER_MAP[self.layer]
    #     # TODO: Move this to the RDD, so I can select which purposes must be edge-generators.
    #     if layer.purpose.symbol in ['METAL', 'DEVICE_METAL', 'CIRCUIT_METAL']:
    #         for edge in self.edge_ports:
    #             ports += edge
    #     # FIXME: This fails with CompoundTransforms, i.e. when stretching.
    #     if isinstance(self.transformation, ReversibleTransform):
    #         ports.reverse_transform(self.transformation)
    #     return ports


# # FIXME: Run default (not stretching).
# class PolygonPortAspects(TransformablePortAspects):

#     edge_ports = ElementListParameter()

#     def create_edge_ports(self, edges):
#         shape = self.shape.transform_copy(self.transformation)
#         return shapes.shape_edge_ports(shape, self.layer, self.id_string(),
#             center=shape.bbox_info.center, loc_name=self.name)

#     def create_ports(self, ports):
#         layer = RDD.GDSII.IMPORT_LAYER_MAP[self.layer]
#         if layer.purpose.symbol in ['METAL', 'DEVICE_METAL', 'CIRCUIT_METAL']:
#             for edge in self.edge_ports:
#                 ports += edge
#         return ports




