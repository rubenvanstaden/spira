import os
import pygmsh
import meshio
import networkx as nx

from spira.yevon.gdsii.elem_list import ElementalListField
from spira.yevon.process.process_layer import ProcessField
from spira.core.parameters.initializer import FieldInitializer
from spira.core.parameters.variables import *
from spira.yevon.utils.geometry import numpy_to_list
from spira.core.parameters.descriptor import DataField
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = ['GmshGeometry', 'SalomeGeometry', 'GeometryField']


class __Geometry__(FieldInitializer):
    pass


class SalomeGeometry(__Geometry__):
    pass


class GmshGeometry(__Geometry__):
    """  """

    _ID = 0

    lcar = NumberField(default=10, doc='Mesh characteristic length.')
    algorithm = IntegerField(default=6, doc='Mesh algorithm used by Gmsh.')
    scale_Factor = NumberField(default=1e6, doc='Mesh coord dimention scaling.')
    coherence_mesh = BoolField(defualt=True, doc='Merge similar points.')

    process = ProcessField()
    process_polygons = ElementalListField()

    mesh_data = DataField(fdef_name='create_mesh_data')

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

        from copy import deepcopy

        surfaces = []
        for i, polygon in enumerate(self.process_polygons):
            # ply = deepcopy(polygon)
            ply = polygon
            shape = ply.shape.transform(ply.transformation)
            layer = RDD.GDSII.EXPORT_LAYER_MAP[ply.layer]
            pts = numpy_to_list(shape.points, start_height=0, unit=1e-6)
            surface_label = '{}_{}_{}_{}'.format(layer.number, layer.datatype, GmshGeometry._ID, i)
            gp = self.geom.add_polygon(pts, lcar=self.lcar, make_surface=True, holes=None)
            self.geom.add_physical(gp.surface, label=surface_label)
            # surfaces.append([gp.surface, gp.line_loop])
            surfaces.append(gp)
            GmshGeometry._ID += 1
        return surfaces

    def create_mesh_data(self):
        """ Generates the mesh data from the 
        created physical surfaces. """

        # if len(self.physical_surfaces) > 1:
        #     self.geom.boolean_union(self.physical_surfaces)

        self.__physical_surfaces__()

        directory = os.getcwd() + '/debug/gmsh/'
        mesh_file = '{}{}.msh'.format(directory, self.process.symbol)
        geo_file = '{}{}.geo'.format(directory, self.process.symbol)
        vtk_file = '{}{}.vtu'.format(directory, self.process.symbol)

        if not os.path.exists(directory):
            os.makedirs(directory)

        mesh_data = pygmsh.generate_mesh(
            self.geom, verbose=False, dim=2,
            prune_vertices=False,
            remove_faces=False,
            geo_filename=geo_file
        )

        meshio.write(mesh_file, mesh_data)
        meshio.write(vtk_file, mesh_data)

        return mesh_data


def GeometryField(local_name=None, restriction=None, **kwargs):
    R = RestrictType(__Geometry__) & restriction
    return RestrictedParameter(local_name, restriction=R, **kwargs)   
