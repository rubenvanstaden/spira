from spira.log import SPIRA_LOG as LOG
from spira.yevon.filters.filter import Filter
from spira.yevon.process.gdsii_layer import LayerList, LayerListParameter
from spira.yevon.gdsii.elem_list import ElementListParameter
from spira.yevon.geometry.ports.port_list import PortListParameter
from spira.yevon.geometry.ports import Port
from spira.yevon.utils import geometry
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

    process_polygons = ElementListParameter()

    def __filter___Net____(self, item):
        triangles = item.process_triangles()
        for key, nodes in triangles.items():
            for n in nodes:
                for e in self.process_polygons:
                    if e.encloses(item.g.node[n]['position']):
                        item.g.node[n]['process_polygon'] = e
                        item.g.node[n]['display'] = RDD.DISPLAY.STYLE_SET[e.layer]
        return [item]

    def __repr__(self):
        return "[SPiRA: NetLabelFilter] (layer count {})".format(0)


class NetDeviceLabelFilter(__NetFilter__):
    """ Add 'enabled' ports to the net. """

    device_ports = PortListParameter()

    def __filter___Net____(self, item):
        for n, triangle in item.triangle_nodes().items():
            points = [geometry.c2d(item.mesh_data.points[i]) for i in triangle]
            for D in self.device_ports:
                if isinstance(D, ContactPort):
                    if D.encloses(points):
                        item.g.node[n]['device_reference'] = D
                        item.g.node[n]['display'] = RDD.DISPLAY.STYLE_SET[D.layer]
                elif isinstance(D, Port):
                    if D.purpose == RDD.PURPOSE.PORT.EDGE_ENABLED:
                        if D.encloses(points):
                            item.g.node[n]['device_reference'] = D
                            item.g.node[n]['display'] = RDD.DISPLAY.STYLE_SET[D.layer]
        return [item]

    def __repr__(self):
        return "[SPiRA: NetLabelFilter] (layer count {})".format(0)


class NetEdgeFilter(__NetFilter__):
    """  """

    process_polygons = ElementListParameter()

    def _triangles_containing_line(self, item, line):
        nodes = []
        for n, triangle in enumerate(item.triangles):
            if (line[0] in triangle) and (line[1] in triangle):
                nodes.append(n)
        return nodes

    def __filter___Net____(self, item):

        ELM_TYPE = {1: 'line', 2: 'triangle'}

        # print('\n---------------------------------\n')
            
        # print('Triangles:')
        # print(item.triangles)
        # print('Lines:')
        # print(item.lines)
        # print('Physical Lines:')
        # print(item.physical_lines)
        
        # print('\n---------------------------------\n')

        # print('Parameter Data:')
        # for k, v in item.mesh_data.field_data.items():
        #     print(k, v)

        # print('\n---------------------------------\n')

        # print('Process Lines')
        # print(item.process_lines())
        # print('Process Triangles')
        # print(item.process_triangles())

        # print('\n---------------------------------\n')

        for key, value in item.mesh_data.field_data.items():

            line_keys = key.split('*')

            if len(line_keys) > 1:
                if line_keys[1] != 'None':
    
                    ply_string = key.split('*')[0]
                    ply_hash = key.split('*')[1]
        
                    elm_type = ELM_TYPE[value[1]]
                    if elm_type == 'line':
        
                        for e in self.process_polygons:
                            for i, physical_line_id in enumerate(item.physical_lines):
                                if physical_line_id == value[0]:
                                    for n in self._triangles_containing_line(item, item.lines[i]):
                                        item.g.node[n]['process_polygon'] = ply_string
                                        # FIXME: Change to equal the overlapping edge display.
                                        item.g.node[n]['display'] = RDD.DISPLAY.STYLE_SET[RDD.PLAYER.I5.VIA]
                                        # item.g.node[n]['display'] = RDD.DISPLAY.STYLE_SET[RDD.PLAYER.M1.HOLE]
        return [item]

    def __repr__(self):
        return "[SPiRA: NetLabelFilter] (layer count {})".format(0)


class NetBlockLabelFilter(__NetFilter__):
    """  """

    from spira.yevon.vmodel.boundary import reference_metal_blocks

    references = ElementListParameter()

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



