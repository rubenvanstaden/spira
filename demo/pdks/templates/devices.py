import spira 
from spira import param, shapes
from spira.lpe.mask import Metal, Native
from spira.lne.net import Net
from demo.pdks import ply
import numpy as np


RDD = spira.get_rule_deck()


class Device(spira.Cell):
    """ A Cell encapsulates a set of elementals that
    describes the layout being generated. """

    metals = param.ElementalListField()
    contacts = param.ElementalListField()

    # FIXME: Merge with structure module.
    level = param.IntegerField(default=1)
    # lcar = param.IntegerField(default=0.000001)
    lcar = param.IntegerField(default=0.0000005)
    algorithm = param.IntegerField(default=6)

    get_primitives = param.DataField(fdef_name='get_primitives_function')
    merged_layers = param.DataField(fdef_name='create_merged_layers')

    def __repr__(self):
        if hasattr(self, 'elementals'):
            elems = self.elementals
            return ("[SPiRA: Device(\'{}\')] " +
                    "({} elementals: {} sref, {} cells, {} polygons, " +
                    "{} labels, {} ports)").format(
                        self.name,
                        elems.__len__(),
                        elems.sref.__len__(),
                        elems.cells.__len__(),
                        elems.polygons.__len__(),
                        elems.labels.__len__(),
                        self.ports.__len__()
                    )
        else:
            return "[SPiRA: Device(\'{}\')]".format(self.__class__.__name__)

    # FIXME: Has to be placed here for deepcopy().
    def __str__(self):
        return self.__repr__()

    def _copy(self):
        cell = Device(
            name=self.name,
            elementals=deepcopy(self.elementals),
            ports=deepcopy(self.ports),
            nets=self.nets
        )
        return cell

    def create_metals(self, elems):
        return elems

    def create_contacts(self, elems):
        return elems

    def create_merged_layers(self):
        elems = spira.ElementList()
        params = {}

        for M in self.metals:
            if M.player in params:
                for pp in M.polygon.polygons:
                    params[M.player].append(pp)
            else:
                params[M.player] = []
                for pp in M.polygon.polygons:
                    params[M.player].append(pp)

        for player, points in params.items():
            shape = shapes.Shape(points=points)
            shape.apply_merge

            # elems += ply.Polygon(
            #     name='box_{}_{}'.format(player, 0),
            #     player=player,
            #     points=shape.points,
            #     level=self.level
            # )

            # Have to enumerate over all merged points,
            # to create unique polyogn IDs.
            for i, pts in enumerate(shape.points):
                # elems += spira.Polygons(shape=[pts])
                elems += ply.Polygon(
                    name='box_{}_{}'.format(player, i),
                    player=player,
                    points=[pts],
                    level=self.level
                )

        return elems

    def create_elementals(self, elems):
        if len(elems) == 0:
            # metals = Metal(elementals=self.metals, level=1)
            metals = Metal(elementals=self.merged_layers, level=1)
            natives = Native(elementals=self.contacts, level=1)

            elems += spira.SRef(metals)
            elems += spira.SRef(natives)

            for key in RDD.VIAS.keys:
                RDD.VIAS[key].PCELL.create_elementals(elems)
        else:
            for key in RDD.VIAS.keys:
                elems += spira.SRef(RDD.VIAS[key].PCELL, midpoint=(0,0))
        return elems

    def get_metal_polygons(self, pl):
        # elems = self.elementals
        # elems = self.metals
        elems = self.merged_layers
        # elems = self.elementals
        ply_elems = spira.ElementList()
        for M in elems:
            if M.layer.is_equal_number(pl.layer):
                # print(M.polygon.gdslayer.datatype)
                ply_elems += M.polygon
            #     if M.polygon.gdslayer.datatype in (1, 2):
            #         ply_elems += M.polygon
        return ply_elems

    def get_primitives_function(self):
        ports = self.ports
        elems = self.contacts
        prim_elems = spira.ElementList()
        for N in elems:
            prim_elems += N
        # if ports is not None:
        #     for P in ports:
        #         prim_elems += P
        return prim_elems

    def create_nets(self, nets):
        for pl in RDD.PLAYER.get_physical_layers(purposes='METAL'):
            metal_elems = self.get_metal_polygons(pl)
            if metal_elems:
            # if self.metals:
                net = Net(
                    name='{}'.format(pl.layer.number),
                    lcar=self.lcar,
                    level=self.level,
                    algorithm=self.algorithm,
                    layer=pl.layer,
                    # polygons=self.metals,
                    polygons=metal_elems,
                    # primitives=self.get_primitives,
                    primitives=self.get_primitives
                    # bounding_boxes=self.bounding_boxes
                )
                nets += net.graph
        return nets

    def create_netlist(self):
        self.g = self.merge
        self.g = self.nodes_combine(algorithm='d2d')
        self.g = self.nodes_combine(algorithm='s2s')

        # if self.g is not None:
        #     for n in self.g.nodes():
        #         # self.g.node[n]['pos'] += self.midpoint
        #         self.g.node[n]['surface'].node_id = '{}_{}'.format(
        #             self.name, 
        #             self.g.node[n]['surface'].node_id
        #         )
        #         if 'device' in self.g.node[n]:
        #             self.g.node[n]['device'].node_id = '{}_{}'.format(
        #                 self.name, 
        #                 self.g.node[n]['device'].node_id
                    # )

        self.plot_netlist(G=self.g, graphname=self.name, labeltext='id')

        return self.g


