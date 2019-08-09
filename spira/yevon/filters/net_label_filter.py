from spira.log import SPIRA_LOG as LOG
from spira.yevon.filters.filter import Filter
from spira.yevon.process.gdsii_layer import LayerList, LayerListParameter
from spira.yevon.gdsii.elem_list import ElementListParameter
from spira.yevon.geometry.ports.port_list import PortListParameter
from spira.yevon.geometry.ports import Port
from spira import settings
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

    def filter_Net(self, item):
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

    def filter_Net(self, item):
        for n, triangle in item.triangle_nodes().items():

            points = [geometry.c2d(item.mesh_data.points[i]) for i in triangle]
            tri_shape = settings.snap_shape(points)

            for D in self.device_ports:

                if D.purpose == RDD.PURPOSE.PORT.CONTACT:
                    if D.encloses(tri_shape.points):
                        item.g.node[n]['device_reference'] = D
                        item.g.node[n]['display'] = RDD.DISPLAY.STYLE_SET[D.layer]
                
                # if D.purpose == RDD.PURPOSE.PORT.PIN:
                #     if D.encloses(tri_shape.points):
                #         item.g.node[n]['device_reference'] = D
                #         item.g.node[n]['display'] = RDD.DISPLAY.STYLE_SET[D.layer]

                if D.purpose == RDD.PURPOSE.PORT.TERMINAL:
                    # print(D)
                    if D.encloses(tri_shape.points):
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

    def filter_Net(self, item):

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

        import re
        from spira.yevon.geometry.coord import Coord

        for key, value in item.mesh_data.field_data.items():

            line_keys = key.split('*')

            if len(line_keys) > 1:
                if line_keys[1] != 'None':

                    ply_string = key.split('*')[0]
                    ply_hash = key.split('*')[1]

                    elm_type = ELM_TYPE[value[1]]
                    if elm_type == 'line':

                        for i, physical_line_id in enumerate(item.physical_lines):
                            if physical_line_id == value[0]:
                                for n in self._triangles_containing_line(item, item.lines[i]):

                                    name = 'P' + ply_string.split(' ')[0]
                                    pos = re.search(r'\((.*?)\)', ply_string).group(1)
                                    pos = pos.split(',')
                                    pos = [float(p) for p in pos]
                                    midpoint = Coord(pos).snap_to_grid()
                                    item.g.node[n]['device_reference'] = Port(
                                        name=name, midpoint=midpoint, process=self.process_polygons.layer.process)
                                    item.g.node[n]['display'] = RDD.DISPLAY.STYLE_SET[RDD.PLAYER.I5.VIA]
                                    # item.g.node[n]['display'] = RDD.DISPLAY.STYLE_SET[RDD.PLAYER.M1.HOLE]

        return [item]

    # def __filter_Net__(self, item):

    #     ELM_TYPE = {1: 'line', 2: 'triangle'}

    #     # print('\n---------------------------------\n')
            
    #     # print('Triangles:')
    #     # print(item.triangles)
    #     # print('Lines:')
    #     # print(item.lines)
    #     # print('Physical Lines:')
    #     # print(item.physical_lines)

    #     # print('\n---------------------------------\n')

    #     # print('Parameter Data:')
    #     # for k, v in item.mesh_data.field_data.items():
    #     #     print(k, v)

    #     # print('\n---------------------------------\n')

    #     # print('Process Lines')
    #     # print(item.process_lines())
    #     # print('Process Triangles')
    #     # print(item.process_triangles())

    #     # print('\n---------------------------------\n')

    #     for key, value in item.mesh_data.field_data.items():

    #         line_keys = key.split('*')

    #         if len(line_keys) > 1:
    #             if line_keys[1] != 'None':

    #                 ply_string = key.split('*')[0]
    #                 ply_hash = key.split('*')[1]
    #                 print(ply_hash)

    #                 elm_type = ELM_TYPE[value[1]]
    #                 if elm_type == 'line':

    #                     for e in self.process_polygons:
    #                         for i, physical_line_id in enumerate(item.physical_lines):
    #                             if physical_line_id == value[0]:
    #                                 for n in self._triangles_containing_line(item, item.lines[i]):
                                        
    #                                     # item.g.node[n]['process_polygon'] = ply_string
    #                                     # # item.g.node[n]['display'] = RDD.DISPLAY.STYLE_SET[RDD.PLAYER.I5.VIA]
    #                                     # item.g.node[n]['display'] = RDD.DISPLAY.STYLE_SET[RDD.PLAYER.M1.HOLE]

    #                                     # shape = e.shape.transform_copy(e.transformation)
    #                                     print(e.shape.hash_string)
    #                                     if ply_hash == e.shape.hash_string:
    #                                         item.g.node[n]['process_polygon'] = e
    #                                         # FIXME: Change to equal the overlapping edge display.
    #                                         # item.g.node[n]['display'] = RDD.DISPLAY.STYLE_SET[RDD.PLAYER.I5.VIA]
    #                                         item.g.node[n]['display'] = RDD.DISPLAY.STYLE_SET[RDD.PLAYER.M1.HOLE]

    #                 print('')

    #     return [item]

    def __repr__(self):
        return "[SPiRA: NetLabelFilter] (layer count {})".format(0)


class NetBlockLabelFilter(__NetFilter__):
    """  """

    from spira.yevon.vmodel.boundary import reference_metal_blocks

    references = ElementListParameter()

    def filter_Net(self, item):
        for S in self.references:
            for e in reference_metal_blocks(S):
                for n in item.g.nodes():
                    if e.encloses(item.g.node[n]['position']):
                        item.g.node[n]['device_reference'] = S
                        item.g.node[n]['display'] = RDD.DISPLAY.STYLE_SET[e.layer]
        return item

    def __repr__(self):
        return "[SPiRA: NetLabelFilter] (layer count {})".format(0)



