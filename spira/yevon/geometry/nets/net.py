from spira.yevon.geometry.nets.base import __Net__
from spira.core.descriptor import DataField
from spira.core.param.variables import GraphField
from spira.yevon.rdd.layer import PhysicalLayerField
from spira.yevon.rdd import get_rule_deck
from spira.yevon.properties.port import PortProperties
from spira.yevon import utils
from spira.yevon.geometry.ports.port import Port
from spira.yevon.geometry.ports.terminal import Terminal


RDD = get_rule_deck()


class Net(__Net__, PortProperties):

    # g = GraphField()
    ps_layer = PhysicalLayerField()

    surface_nodes = DataField(fdef_name='create_surface_nodes')
    device_nodes = DataField(fdef_name='create_device_nodes')
    boundary_nodes = DataField(fdef_name='create_boundary_nodes')
    routes = DataField(fdef_name='create_route_nodes')

    def __init__(self, elementals=None, **kwargs):
        super().__init__(elementals=elementals, **kwargs)

        self.surface_nodes
        self.device_nodes

    def create_surface_nodes(self):
        triangles = self.__layer_triangles_dict__()
        for key, nodes in triangles.items():
            for n in nodes:
                for poly in self.elementals:
                    if poly.encloses(self.g.node[n]['pos']):
                        # pp.color = pl.data.COLOR
                        self.g.node[n]['surface'] = poly

    # def create_surface_nodes(self):
    #     triangles = self.__layer_triangles_dict__()
    #     for key, nodes in triangles.items():
    #         for n in nodes:
    #             # for pp in self.elementals:
    #             #     poly = pp.polygon
    #             for poly in self.elementals:
    #                 if poly.encloses(self.g.node[n]['pos']):
    #                     for pl in RDD.PLAYER.get_physical_layers(purposes='METAL'):
    #                         # if pl.layer == self.layer:
    #                         print(pl.layer)
    #                         print(poly.gds_layer)
    #                         if pl.layer == poly.gds_layer:
    #                             # pp.color=pl.data.COLOR
    #                             # self.g.node[n]['surface'] = pp
    #                             # pp.color = pl.data.COLOR
    #                             self.g.node[n]['surface'] = poly
    
    def create_device_nodes(self):
        for n, triangle in self.__triangle_nodes__().items():
            points = [utils.c2d(self.mesh_data.points[i]) for i in triangle]
            for D in self.ports:
                if isinstance(D, (Port, Terminal)):
                    if D.encloses(points):
                        self.g.node[n]['device'] = D
                else:
                    for p in D.ports:
                        if p.gds_layer.number == self.layer.number:
                            if p.encloses(points):
                                if 'device' in self.g.node[n]:
                                    self.add_new_node(n, D, p.midpoint)
                                else:
                                    self.g.node[n]['device'] = D

    # def create_device_nodes(self):
    #     for n, triangle in self.__triangle_nodes__().items():
    #         points = [utils.c2d(self.mesh_data.points[i]) for i in triangle]
    #         # for D in self.primitives:
    #         for D in self.ports:
    #             if isinstance(D, (spira.Port, spira.Term)):
    #                 if not isinstance(D, (spira.Dummy, spira.EdgeTerm)):
    #                     if D.encloses(points):
    #                         self.g.node[n]['device'] = D
    #             else:
    #                 for p in D.ports:
    #                     if p.gds_layer.number == self.layer.number:
    #                         if p.encloses(points):
    #                             if 'device' in self.g.node[n]:
    #                                 self.add_new_node(n, D, p.midpoint)
    #                             else:
    #                                 self.g.node[n]['device'] = D

    def create_route_nodes(self):
        """  """
        from spira import pc

        def r_func(R):
            if issubclass(type(R), pc.ProcessLayer):
                R_ply = R.elementals[0]
                for n in self.g.nodes():
                    if R_ply.encloses(self.g.node[n]['pos']):
                        self.g.node[n]['route'] = R
            else:
                for pp in R.ref.metals:
                    R_ply = pp.elementals[0]
                    for n in self.g.nodes():
                        if R_ply.encloses(self.g.node[n]['pos']):
                            self.g.node[n]['route'] = pp

        for R in self.route_nodes:
            if isinstance(R, spira.ElementList):
                for r in R:
                    r_func(r)
            else:
                r_func(R)
    
    def create_boundary_nodes(self):
        if self.level > 1:
            for B in self.bounding_boxes:
                for ply in B.elementals.polygons:
                    for n in self.g.nodes():
                        if ply.encloses(self.g.node[n]['pos']):
                            self.g.node[n]['device'] = B.S
                            self.g.node[n]['device'].node_id = '{}_{}'.format(B.S.ref.name, B.S.midpoint)
