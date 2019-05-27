import numpy as np
import networkx as nx

from spira.core.parameters.variables import GraphField
from spira.yevon.geometry.physical_geometry.geometry import Geometry
from spira.core.parameters.descriptor import DataField
from spira.yevon.geometry.coord import Coord
from spira.yevon.rdd import get_rule_deck


RDD = get_rule_deck()


# TODO: Make the Net a transformable.


class __Net__(Geometry):
    """ Constructs a graph from the physical geometry
    generated from the list of elementals. """

    g = GraphField()

    mesh_graph = DataField(fdef_name='create_mesh_graph')
    triangles = DataField(fdef_name='create_triangles')
    physical_triangles = DataField(fdef_name='create_physical_triangles')

    def __init__(self, elementals=None, **kwargs):
        super().__init__(elementals=elementals, **kwargs)
        self.mesh_graph
        # self.g = nx.Graph()

    # def __getitem__(self, n):
    #     return self.g.node[n]

    def transform(self, transformation):
        pass

    def transform_copy(self, transformation):
        pass

    def move(self, coordinate):
        pass

    def create_triangles(self):
        if 'triangle' not in self.mesh_data.cells:
            raise ValueError('Triangle not found in cells')
        return self.mesh_data.cells['triangle']

    def create_physical_triangles(self):
        # if 'triangle' not in self.mesh_data.cell_data[0]:
        if 'triangle' not in self.mesh_data.cell_data:
            raise ValueError('Triangle not in meshio cell_data')
        # if 'gmsh:physical' not in self.mesh_data.cell_data[0]['triangle']:
        if 'gmsh:physical' not in self.mesh_data.cell_data['triangle']:
            raise ValueError('Physical not found in meshio triangle')
        # return self.mesh_data.cell_data[0]['triangle']['gmsh:physical'].tolist()
        return self.mesh_data.cell_data['triangle']['gmsh:physical'].tolist()

    def create_mesh_graph(self):
        """ Create a graph from the meshed geometry. """
        # print(self.mesh_data)
        ll = len(self.mesh_data.points)
        A = np.zeros((ll, ll), dtype=np.int64)
        for n, triangle in enumerate(self.triangles):
            self.__add_edges__(n, triangle, A)
        for n, triangle in enumerate(self.triangles):
            self.__add_positions__(n, triangle)

    def __add_edges__(self, n, tri, A):
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

    def __add_positions__(self, n, tri):
        pp = self.mesh_data.points
        n1, n2, n3 = pp[tri[0]], pp[tri[1]], pp[tri[2]]
        sum_x = (n1[0] + n2[0] + n3[0]) / (3.0*RDD.GDSII.GRID)
        sum_y = (n1[1] + n2[1] + n3[1]) / (3.0*RDD.GDSII.GRID)
        self.g.node[n]['vertex'] = tri
        # self.g.node[n]['position'] = [sum_x, sum_y]
        self.g.node[n]['position'] = Coord(sum_x, sum_y)

    def __add_new_node__(self, n, D, pos):
        l1 = spira.Layer(name='Label', number=104)
        label = spira.Label(
            position=pos,
            text='new',
            gds_layer = l1
        )
        label.node_id = '{}_{}'.format(n, n)
        num = self.g.number_of_nodes()
        self.g.add_node(num+1,
            pos=pos,
            device=D,
            surface=label,
            display='{}'.format(l1.name)
        )
        self.g.add_edge(n, num+1)

    def __layer_triangles_dict__(self):
        """
        Arguments
        ---------
        tri : list
            The surface_id of the triangle
            corresponding to the index value.
        key -> 5_0_1 (layer_datatype_polyid)
        value -> [1 2] (1=surface_id 2=triangle)
        """

        triangles = {}
        # for name, value in self.mesh_data.field_data[0].items():
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

    def __triangle_nodes__(self):
        """ Get triangle field_data in list form. """
        nodes = []
        for v in self.__layer_triangles_dict__().values():
            nodes.extend(v)
        triangles = {}
        for n in nodes:
            for node, triangle in enumerate(self.triangles):
                if n == node:
                    triangles[n] = triangle
        return triangles
