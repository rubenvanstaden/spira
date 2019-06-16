from spira.log import SPIRA_LOG as LOG
from spira.yevon.filters.filter import Filter
# from spira.yevon.process.layer_list import LayerList, LayerListField
from spira.yevon.process.gdsii_layer import LayerList, LayerListField
from spira.yevon.gdsii.elem_list import ElementalListField
from spira.yevon.geometry.ports.port_list import PortListField
from spira.yevon.vmodel.elementals import reference_metal_blocks
from spira.yevon.geometry.ports import Port, ContactPort
from spira.yevon.utils import geometry
from spira.yevon.geometry.ports.port import BranchPort
from copy import deepcopy
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = [
    'NetProcessLabelFilter',
    'NetDeviceLabelFilter',
    'NetBlockLabelFilter',
    'NetEdgeFilter'
]


class __NetFilter__(Filter):
    pass


class NetProcessLabelFilter(__NetFilter__):
    """  """

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


class NetEdgeFilter(__NetFilter__):
    """  """

    process_polygons = ElementalListField()

    def __filter___Net____(self, item):

        ELM_TYPE = {1: 'line', 2: 'triangle'}

        # print('Triangles:')
        # print(item.triangles)
        # print('Lines:')
        # print(item.lines)
        # print('Physical Lines:')
        # print(item.physical_lines)
        # print('Field Data:')
        # for k, v in item.mesh_data.field_data.items():
        #     print(k, v)
        # # print(item.process_lines())
        # # print(item.get_triangles_connected_to_line())

        for key, value in item.mesh_data.field_data.items():

            # line_id = key.split('_')[0]
            # line_id = key[:-2]
            line_id = key[1]
            print(line_id)
            
            elm_type = ELM_TYPE[value[1]]
            if elm_type == 'line':

                for e in self.process_polygons:
                    pid = e.shape.hash_string
    
                    # if line_id == pid:
                    if line_id == 'b':
                        i = item.physical_lines.index(value[0])
                        line = item.lines[i]

                        for n, triangle in enumerate(item.triangles):
                            if (line[0] in triangle) and (line[1] in triangle):
                                print('YESSSSSSS')
                                print(triangle)
                                
                                item.g.node[n]['process_polygon'] = e
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
                if isinstance(D, ContactPort):
                    if D.encloses(points):
                        # if 'device_reference' in item.g.node[n]:
                        #     # D = item.g.node[n]['device_reference']
                        #     polygon = item.g.node[n]['process_polygon']
                        #     # position = item.g.node[n]['position']
                        #     position = deepcopy(D.midpoint)
                        #     display = item.g.node[n]['display']
                        #     item.add_new_node(n=n, D=D, polygon=polygon, position=position, display=display)

                        #     # C = item.g.node[n]['device_reference']
                        #     # port = BranchPort(
                        #     #     name='D1',
                        #     #     midpoint=C.midpoint,
                        #     #     process=RDD.PROCESS.M2,
                        #     #     purpose=RDD.PURPOSE.PORT.BRANCH
                        #     # )
                        #     # item.g.node[n]['device_reference'] = port

                        # else:
                            # item.g.node[n]['device_reference'] = D
                            # item.g.node[n]['display'] = RDD.DISPLAY.STYLE_SET[D.layer]
                        item.g.node[n]['device_reference'] = D
                        item.g.node[n]['display'] = RDD.DISPLAY.STYLE_SET[D.layer]
                elif isinstance(D, Port):
                    if D.purpose == RDD.PURPOSE.PORT.EDGE_ENABLED:
                        if D.encloses(points):
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



