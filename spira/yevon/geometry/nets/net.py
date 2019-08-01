import numpy as np
import networkx as nx
import spira.all as spira

from copy import deepcopy
from spira.core.parameters.variables import GraphParameter, StringParameter
from spira.core.parameters.descriptor import Parameter
from spira.yevon.geometry.coord import Coord
from spira.yevon.vmodel.geometry import GeometryParameter
from spira.yevon.geometry.ports.base import __Port__
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = ['Net']


ELM_TYPE = {1: 'line', 2: 'triangle'}


from spira.core.transformable import Transformable
from spira.core.parameters.initializer import ParameterInitializer
class __Net__(Transformable, ParameterInitializer):
    """  """

    @property
    def count(self):
        return nx.number_of_nodes(self.g)


class Net(__Net__):
    """
    Constructs a graph from the physical geometry
    generated from the list of elements.
    """

    # g = GraphParameter()
    g = Parameter()

    mesh_data = Parameter(fdef_name='create_mesh_data')
    geometry = GeometryParameter(allow_none=True, default=None)

    lines = Parameter(fdef_name='create_lines')
    triangles = Parameter(fdef_name='create_triangles')
    physical_triangles = Parameter(fdef_name='create_physical_triangles')
    physical_lines = Parameter(fdef_name='create_physical_lines')

    name = StringParameter(default='no_name')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'g' in kwargs:
            self.g = kwargs['g']
        else:
            self.g = nx.Graph()
            self._generate_mesh_graph()

    def __repr__(self):
        if self.geometry is None:
            class_string = "[SPiRA: Net] (name \'{}\', nodes {})"
            return class_string.format(self.name, self.count)
        else:
            class_string = "[SPiRA: Net] (name \'{}\', nodes {}, geometry {})"
            return class_string.format(self.name, self.count, self.geometry.process.symbol)

    def __str__(self):
        return self.__repr__()

    def _generate_mesh_graph(self):
        """ Create a graph from the meshed geometry. """
        ll = len(self.mesh_data.points)
        A = np.zeros((ll, ll), dtype=np.int64)

        for n, triangle in enumerate(self.triangles):
            self._add_edges(n, triangle, A)
        for n, triangle in enumerate(self.triangles):
            self._add_positions(n, triangle)

    def _add_edges(self, n, tri, A):
        def update_adj(self, t1, adj_mat, v_pair):
            if (adj_mat[v_pair[0]][v_pair[1]] != 0):
                t2 = adj_mat[v_pair[0]][v_pair[1]] - 1
                self.g.add_edge(t1, t2, label=None)
            else:
                adj_mat[v_pair[0]][v_pair[1]] = t1 + 1
                adj_mat[v_pair[1]][v_pair[0]] = t1 + 1
        v1 = [tri[0], tri[1], tri[2]]
        v2 = [tri[1], tri[2], tri[0]]
        for v_pair in list(zip(v1, v2)):
            update_adj(self, n, A, v_pair)

    def _add_positions(self, n, triangle):
        from spira import settings
        pp = self.mesh_data.points
        grids_per_unit = settings.get_grids_per_unit()
        n1, n2, n3 = pp[triangle[0]], pp[triangle[1]], pp[triangle[2]]
        x = (n1[0] + n2[0] + n3[0]) / 3
        y = (n1[1] + n2[1] + n3[1]) / 3
        x = x * grids_per_unit
        y = y * grids_per_unit
        self.g.node[n]['vertex'] = triangle
        self.g.node[n]['position'] = Coord(x, y)
        self.g.node[n]['display'] = RDD.DISPLAY.STYLE_SET[RDD.PLAYER.METAL]

    def create_mesh_data(self):
        return self.geometry.mesh_data

    def add_new_node(self, n, D, polygon, position, display):
        num = self.g.number_of_nodes()
        self.g.add_node(num+1, position=position, device_reference=D, process_polygon=polygon, display=display)
        self.g.add_edge(n, num+1)

    def create_triangles(self):
        if 'triangle' not in self.mesh_data.cells:
            raise ValueError('Triangle not found in cells')
        return self.mesh_data.cells['triangle']

    def create_lines(self):
        if 'line' not in self.mesh_data.cells:
            raise ValueError('Line not found in cells')
        return self.mesh_data.cells['line']

    def create_physical_triangles(self):
        if 'triangle' not in self.mesh_data.cell_data:
            raise ValueError('Triangle not in meshio cell_data')
        if 'gmsh:physical' not in self.mesh_data.cell_data['triangle']:
            raise ValueError('Physical not found in meshio triangle')
        return self.mesh_data.cell_data['triangle']['gmsh:physical'].tolist()

    def create_physical_lines(self):
        if 'line' not in self.mesh_data.cell_data:
            raise ValueError('Line not in meshio cell_data')
        if 'gmsh:physical' not in self.mesh_data.cell_data['line']:
            raise ValueError('Physical not found in meshio triangle')
        return self.mesh_data.cell_data['line']['gmsh:physical'].tolist()

    def process_triangles(self):
        """
        Arguments
        ---------
        tri : list
            The surface_id of the triangle
            corresponding to the index value.
        name -> 5_0_1 (layer_datatype_polyid)
        value -> [1 2] (1=surface_id 2=triangle)
        """

        triangles = {}
        for name, value in self.mesh_data.field_data.items():
            for n in self.g.nodes():
                surface_id = value[0]
                if self.physical_triangles[n] == surface_id:
                    layer = int(name.split('_')[0])
                    datatype = int(name.split('_')[1])
                    key = (layer, datatype)
                    if key in triangles:
                        triangles[key].append(n)
                    else:
                        triangles[key] = [n]
        return triangles

    def process_lines(self):
        """
        Arguments
        ---------
        tri : list
            The surface_id of the triangle
            corresponding to the index value.
        name -> 5_0_1 (layer_datatype_polyid)
        value -> [1 2] (1=surface_id 2=triangle)
        """

        lines = {}
        for name, value in self.mesh_data.field_data.items():
            # print(name, value)
            # print(self.physical_lines)
            for n in self.physical_lines:
                line_id = value[0]
                if n == line_id:
                    # print(name)
                    # print(value)
                    # print('')
                    polygon_string = name.split('*')[0]
                    polygon_hash = name.split('*')[1]
                    polygon_uid = int(name.split('*')[2])
                    key = (polygon_string, polygon_hash, polygon_uid)
                    if key in lines:
                        lines[key].append(n)
                    else:
                        lines[key] = [n]
        return lines

    def get_triangles_connected_to_line(self):
        """
        Labeling of an edge line:
        polygon_uid_i [line elm_type]
        [SPiRA: Polygon 'M5']_17_0 [2 1]

        Labeling of triangle:
        layer datatype [triangle elm_type]
        50_1_0_0 [1 2]
        """

        # lines = []
        # for v in self.process_lines().values():
        #     lines.extend(v)
        # print(lines)
        # triangles = {}
        # for n in nodes:
        #     for node, triangle in enumerate(self.triangles):
        #         if n == node:
        #             triangles[n] = triangle
        # return triangles

    def triangle_nodes(self):
        """ Get triangle field_data in list form. """
        nodes = []
        for v in self.process_triangles().values():
            nodes.extend(v)
        triangles = {}
        for n in nodes:
            for node, triangle in enumerate(self.triangles):
                if n == node:
                    triangles[n] = triangle
        return triangles

    def transform(self, transformation):
        for n in self.g.nodes():
            self.g.node[n]['position'] = transformation.apply_to_coord(self.g.node[n]['position'])
        return self








