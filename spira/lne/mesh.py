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
from spira.core.initializer import BaseElement
# from spira.rdd import get_rule_deck
from copy import copy, deepcopy


# -------------------------------------------------------------------
# colormap: https://www.color-hex.com/color-palette/166
# https://www.color-hex.com/color-palette/66223
# -------------------------------------------------------------------


class __Mesh__(meshio.Mesh, BaseElement):

    def __init__(self, polygons, points, cells, **kwargs):

        self.polygons = polygons

        BaseElement.__init__(self, **kwargs)

        meshio.Mesh.__init__(self, points, cells,
                             point_data=self.point_data,
                             cell_data=self.cell_data,
                             field_data=self.field_data,
                             node_sets=self.node_sets,
                             gmsh_periodic=self.gmsh_periodic)

        self.g = nx.Graph()

        self.mesh_graph

    def __repr__(self):
        return '[SPiRA: Mesh] ({})'.format(self.g.number_of_nodes())

    def __str__(self):
        return self.__repr__()


class MeshAbstract(__Mesh__):
    """ Class that connects a meshio generated mesh with
    a networkx generated graph of the set of polygons. """

    name = param.StringField()
    layer = param.LayerField()
    point_data = param.ElementListField()
    cell_data = param.ElementListField()
    field_data = param.ElementListField()
    node_sets = param.ElementListField()
    gmsh_periodic = param.ElementListField()

    mesh_graph = param.DataField(fdef_name='create_mesh_graph')

    def __init__(self, polygons, points, cells, **kwargs):
        super().__init__(polygons, points, cells, **kwargs)

    def create_mesh_graph(self):
        """ Create a graph from the meshed geometry. """

        ll = len(self.points)
        A = np.zeros((ll, ll), dtype=np.int64)

        for n, triangle in enumerate(self.__triangles__()):
            self.add_edges(n, triangle, A)

        for n, triangle in enumerate(self.__triangles__()):
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

        sum_x = 1e+8*(n1[0] + n2[0] + n3[0]) / 3.0
        sum_y = 1e+8*(n1[1] + n2[1] + n3[1]) / 3.0

        self.g.node[n]['vertex'] = tri
        self.g.node[n]['pos'] = [sum_x, sum_y]

    def __triangles__(self):
        if 'triangle' not in self.cells:
            raise ValueError('Triangle not found in cells')
        return self.cells['triangle']

    def __physical_triangles__(self):
        if 'triangle' not in self.cell_data[0]:
            raise ValueError('Triangle not in meshio cell_data')
        if 'gmsh:physical' not in self.cell_data[0]['triangle']:
            raise ValueError('Physical not found ing meshio triangle')
        return self.cell_data[0]['triangle']['gmsh:physical'].tolist()

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
                ptriangles = self.__physical_triangles__()
                if ptriangles[n] == surface_id:
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
            for node, triangle in enumerate(self.__triangles__()):
                if n == node:
                    triangles[n] = triangle
        return triangles

    def __point_data__(self):
        pass

    def flat_copy(self, level=-1, commit_to_gdspy=False):
        return self

    def flatten(self):
        return [self]

    def commit_to_gdspy(self, cell):
        pass

    def transform(self, transform):
        return self


class MeshLabeled(MeshAbstract):

    RDD = spira.get_rule_deck()

    primitives = param.ElementListField()

    surface_nodes = param.DataField(fdef_name='create_surface_nodes')
    pinlabel_nodes = param.DataField(fdef_name='create_pinlabel_nodes')

    def __init__(self, polygons, points, cells, **kwargs):
        print('\nPinLabels object')

        super().__init__(polygons, points, cells, **kwargs)

        self.points = points
        self.cells = cells

        self.surface_nodes
        self.pinlabel_nodes

    def create_surface_nodes(self):

        LOG.header('Adding surface labels')

        node_count = 0

        triangles = self.__layer_triangles_dict__()
        for key, nodes in triangles.items():
            for n in nodes:
                position = self.g.node[n]['pos']

                pid = utils.labeled_polygon_id(position, self.polygons)

                if pid is not None:
                    params = {}
                    params['text'] = self.name
                    params['gdslayer'] = self.layer
                    params['color'] = RDD.METALS.get_key_by_layer(self.layer)['COLOR']

                    label = spira.Label(position=position, **params)
                    label.id = '{}_{}'.format(key[0], pid)

                    self.g.node[n]['surface'] = label

            node_count += 1

        print('# surface nodes added: {}'.format(node_count))

    def create_pinlabel_nodes(self):

        LOG.header('Adding pin labels')

        for node, triangle in self.__triangle_nodes__().items():
            points = [utils.c2d(self.points[i]) for i in triangle]
            for S in self.primitives:
                if isinstance(S, spira.Port):
                    self.add_port_label(node, S, points)
                else:
                    self.add_device_label(node, S, points)

    def add_new_node(self, n, D, pos):
        params = {}
        params['text'] = 'new'
        l1 = spira.Layer(name='Label', number=104)
        params['gdslayer'] = l1
        # params['color'] = RDD.METALS.get_key_by_layer(self.layer)['COLOR']

        label = spira.Label(position=pos, **params)
        label.id = '{}_{}'.format(n, n)

        num = self.g.number_of_nodes()

        self.g.add_node(num+1, pos=pos, pin=D, surface=label)
        self.g.add_edge(n, num+1)

    def add_port_label(self, n, D, points):
        if D.point_inside(points):
            P = spira.PortNode(name=D.name, elementals=D)
            self.g.node[n]['pin'] = P

    def add_device_label(self, n, S, points):
        for name, p in S.ports.items():
            if p.gdslayer.name == 'GROUND':
                pass
                # if lbl.layer == self.layer.number:
                #     params = {}
                #     params['text'] = 'GROUND'
                #     l1 = spira.Layer(name='GND', number=104)
                #     params['gdslayer'] = l1
                #
                #     label = spira.Label(position=lbl.position, **params)
                #     label.id = '{}_{}'.format(n, n)
                #
                #     ply = spira.Polygons(gdslayer=l1)
                #
                #     D_gnd = BaseVia(name='BaseVIA_GND',
                #                     ply=ply,
                #                     m2=l1, m1=l1)
                #
                #     num = self.g.number_of_nodes()
                #
                #     self.g.add_node(num+1, pos=lbl.position, pin=D_gnd, surface=label)
                #     self.g.add_edge(n, num+1)
            else:
                # print(S.flat_copy())
                # print(p.gdslayer.number)
                # print(self.layer.number)
                # print('')
                if p.gdslayer.number == self.layer.number:
                    if p.point_inside(points):
                        self.g.node[n]['pin'] = S
                        # if 'pin' in self.g.node[n]:
                        #     self.add_new_node(n, D, lbl.position)
                        # else:
                        #     self.g.node[n]['pin'] = D


        # D = S.ref
        # for L in D.elementals.labels:
        #     lbl = deepcopy(L)
        #
        #     lbl.move(origin=lbl.position, destination=S.origin)
        #
        #     if lbl.gdslayer.name == 'GROUND':
        #         if lbl.layer == self.layer.number:
        #             params = {}
        #             params['text'] = 'GROUND'
        #             l1 = spira.Layer(name='GND', number=104)
        #             params['gdslayer'] = l1
        #
        #             label = spira.Label(position=lbl.position, **params)
        #             label.id = '{}_{}'.format(n, n)
        #
        #             ply = spira.Polygons(gdslayer=l1)
        #
        #             D_gnd = BaseVia(name='BaseVIA_GND',
        #                             ply=ply,
        #                             m2=l1, m1=l1)
        #
        #             num = self.g.number_of_nodes()
        #
        #             self.g.add_node(num+1, pos=lbl.position, pin=D_gnd, surface=label)
        #             self.g.add_edge(n, num+1)
        #     else:
        #         if lbl.layer == self.layer.number:
        #             if lbl.point_inside(points):
        #                 self.g.node[n]['pin'] = D
        #                 # if 'pin' in self.g.node[n]:
        #                 #     self.add_new_node(n, D, lbl.position)
        #                 # else:
        #                 #     self.g.node[n]['pin'] = D


class Mesh(MeshLabeled):
    pass
