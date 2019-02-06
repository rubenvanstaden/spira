import spira
import numpy as np
from spira import param, shapes
from spira.lpe import mask
from demo.pdks import ply
from spira.lpe.containers import __CellContainer__
from spira.lne.net import Net
from demo.pdks.templates.devices import Device
from copy import copy, deepcopy


RDD = spira.get_rule_deck()


class BoundingBox(__CellContainer__):
    """ Add a GROUND bbox to Device for primitive and DRC
    detection, since GROUND is only in Mask Cell. """

    midpoint = param.MidPointField()

    def create_elementals(self, elems):
        c_cell = deepcopy(self.cell)

        polygons = spira.ElementList()
        Em = c_cell.elementals.flat_copy()
        for e in Em:
            polygons += e

        setter = {}
        for p in polygons:
            layer = p.gdslayer.number
            setter[layer] = 'not_set'

        for p in polygons:
            for pl in RDD.PLAYER.get_physical_layers(purposes=['METAL', 'GND']):
                if pl.layer == p.gdslayer:
                    if setter[pl.layer.number] == 'not_set':
                        l1 = spira.Layer(name='BoundingBox', number=pl.layer.number, datatype=9)
                        ply = spira.Polygons(shape=self.cell.pbox, gdslayer=l1)
                        ply.center = self.midpoint
                        elems += ply
                        setter[pl.layer.number] = 'already_set'
        return elems


class __Mask__(__CellContainer__):
    level = param.IntegerField(default=1)

    alias = param.StringField()
    player = param.PhysicalLayerField()
    level = param.IntegerField(default=1)
    lcar = param.IntegerField(default=0.1)
    algorithm = param.IntegerField(default=6)

    metals = param.DataField(fdef_name='create_flatten_metals')
    merged_layers = param.DataField(fdef_name='create_merged_layers')

    def create_flatten_metals(self):
        metal_elems = spira.ElementList()
        R = self.cell.routes.flat_copy()
        B = self.cell.boxes.flat_copy()
        Rm = R.get_polygons(layer=self.player.layer)
        Bm = B.get_polygons(layer=self.player.layer)
        for e in Rm:
            metal_elems += e
        for e in Bm:
            metal_elems += e
        return metal_elems

    def create_merged_layers(self):
        points = []
        elems = spira.ElementList()
        for p in self.metals:
            assert isinstance(p, spira.Polygons)
            for pp in p.polygons:
                points.append(pp)
        if points:
            shape = shapes.Shape(points=points)
            shape.apply_merge
            for pts in shape.points:
                elems += spira.Polygons(shape=[pts])
        return elems

    def create_elementals(self, elems):
        player = None
        for k, v in RDD.PLAYER.items:
            if v.layer == self.player.layer:
                player = v

        for i, poly in enumerate(self.merged_layers):
            assert isinstance(poly, spira.Polygons)
            if player is not None:
                ml = ply.Polygon(
                    name='ply_{}_{}'.format(self.alias, i),
                    player=player,
                    points=poly.polygons,
                    level=self.level
                )
                elems += ml
        return elems


class Metal(__Mask__):
    pass


class Native(__Mask__):
    pass


class Gate(__CellContainer__):
    """
    Decorates all elementas with purpose metal with
    LCells and add them as elementals to the new class.
    """

    metal_layers = param.DataField(fdef_name='create_metal_layers')
    level = param.IntegerField(default=2)
    device_ports = param.DataField(fdef_name='create_device_ports')
    lcar = param.IntegerField(default=0.1)
    algorithm = param.IntegerField(default=6)

    def create_device_ports(self):
        ports = spira.ElementList()
        for R in self.cell.routes:
            pp = R.ref.elementals.polygons
            if len(pp) > 0:
                g = R.ref.elementals.polygons[0]
                for D in self.cell.elementals.sref:
                    if issubclass(type(D.ref), Device):
                        for S in D.ref.elementals:
                            if isinstance(S.ref, mask.Metal):
                                for M in S.ref.elementals:

                                    ply = deepcopy(M.polygon)
                                    ply.move(midpoint=ply.center, destination=S.midpoint)

                                    P = M.metal_port._copy()
                                    P.connect(D, ply)
                                    d = D.midpoint
                                    P.move(midpoint=P.midpoint, destination=d)
                                    ports += P

        return ports

    def get_metal_polygons(self, pl):
        elems = self.elementals
        ply_elems = spira.ElementList()
        for S in elems.sref:
            if isinstance(S.ref, Metal):
                for M in S.ref.elementals:
                    if M.layer.is_equal_number(pl.layer):
                        if M.polygon.gdslayer.datatype in (1, 2):
                            ply_elems += M.polygon
        return ply_elems

    def create_nets(self, nets):
        for pl in RDD.PLAYER.get_physical_layers(purposes='METAL'):
            metal_elems = self.get_metal_polygons(pl)
            if metal_elems:
                print('boxxxx')
                print(self.cell.boxes)
                net = Net(
                    name='{}'.format(pl.layer.number),
                    lcar=self.lcar,
                    level=self.level,
                    algorithm=self.algorithm,
                    layer=pl.layer,
                    polygons=metal_elems,
                    primitives=self.ports,
                    bounding_boxes=self.cell.boxes
                )
                nets += net.graph
        return nets

    def create_netlist(self):
        self.g = self.merge
        self.g = self.nodes_combine(algorithm='d2d')
        # self.g = self.nodes_combine(algorithm='s2s')
        self.plot_netlist(G=self.g, graphname=self.name, labeltext='id')
        return self.g

    def create_metal_layers(self):
        elems = spira.ElementList()
        for player in RDD.PLAYER.get_physical_layers(purposes='METAL'):
            alias = '{}_{}'.format(
                player.layer.number,
                self.cell.id
            )
            metal = Metal(
                alias=alias,
                cell=self.cell,
                player=player,
                level=self.level
            )
            elems += spira.SRef(metal)
        return elems

    def create_elementals(self, elems):
        for e in self.metal_layers:
            elems += e
        return elems

    def create_ports(self, ports):
        for p in self.device_ports:
            ports += p
        for p in self.cell.terms:
            ports += p
        return ports


class Circuit(spira.Cell):
    """ A Cell encapsulates a set of elementals that
    describes the layout being generated. """

    routes = param.ElementalListField(fdef_name='create_routes')
    boxes = param.ElementalListField(fdef_name='create_boxes')
    lcar = param.IntegerField(default=0.1)
    algorithm = param.IntegerField(default=6)
    level = param.IntegerField(default=1)
    mask = param.DataField(fdef_name='create_mask')
    devices = param.DataField(fdef_name='create_devices')

    def __init__(self, elementals=None, ports=None, nets=None, routes=None, boxes=None, library=None, **kwargs):
        super().__init__(elementals=None, ports=None, nets=None, library=None, **kwargs)

        if routes is not None:
            self.routes = routes
        if boxes is not None:
            self.boxes = boxes

    def create_routes(self, routes):
        return routes

    def create_boxes(self, boxes):
        return boxes

    def __repr__(self):
        if hasattr(self, 'elementals'):
            elems = self.elementals
            return ("[SPiRA: Circuit(\'{}\')] " +
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
            return "[SPiRA: Cell(\'{}\')]".format(self.__class__.__name__)

    # FIXME: Has to be placed here for deepcopy().
    def __str__(self):
        return self.__repr__()

    def _copy(self):
        cell = Circuit(
            name=self.name,
            elementals=deepcopy(self.elementals),
            routes=deepcopy(self.routes),
            ports=deepcopy(self.ports),
            nets=self.nets
        )
        return cell

    def create_mask(self):
        cell = None
        if self.level == 2:
            cell = Layout(cell=self)
        elif self.level == 3:
            pass
        elif self.level == 4:
            pass
        return cell

    def create_netlist(self):
        self.mask.netlist

    def create_devices(self):
        """ Generate bounding boxes around each Device. """
        # FIXME: Assumes level 1 hierarchical cell.
        elems = spira.ElementList()
        for S in self.elementals.sref:
            if issubclass(type(S.ref), Device):
                elems += S
        return elems

    def create_boxes(self, boxes):
        """ Generate bounding boxes around each Device. """
        # FIXME: Assumes level 1 hierarchical cell.
        for S in self.elementals.sref:
            if issubclass(type(S.ref), Device):
                boxes += BoundingBox(cell=S.ref, midpoint=S.midpoint)
        return boxes


class Layout(__CellContainer__):
    """  """

    def create_elementals(self, elems):
        elems += spira.SRef(Gate(cell=self.cell))
        for e in self.cell.devices:
            elems += e
        return elems

    def create_nets(self, nets):
        for s in self.elementals.sref:
            g = s.ref.netlist
            if g is not None:
                for n in g.nodes():
                    p = np.array(g.node[n]['pos'])
                    m = np.array(s.midpoint)
                    g.node[n]['pos'] = p + m
                nets += g
        return nets

    def create_netlist(self):
        self.g = self.merge
        self.g = self.nodes_combine(algorithm='d2s')
        # self.g = self.nodes_combine(algorithm='d2d')
        # self.g = self.nodes_combine(algorithm='s2s')

        self.plot_netlist(G=self.g, graphname=self.name, labeltext='id')

