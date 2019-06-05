from spira.log import SPIRA_LOG as LOG
from spira.yevon.filters.filter import Filter
from spira.yevon.process.layer_list import LayerList, LayerListField
from spira.yevon.gdsii.elem_list import ElementalListField
from spira.yevon.geometry.ports.port_list import PortListField
from spira.yevon.vmodel.elementals import reference_metal_blocks
from spira.yevon.geometry.ports import Port
from spira.yevon.utils import geometry
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = ['NetProcessLabelFilter', 'NetBlockLabelFilter', 'NetDeviceLabelFilter']


class __NetFilter__(Filter):
    pass


class NetProcessLabelFilter(__NetFilter__):
    process_polygons = ElementalListField()

    def __filter___Net____(self, item):
        triangles = item.process_triangles()
        for key, nodes in triangles.items():
            for n in nodes:
                for e in self.process_polygons:
                    if e.encloses(item.g.node[n]['position']):
                        item.g.node[n]['process_polygon'] = e
                        item.g.node[n]['display'] = RDD.DISPLAY.STYLE_SET[e.layer]
        return item

    def __repr__(self):
        return "[SPiRA: NetLabelFilter] (layer count {})".format(0)


class NetBlockLabelFilter(__NetFilter__):
    references = ElementalListField()

    def __filter___Net____(self, item):
        for S in self.references:
            for e in reference_metal_blocks(S):
                for n in item.g.nodes():
                    if e.encloses(item.g.node[n]['position']):
                        item.g.node[n]['device_reference'] = S
                        item.g.node[n]['display'] = RDD.DISPLAY.STYLE_SET[e.layer]
        return item

    def __repr__(self):
        return "[SPiRA: NetLabelFilter] (layer count {})".format(0)


class NetDeviceLabelFilter(__NetFilter__):
    """ Add 'enabled' ports to the net. """

    device_ports = PortListField()

    def __filter___Net____(self, item):
        for n, triangle in item.triangle_nodes().items():
            points = [geometry.c2d(item.mesh_data.points[i]) for i in triangle]
            for D in self.device_ports:
                if isinstance(D, Port):
                    if D.purpose == RDD.PURPOSE.PORT.EDGE_ENABLED:
                        if D.encloses(points):
                            print(D)
                            item.g.node[n]['device_reference'] = D
                            item.g.node[n]['display'] = RDD.DISPLAY.STYLE_SET[D.layer]
                # else:
                #     for p in D.ports:
                #         if p.gds_layer.number == item.layer.number:
                #             if p.encloses(points):
                #                 if 'device_reference' in item.g.node[n]:
                #                     item.add_new_node(n, D, p.midpoint)
                #                 else:
                #                     # TODO: Maybe to item.node_device = D
                #                     item.g.node[n]['device_reference'] = D
        return item

    def __repr__(self):
        return "[SPiRA: NetLabelFilter] (layer count {})".format(0)

