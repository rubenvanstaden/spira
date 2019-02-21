import os
import spira
import pygmsh
import meshio
import inspect

import numpy as np
import networkx as nx
from spira import settings

from spira.gdsii.elemental.label import Label
from spira.gdsii import utils
from spira import param

from spira import log as LOG
from spira.core.initializer import ElementalInitializer
from copy import copy, deepcopy


# -------------------------------------------------------------------
# colormap: https://www.color-hex.com/color-palette/166
# https://www.color-hex.com/color-palette/66223
# -------------------------------------------------------------------


RDD = spira.get_rule_deck()


class __Mesh__(meshio.Mesh, ElementalInitializer):

    data = param.ElementalListField()
    gmsh_periodic = param.ElementalListField()
    level = param.IntegerField(default=1)

    points = param.DataField(fdef_name='create_points')
    cells = param.DataField(fdef_name='create_cells')
    point_data = param.DataField(fdef_name='create_point_data')
    cell_data = param.DataField(fdef_name='create_cell_data')
    field_data = param.DataField(fdef_name='create_field_data')
    node_sets = param.DataField(fdef_name='create_node_sets')

    mesh_graph = param.DataField(fdef_name='create_mesh_graph')

    def __init__(self, polygons, bounding_boxes=None, **kwargs):

        self.polygons = polygons
        self.bounding_boxes = bounding_boxes

        ElementalInitializer.__init__(self, **kwargs)

        meshio.Mesh.__init__(self,
            points=self.points,
            cells=self.cells,
            point_data=self.point_data,
            cell_data=self.cell_data,
            field_data=self.field_data,
            node_sets=self.node_sets,
            gmsh_periodic=self.gmsh_periodic
        )

        self.g = nx.Graph()

        self.mesh_graph

    def __repr__(self):
        return '[SPiRA: Mesh] ({})'.format(self.g.number_of_nodes())

    def __str__(self):
        return self.__repr__()

    def create_points(self):
        return self.data[0]

    def create_cells(self):
        return self.data[1]

    def create_point_data(self):
        return [self.data[2]]

    def create_cell_data(self):
        return [self.data[3]]

    def create_field_data(self):
        return [self.data[4]]

    def create_node_sets(self):
        return []


class MeshAbstract(__Mesh__):
    """ Class that connects a meshio generated mesh with
    a networkx generated graph of the set of polygons. """

    name = param.StringField()
    layer = param.LayerField()

    triangles = param.DataField(fdef_name='create_triangles')
    physical_triangles = param.DataField(fdef_name='create_physical_triangles')

    def __init__(self, polygons, bounding_boxes=None, **kwargs):
        super().__init__(polygons, bounding_boxes, **kwargs)

    def create_triangles(self):
        if 'triangle' not in self.cells:
            raise ValueError('Triangle not found in cells')
        return self.cells['triangle']

    def create_physical_triangles(self):
        if 'triangle' not in self.cell_data[0]:
            raise ValueError('Triangle not in meshio cell_data')
        if 'gmsh:physical' not in self.cell_data[0]['triangle']:
            raise ValueError('Physical not found in meshio triangle')
        return self.cell_data[0]['triangle']['gmsh:physical'].tolist()

    def create_mesh_graph(self):
        """ Create a graph from the meshed geometry. """
        ll = len(self.points)
        A = np.zeros((ll, ll), dtype=np.int64)
        for n, triangle in enumerate(self.triangles):
            self.add_edges(n, triangle, A)
        for n, triangle in enumerate(self.triangles):
            self.add_positions(n, triangle)

    def add_edges(self, n, tri, A):
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

    def add_positions(self, n, tri):
        pp = self.points
        n1, n2, n3 = pp[tri[0]], pp[tri[1]], pp[tri[2]]
        sum_x = (n1[0] + n2[0] + n3[0]) / (3.0*RDD.GDSII.GRID)
        sum_y = (n1[1] + n2[1] + n3[1]) / (3.0*RDD.GDSII.GRID)
        self.g.node[n]['vertex'] = tri
        self.g.node[n]['pos'] = [sum_x, sum_y]

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
        for name, value in self.field_data[0].items():
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


class MeshLabeled(MeshAbstract):

    primitives = param.ElementalListField()

    surface_nodes = param.DataField(fdef_name='create_surface_nodes')
    device_nodes = param.DataField(fdef_name='create_device_nodes')
    boundary_nodes = param.DataField(fdef_name='create_boundary_nodes')

    def __init__(self, polygons, bounding_boxes=None, **kwargs):
        super().__init__(polygons, bounding_boxes, **kwargs)

        self.surface_nodes
        self.device_nodes

        if bounding_boxes is not None:
            self.boundary_nodes

    def create_surface_nodes(self):
        triangles = self.__layer_triangles_dict__()
        for key, nodes in triangles.items():
            for n in nodes:

                pid = utils.labeled_polygon_id(
                    self.g.node[n]['pos'], 
                    self.polygons
                )

                if pid is not None:
                    for pl in RDD.PLAYER.get_physical_layers(purposes='METAL'):
                        if pl.layer == self.layer:
                            label = spira.Label(
                                position=self.g.node[n]['pos'],
                                text=self.name,
                                gdslayer=self.layer,
                                color=pl.data.COLOR
                            )
                            label.node_id = '{}'.format(pid)
                            display = '{}'.format(pl.layer.name)
                            self.g.node[n]['surface'] = label
                            self.g.node[n]['display'] = display

    def create_device_nodes(self):
        for node, triangle in self.__triangle_nodes__().items():
            points = [utils.c2d(self.points[i]) for i in triangle]
            for S in self.primitives:
                self.add_device_label(node, S, points)

    def create_boundary_nodes(self):
        if self.level > 1:
            for B in self.bounding_boxes:
                for p in B.elementals.polygons:
                    ply = deepcopy(p)
                    ply.center = B.S.midpoint
                    bnodes = []
                    for n in self.g.nodes():
                        s = self.g.node[n]['surface']
                        if s.encloses(ply.polygons[0]):
                            bnodes.append(n)

                    device_node = None
                    for n in bnodes:
                        # self.g.node[n]['surface'].color = '#FFA07A'
                        self.g.node[n]['device'] = B.S
                        self.g.node[n]['device'].color = '#FFA07A'
                        self.g.node[n]['device'].node_id = '{}_{}'.format(B.S.ref.name, B.S.midpoint)

                        # self.g.node[n]['surface'].color = '#ffffff'
                        # if 'device' in self.g.node[n]:
                        #     self.g.node[n]['device'].color = '#ffffff'
                    #     if 'device' in self.g.node[n]:
                    #         if device_node is None:
                    #             device_node = self.g.node[n]['device']
                    # if device_node is not None:
                    #     for n in bnodes:
                    #         self.g.node[n]['device'] = device_node

    def add_new_node(self, n, D, pos):
        l1 = spira.Layer(name='Label', number=104)
        label = spira.Label(
            position=pos,
            text='new',
            gdslayer = l1
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

    def add_device_label(self, n, D, points):
        if isinstance(D, (spira.Port, spira.Term)):
            if not isinstance(D, spira.Dummy):
                if D.encloses(points):
                    self.g.node[n]['device'] = D
        else:
            for p in D.ports:
                if p.gdslayer.number == self.layer.number:
                    if p.encloses(points):
                        if 'device' in self.g.node[n]:
                            self.add_new_node(n, D, p.midpoint)
                        else:
                            self.g.node[n]['device'] = D


class Mesh(MeshLabeled):
    pass


