# from spira.core.initializer import FieldInitializer
import os
import pygmsh
import networkx as nx
from spira.yevon.gdsii.base import __Group__
from spira.core.param.variables import *
from spira.core.descriptor import DataField
from spira.yevon.utils import numpy_to_list


class Geometry(__Group__):
    
    _ID = 0
    
    name = StringField(default='NoName')
    lcar = NumberField(default=1e6)
    height = FloatField(default=0.0)
    holes = IntegerField(default=0)
    algorithm = IntegerField(default=6)
    dimension = IntegerField(default=2)

    physical_surfaces = DataField(fdef_name='create_physical_surfaces')
    mesh_data = DataField(fdef_name='create_mesh_data')

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

        if self.holes == 0:
            holes = None
        else:
            holes = self.holes

        ps = []
        for ply in self.elementals:
            for i, points in enumerate(ply.points):
                c_points = numpy_to_list(points, self.height, unit=1e-6)
                surface_label = '{}_{}_{}_{}'.format(
                    ply.gds_layer.number,
                    ply.gds_layer.datatype,
                    Geometry._ID, i
                )
                gp = self.geom.add_polygon(c_points, lcar=self.lcar, make_surface=True, holes=holes)
                self.geom.add_physical(gp.surface, label=surface_label)
                ps.append([gp.surface, gp.line_loop])
                Geometry._ID += 1
        return ps

    def create_mesh_data(self):

        ps = self.physical_surfaces

        if len(ps) > 1:
            self.geom.boolean_union(ps)

        directory = os.getcwd() + '/debug/gmsh/'
        mesh_file = '{}{}.msh'.format(directory, self.name)
        geo_file = '{}{}.geo'.format(directory, self.name)
        vtk_file = '{}{}.vtu'.format(directory, self.name)

        if not os.path.exists(directory):
            os.makedirs(directory)

        mesh_data = None

        mesh_data = pygmsh.generate_mesh(
            self.geom,
            verbose=False,
            dim=self.dimension,
            prune_vertices=False,
            remove_faces=False,
            geo_filename=geo_file
        )

        # FIXME: WARNING:root:Binary Gmsh needs c_int (typically numpy.int32) integers (got int64). Converting.
        # mm = meshio.Mesh(*mesh_data)
        # meshio.write(mesh_file, mm)
        # meshio.write(vtk_file, mm)

        return mesh_data


