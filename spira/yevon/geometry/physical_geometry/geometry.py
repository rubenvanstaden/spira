import os
import pygmsh
import meshio
import networkx as nx

from spira.yevon.gdsii.group import __Group__
from spira.core.parameters.variables import *
from spira.yevon.utils.geometry import numpy_to_list
from spira.core.parameters.descriptor import DataField


class __Geometry__(object):
    pass


class GmshGeometry(__Group__):

    _ID = 0

    name = StringField(default='NoName')
    lcar = NumberField(default=1e6)
    height = FloatField(default=0.0)
    holes = IntegerField(default=0)
    algorithm = IntegerField(default=6)
    dimension = IntegerField(default=2)

    # TODO: Add GMSH geometry parameter.
    # geom = GmshField(algorithm=6, scaling_factor=1e-6, coherence_mesh=True)

    mesh_data = DataField(fdef_name='create_mesh_data')
    physical_surfaces = DataField(fdef_name='create_physical_surfaces')

    def __init__(self, elementals=None, **kwargs):
        super().__init__(elementals=elementals, **kwargs)

        self.geom = pygmsh.opencascade.Geometry(
            characteristic_length_min=self.lcar,
            characteristic_length_max=self.lcar
        )
        self.geom.add_raw_code('Mesh.Algorithm = {};'.format(self.algorithm))
        self.geom.add_raw_code('Mesh.ScalingFactor = {};'.format(1e-6))
        self.geom.add_raw_code('Coherence Mesh;')

    def create_physical_surfaces(self):
        """ Creates physical surfaces that is compatible
        with the GMSH library for mesh generation. """

        if self.holes == 0: holes = None
        else: holes = self.holes
        surfaces = []
        for i, ply in enumerate(self.process_polygons):
            pts = numpy_to_list(ply.points, self.height, unit=1e-6)
            surface_label = '{}_{}_{}_{}'.format(
                ply.gds_layer.number,
                ply.gds_layer.datatype,
                Geometry._ID, i
            )
            gp = self.geom.add_polygon(pts, lcar=self.lcar, make_surface=True, holes=holes)
            self.geom.add_physical(gp.surface, label=surface_label)
            surfaces.append([gp.surface, gp.line_loop])
            Geometry._ID += 1
        return surfaces

    def create_mesh_data(self):
        """ Generates the mesh data from the 
        created physical surfaces. """

        if len(self.physical_surfaces) > 1:
            self.geom.boolean_union(self.physical_surfaces)

        directory = os.getcwd() + '/debug/gmsh/'
        mesh_file = '{}{}.msh'.format(directory, self.name)
        geo_file = '{}{}.geo'.format(directory, self.name)
        vtk_file = '{}{}.vtu'.format(directory, self.name)

        if not os.path.exists(directory):
            os.makedirs(directory)

        mesh_data = pygmsh.generate_mesh(
            self.geom,
            verbose=False,
            dim=self.dimension,
            prune_vertices=False,
            remove_faces=False,
            geo_filename=geo_file
        )

        meshio.write(mesh_file, mesh_data)
        meshio.write(vtk_file, mesh_data)

        return mesh_data


