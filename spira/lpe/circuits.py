import spira
import numpy as np
from spira import param, shapes
from spira.lpe import mask
from demo.pdks import ply
from spira.lpe.containers import __CellContainer__
from spira.lne.net import Net
from copy import copy, deepcopy
from spira.lpe.mask_layers import Metal
from spira.lpe.devices import __Device__, DeviceLayout
from spira.lpe.devices import Gate

from spira.lgm.route.manhattan_base import RouteManhattan
from spira.lgm.route.basic import RouteShape, RouteBasic, Route


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


class Circuit(__CellContainer__):
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

    def create_netlist(self):
        self.mask.netlist

    def create_routes(self, routes):
        if self.cell.name is not None:
            for e in self.cell.elementals:
                if issubclass(type(e), spira.Polygons):
                    routes += e
        return routes

    def create_mask(self):
        cell = None
        if self.level == 2:
            cell = Layout(cell=self)
            # cell = Gate(cell=self, level=2)
        elif self.level == 3:
            pass
        elif self.level == 4:
            pass
        return cell

    def w2n(self, new_cell, c, c2dmap):
        for e in c.elementals:
            if isinstance(e, spira.SRef):
                S = deepcopy(e)
                if e.ref in c2dmap:
                    S.ref = c2dmap[e.ref]
                    new_cell += S

    def create_devices(self):
        # FIXME: Assumes level 1 hierarchical cell.
        elems = spira.ElementList()
        if self.cell is None:
            print('A')
            for S in self.elementals.sref:
                if issubclass(type(S.ref), __Device__):
                    elems += S
        else:
            deps = self.cell.dependencies()
            c2dmap = {}
            for key in RDD.DEVICES.keys:
                D = RDD.DEVICES[key].PCELL
                # FIXME!!!
                D.center = (0,0)
                for C in deps:
                    L = DeviceLayout(cell=C, level=1)
                    D.metals = L.metals
                    D.contacts = L.contacts
                    c2dmap.update({C: D})
            for c in self.cell.dependencies():
                self.w2n(elems, c, c2dmap)
        return elems

    def create_boxes(self, boxes):
        """ Generate bounding boxes around each Device. """
        # FIXME: Assumes level 1 hierarchical cell.
        for S in self.devices:
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

