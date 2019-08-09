import os
import pygmsh
import meshio
import networkx as nx

from copy import deepcopy
from spira.yevon.gdsii.elem_list import ElementListParameter
from spira.yevon.process.process_layer import ProcessParameter
from spira.core.parameters.initializer import ParameterInitializer
from spira.core.parameters.variables import *
from spira.core.parameters.descriptor import Parameter, FunctionParameter
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = ['GmshGeometry', 'SalomeGeometry', 'GeometryParameter']


class __Geometry__(ParameterInitializer):
    pass


class SalomeGeometry(__Geometry__):
    """ Generate a geometry using the Salome library. """
    pass


class GmshGeometry(__Geometry__):
    """ Generate a geometry using the Gmsh library. """

    _ID = 0

    _uid = 0

    lcar = NumberParameter(default=100, doc='Mesh characteristic length.')
    algorithm = IntegerParameter(default=1, doc='Mesh algorithm used by Gmsh.')
    scale_Factor = NumberParameter(default=1e-6, doc='Mesh coord dimention scaling.')
    coherence_mesh = BoolParameter(defualt=True, doc='Merge similar points.')

    process = ProcessParameter()
    process_polygons = ElementListParameter()

    mesh_data = Parameter(fdef_name='create_mesh_data')

    def get_filename(self):
        if not hasattr(self, '__alias__'):
            self.__alias__ = '{}_{}'.format(self.process.symbol, GmshGeometry._uid)
            GmshGeometry._uid += 1
        return self.__alias__

    def set_filename(self, value):
        if value is not None:
            self.__alias__ = value

    filename = FunctionParameter(get_filename, set_filename, doc='Functions to generate an alias for cell name.')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.geom = pygmsh.opencascade.Geometry(
            characteristic_length_min=self.lcar,
            characteristic_length_max=self.lcar
        )
        self.geom.add_raw_code('Mesh.Algorithm = {};'.format(self.algorithm))
        self.geom.add_raw_code('Mesh.ScalingFactor = {};'.format(self.scale_Factor))
        if self.coherence_mesh is True:
            self.geom.add_raw_code('Coherence Mesh;')

    def __physical_surfaces__(self):
        """ Creates physical surfaces that is compatible
        with the GMSH library for mesh generation. """
        import re

        surfaces = []
        for i, ply in enumerate(self.process_polygons):
            shape = ply.shape.transform_copy(ply.transformation)
            layer = RDD.GDSII.EXPORT_LAYER_MAP[ply.layer]
            pts = [[p[0], p[1], 0] for p in shape.points]
            surface_label = '{}_{}_{}_{}'.format(layer.number, layer.datatype, GmshGeometry._ID, i)
            gp = self.geom.add_polygon(pts, lcar=self.lcar, make_surface=True, holes=None)

            for j, ll in enumerate(gp.lines):
                pid = ply.shape.segment_labels[j].split(' - hash ')
                if len(pid) > 1:
                    line_label = "{}*{}*{}".format(pid[0], pid[1], j)
                else:
                    line_label = "{}*{}*{}".format(pid[0], None, j)
                self.geom.add_physical(ll, label=line_label)
            self.geom.add_physical(gp.surface, label=surface_label)
            # surfaces.append([gp.surface, gp.line_loop])

            surfaces.append(gp)
            GmshGeometry._ID += 1
        return surfaces

    def create_mesh_data(self):
        """ Generates the mesh data from the created physical surfaces. """

        # if len(self.physical_surfaces) > 1:
        #     self.geom.boolean_union(self.physical_surfaces)

        self.__physical_surfaces__()

        directory = os.getcwd() + '/debug/gmsh/'

        mesh_file = '{}{}.msh'.format(directory, self.filename)
        geo_file = '{}{}.geo'.format(directory, self.filename)
        vtk_file = '{}{}.vtu'.format(directory, self.filename)

        if not os.path.exists(directory):
            os.makedirs(directory)

        mesh_data = pygmsh.generate_mesh(
            self.geom, verbose=False, dim=2,
            prune_vertices=False,
            remove_faces=False,
            geo_filename=geo_file
        )

        # meshio.write(mesh_file, mesh_data)
        # meshio.write(vtk_file, mesh_data)

        return mesh_data


def GeometryParameter(local_name=None, restriction=None, **kwargs):
    R = RestrictType(__Geometry__) & restriction
    return RestrictedParameter(local_name, restriction=R, **kwargs)

