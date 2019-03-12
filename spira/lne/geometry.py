import os
import spira
import pygmsh
import meshio

from spira.core.lists import ElementList
from spira.utils import numpy_to_list
from spira import param
from spira.lne.mesh import Mesh
from spira.core.initializer import ElementalInitializer


RDD = spira.get_rule_deck()


class __Geometry__(ElementalInitializer):

    _ID = 0

    height = param.FloatField(default=0)
    holes = param.IntegerField(default=None)
    algorithm = param.IntegerField(default=6)

    create_mesh = param.DataField(fdef_name='create_meshio')
    pygmsh_elementals = param.DataField(fdef_name='create_pygmsh_elementals')

    def __init__(self, lcar, **kwargs):
        ElementalInitializer.__init__(self, **kwargs)

        if lcar == 0:
            raise ValueError('Characteristic Length cannot be zero.')

        self.geom = pygmsh.opencascade.Geometry(
            characteristic_length_min=lcar,
            characteristic_length_max=lcar
        )

        self.geom.add_raw_code('Mesh.Algorithm = {};'.format(self.algorithm))
        # self.geom.add_raw_code('Mesh.ScalingFactor = {};'.format(RDD.GDSII.GRID))
        self.geom.add_raw_code('Mesh.ScalingFactor = {};'.format(1e-6))
        self.geom.add_raw_code('Coherence Mesh;')

        self.mesh = None

    def __surfaces__(self):
        surfaces = []
        for e in self.pygmsh_elementals:
            if isinstance(e, pygmsh.built_in.plane_surface.PlaneSurface):
                surfaces.append(e)
        return surfaces


class GeometryAbstract(__Geometry__):

    name = param.StringField()
    layer = param.LayerField()
    dimension = param.IntegerField(default=2)
    polygons = param.ElementalListField()

    def __init__(self, lcar=1e6, **kwargs):
        super().__init__(lcar=lcar, **kwargs)

    def create_meshio(self):

        if len(self.__surfaces__()) > 1:
            self.geom.boolean_union(self.__surfaces__())

        directory = os.getcwd() + '/debug/gmsh/'
        mesh_file = '{}{}.msh'.format(directory, self.name)
        geo_file = '{}{}.geo'.format(directory, self.name)
        vtk_file = '{}{}.vtu'.format(directory, self.name)

        if not os.path.exists(directory):
            os.makedirs(directory)

        mesh_data = None

        mesh_data = pygmsh.generate_mesh(
            self.geom,
            # verbose=False,
            verbose=True,
            dim=self.dimension,
            prune_vertices=False,
            remove_faces=False,
            geo_filename=geo_file
        )

        mm = meshio.Mesh(*mesh_data)
        print('done meshing')

        # FIXME: WARNING:root:Binary Gmsh needs c_int (typically numpy.int32) integers (got int64). Converting.
        # meshio.write(mesh_file, mm)
        # meshio.write(vtk_file, mm)

        return mesh_data

    def create_pygmsh_elementals(self):
        from spira.utils import scale_polygon_down as spd
        from spira.utils import scale_polygon_up as spu

        elems = ElementList()
        for pp in self.polygons:
            ply = pp.polygon
            print('')
            print(ply)
            for i, points in enumerate(ply.polygons):
                # print(points)
                # c_points = numpy_to_list(points, self.height, unit=RDD.GDSII.GRID)
                c_points = numpy_to_list(points, self.height, unit=1e-6)
                # c_points = numpy_to_list(points, self.height, unit=1)
                print(c_points)
                surface_label = '{}_{}_{}_{}'.format(
                    ply.gdslayer.number,
                    ply.gdslayer.datatype,
                    GeometryAbstract._ID, i
                )
                gp = self.geom.add_polygon(
                    c_points,
                    lcar=1e6,
                    make_surface=True,
                    holes=self.holes
                )
                self.geom.add_physical_surface(gp.surface, label=surface_label)
                elems += [gp.surface, gp.line_loop]
                GeometryAbstract._ID += 1
        return elems


class Geometry(GeometryAbstract):
    pass
