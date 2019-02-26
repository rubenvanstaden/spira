import spira
import time
import numpy as np
from spira import param
from demo.pdks import ply
from copy import copy, deepcopy
from spira.gdsii.io import current_path
from spira.lpe.circuits import Circuit
from spira.lpe.devices import Device, DeviceLayout
from spira.lpe.containers import __CellContainer__, __NetContainer__, __CircuitContainer__

from spira.lgm.route.manhattan_base import Route
from spira.lgm.route.basic import RouteShape, RouteBasic
from spira.lpe.pcells import  __NetlistCell__
from spira.lpe.boxes import BoundingBox
from spira.lpe.pcells import __PolygonOperator__

from demo.pdks.process.mitll_pdk.database import RDD
from spira.lpe.mask import Metal
from spira.gdsii.utils import offset_operation as offset


class CircuitTemplate(__CellContainer__):
    pass


class RouteDevice(__PolygonOperator__):
    """ A Cell encapsulates a set of elementals that
    describes the layout being generated. """

    # level = param.IntegerField(default=1)
    # lcar = param.IntegerField(default=0.00001)

    def __init__(self, name=None, elementals=None, ports=None, nets=None, metals=None, library=None, **kwargs):
        super().__init__(name=None, elementals=None, ports=None, nets=None, library=None, **kwargs)

        if metals is not None:
            self.metals = metals

    def get_local_devices(self):
        prim_elems = spira.ElementList()
        for N in self.contacts:
            prim_elems += N
        # FIXME: Works for ytron, fails for junction.
        # for P in self.ports:
        #     prim_elems += P
        return prim_elems

    def create_elementals(self, elems):
        metals = Metal(elementals=self.merged_layers, level=self.level)
        elems += spira.SRef(metals)
        return elems

    def create_ports(self, ports):
        """ Activate the edge ports to be used in
        the Device for metal connections. """

        for i, m in enumerate(self.metals):
            for p in m.ports:
                if isinstance(p, spira.Term):
                    edgelayer = deepcopy(p.gdslayer)
                    edgelayer.datatype = 90
                    arrowlayer = deepcopy(p.gdslayer)
                    arrowlayer.datatype = 81
                    term = spira.Term(
                        name='{}_{}'.format(i, p.name),
                        gdslayer=deepcopy(m.player.layer),
                        midpoint=deepcopy(p.midpoint),
                        orientation=deepcopy(p.orientation),
                        reflection=p.reflection,
                        edgelayer=edgelayer,
                        arrowlayer=arrowlayer,
                        width=p.width,
                        length=deepcopy(p.length)
                    )

                    ports += term

        return ports



class Mask(__CircuitContainer__):

    level = param.IntegerField(default=1)
    terminals = param.ElementalListField()
    route_points = param.DataField(fdef_name='create_route_points')
    metal_ports = param.DataField(fdef_name='get_metal_ports')
    route_ports = param.DataField(fdef_name='get_route_ports')

    def create_devices(self, elems):
        for S in self.cell.elementals.sref:
            elems += S
        return elems

    # def get_metal_ports(self):
    #     metal_ports = {}
    #     for i, D in enumerate(self.devices):
    #         for S in D.ref.elementals:
    #             if isinstance(S.ref, Metal):
    #                 for proces_device_metal in S.ref.elementals:

    #                     M = deepcopy(proces_device_metal)
    #                     M_ply = M.polygon

    #                     # if D.rotation is not None:
    #                     #     D.rotation = (-1) * D.rotation

    #                     tf = {
    #                         'midpoint': D.midpoint,
    #                         'rotation': D.rotation,
    #                         'magnification': D.magnification,
    #                         'reflection': D.reflection
    #                     }

    #                     M_ply.transform(tf)

    #                     key = (D.__str__(), M_ply)

    #                     metal_ports[key] = []
                        
    #                     for name, port in D.ports.items():
    #                         if isinstance(port, spira.Term):
    #                             metal_ports[key].append(port)

    #     return metal_ports

    def get_metal_ports(self):
        metal_ports = {}
        for i, D in enumerate(self.devices):
            for S in D.ref.metals:

                M = deepcopy(S)
                M_ply = M.polygon
                
                # if D.rotation is not None:
                #     D.rotation = (-1) * D.rotation

                tf = {
                    'midpoint': D.midpoint,
                    'rotation': D.rotation,
                    'magnification': D.magnification,
                    'reflection': D.reflection
                }

                M_ply.transform(tf)

                key = (D.__str__(), M_ply)

                metal_ports[key] = []
                
                for name, port in D.ports.items():
                    if isinstance(port, spira.Term):
                        metal_ports[key].append(port)

        return metal_ports

    def get_route_ports(self):

        for R_ply, R_edges in self._new_routes.items():

            for key, ports in self.metal_ports.items():
                D_str, M_ply = key[0], key[1]
                # if M_ply.gdslayer.number == R_ply.gdslayer.number:

                #     B = my_blocks[D_str]

                #     for port in ports:
                #         for route_edge_port in R_edges:
                #             rp = route_edge_port
                #             # if M_ply & rp.edge:
                #             # for mp in M_ply.shape.points:
                #             if rp.encloses_midpoint(port.edge.polygons):
                #                 edgelayer = deepcopy(rp.gdslayer)
                #                 edgelayer.number = R_ply.gdslayer.number
                #                 edgelayer.datatype = 76
                #                 r_term = spira.Term(
                #                     name=rp.name,
                #                     gdslayer=deepcopy(rp.gdslayer),
                #                     midpoint=deepcopy(rp.midpoint),
                #                     orientation=deepcopy(rp.orientation),
                #                     reflection=rp.reflection,
                #                     edgelayer=edgelayer,
                #                     width=rp.width,
                #                 )
                #                 # B += r_term
                #                 # boxes += B
    
                #     # for port in ports:
                #     #     # if R_ply & port.edge:
                #     #     for mp in R_ply.shape.points:
                #     #         if port.encloses(mp):
                #     #             edgelayer = deepcopy(port.gdslayer)
                #     #             edgelayer.number = R_ply.gdslayer.number
                #     #             edgelayer.datatype = 75
                #     #             m_term = spira.Term(
                #     #                 name=port.name,
                #     #                 gdslayer=deepcopy(port.gdslayer),
                #     #                 midpoint=deepcopy(port.midpoint),
                #     #                 orientation=deepcopy(port.orientation),
                #     #                 reflection=port.reflection,
                #     #                 edgelayer=edgelayer,
                #     #                 width=port.width,
                #     #             )
                #     #             B += m_term
                #     #             boxes += B

    # def create_route_points(self):
    #     if self.cell is not None:
    #         routes = {}
    #         cell = deepcopy(self.cell)
    #         flat_plys = cell.flat_copy()

    #         for player in RDD.PLAYER.get_physical_layers(purposes='METAL'):
    
    #             route_points = []
    #             device_points = []
    
    #             polygons = flat_plys.get_polygons(layer=player.layer, cell_type=0)
    #             for e in polygons:
    #                 route_points.extend(e.shape.points)
    
    #             if len(route_points) > 0:
    #                 route_polygon = spira.Polygons(
    #                     shape=route_points, 
    #                     gdslayer=spira.Layer(number=player.layer.number, datatype=0)
    #                 )
    #                 # elems += route_polygon
    #             else:
    #                 route_polygon = None
    
    #             polygons = flat_plys.get_polygons(layer=player.layer, cell_type=1)
    #             for e in polygons:
    #                 points = []
    #                 for pts in e.shape.points:
    #                     p = utils.offset_operation(points=pts, size='up')
    #                     # print(p)
    #                     points.extend(p)
    #                 print(points)
    #                 device_points.extend(points)
    
    #             if len(device_points) > 0:
    #                 device_polygon = spira.Polygons(
    #                     shape=device_points, 
    #                     gdslayer=spira.Layer(number=player.layer.number, datatype=1)
    #                 )
    #                 # elems += device_polygon
    #             else:
    #                 device_polygon = None
    
    #             if (route_polygon is not None) and (device_polygon is not None):
    #                 points = route_polygon - device_polygon
    #             else:
    #                 points = None
    
    #             if points is not None:
    #                 routes[player] = points
    
    #         return routes
    
    def create_elementals(self, elems):

        # if self.cell is not None:
        #     routes = {}
        #     cell = deepcopy(self.cell)
        #     flat_plys = cell.flat_copy()
    
        #     for player in RDD.PLAYER.get_physical_layers(purposes='METAL'):
    
        #         route_points = []
        #         device_points = []
    
        #         polygons = flat_plys.get_polygons(layer=player.layer, cell_type=0)
        #         for e in polygons:
        #             route_points.extend(e.shape.points)
    
        #         if len(route_points) > 0:
        #             route_polygon = spira.Polygons(
        #                 shape=route_points, 
        #                 gdslayer=spira.Layer(number=player.layer.number, datatype=0)
        #             )
        #             elems += route_polygon
        #         else:
        #             route_polygon = None
    
        #         polygons = flat_plys.get_polygons(layer=player.layer, cell_type=1)
        #         for e in polygons:
        #             points = []
        #             for pts in e.shape.points:
        #                 p = offset(points=pts, offset_type='up')
        #                 points.extend(p)
        #             device_points.extend(points)
    
        #         if len(device_points) > 0:
        #             device_polygon = spira.Polygons(
        #                 shape=device_points, 
        #                 gdslayer=spira.Layer(number=player.layer.number, datatype=1)
        #             )
        #             elems += device_polygon
        #         else:
        #             device_polygon = None
    
        #         if (route_polygon is not None) and (device_polygon is not None):
        #             points = route_polygon - device_polygon
        #         else:
        #             points = None
    
        #         if points is not None:
        #             layer = spira.Layer(number=player.layer.number, datatype=2)
        #             elems += spira.Polygons(shape=points, gdslayer=layer)
    
        # for pl, points in self.route_points.items():
        #     layer = spira.Layer(number=pl.layer.number, datatype=2)
        #     elems += spira.Polygons(shape=points, gdslayer=layer)

        # for key, ports in self.metal_ports.items():
        #     D_str, M_ply = key[0], key[1]
        #     elems += M_ply
        #     for port in ports:
        #         self.ports += port

        for R in self.routes:

            for D in self.devices:

                for S in D.ref.metals:
                    M = deepcopy(S)
                    M_ply = M.polygon
                    tf = {
                        'midpoint': D.midpoint,
                        'rotation': D.rotation,
                        'magnification': D.magnification,
                        'reflection': D.reflection
                    }
                    M_ply.transform(tf)
                    # for S in R.ref.metals:
                    for key, port in R.ports.items():
                        # for rp in S.ports:
                        # print(port.edge)
                        # print(port.edge.shape.points)
                        # print(M_ply)
                        # print(M_ply.shape.points)
                        # print('')
                        if M_ply & port.edge:
                            elems += port.edge

        # for R in self.routes:
        #     elems += R

        return elems

    def create_routes(self, routes):

        # # FIXME: Only commit to cell after routes
        # # have passed all DRC checks.
        # if self.cell is not None:
        #     elems = spira.ElementList()
        #     cell = spira.Cell(name='RouteCell')
        #     for e in self.cell.elementals:
        #         if issubclass(type(e), spira.Polygons):
        #             for player in RDD.PLAYER.get_physical_layers(purposes='METAL'):
        #                 if player.layer.number == e.gdslayer.number:
        #                     cell += ply.Polygon(points=e.shape.points, player=player)
        #     elems += spira.SRef(cell)
        #     R = Route(elementals=elems)
        #     routes += spira.SRef(R)

        # for R in self.cell.routes:
        #     routes += R

        if self.cell is not None:
            metals = spira.ElementList()
            for e in self.cell.elementals:
                if issubclass(type(e), spira.Polygons):
                    for player in RDD.PLAYER.get_physical_layers(purposes='METAL'):
                        if player.layer.number == e.gdslayer.number:
                            metals += ply.Polygon(points=e.shape.points, player=player)
            R = RouteDevice(metals=metals)
            routes += spira.SRef(R)

        return routes

    @property
    def _new_routes(self):
        print('--- new routes ---')
        my_routes = {}
        if self.cell is not None:
            elems = spira.ElementList()
            cell = spira.Cell(name='RouteCell')
            for e in self.cell.elementals:
                if issubclass(type(e), spira.Polygons):
                    for player in RDD.PLAYER.get_physical_layers(purposes='METAL'):
                        if player.layer.number == e.gdslayer.number:
                            pc = ply.Polygon(points=e.shape.points, player=player)
                            my_routes[pc.polygon] = pc.edge_ports
                            cell += pc
            # elems += spira.SRef(cell)
            # R = Route(elementals=elems)
            # routes += spira.SRef(R)

        return my_routes

    def my_routes(self):
        # routes = spira.ElementList()
        if self.cell is not None:
            metals = spira.ElementList()
            for e in self.cell.elementals:
                if issubclass(type(e), spira.Polygons):
                    for player in RDD.PLAYER.get_physical_layers(purposes='METAL'):
                        if player.layer.number == e.gdslayer.number:
                            metals += ply.Polygon(points=e.shape.points, player=player)
            R = RouteDevice(metals=metals)
            self.cell.routes += spira.SRef(R)
            # self.cell.routes = routes
        return self.cell.routes

    def create_boxes(self, boxes):

        start = time.time()

        print('[*] Connecting routes with devices')

        my_blocks = {}

        for D in self.devices:
            B = BoundingBox(S=D)
            my_blocks[D.__str__()] = B

        for R in self.routes:

            for D in self.devices:

                for S in D.ref.metals:
                    M = deepcopy(S)
                    M_ply = M.polygon
                    tf = {
                        'midpoint': D.midpoint,
                        'rotation': D.rotation,
                        'magnification': D.magnification,
                        'reflection': D.reflection
                    }
                    M_ply.transform(tf)
                    # for S in R.ref.metals:
                    for key, port in R.ports.items():
                        # for rp in S.ports:
                        # if rp.gdslayer.number == M_ply.gdslayer.number:
                        B = my_blocks[D.__str__()]
                        for mp in M_ply.shape.points:
                            if port.encloses(mp):
                            # if M_ply & port.edge:
                                edgelayer = deepcopy(port.gdslayer)
                                # edgelayer.number = R_ply.gdslayer.number
                                edgelayer.datatype = 76
                                r_term = spira.Term(
                                    name=port.name,
                                    gdslayer=deepcopy(port.gdslayer),
                                    midpoint=deepcopy(port.midpoint),
                                    orientation=deepcopy(port.orientation),
                                    reflection=port.reflection,
                                    edgelayer=edgelayer,
                                    width=port.width,
                                )
    
                                key = (port.name, port.gdslayer.number)
                                # key = rp.node_id
                                R.port_locks[key] = False
                                # print(key)
    
                                commit = True
                                for p in B.ports:
                                    if p.__str__() == r_term.__str__():
                                        commit = False
                                if commit is True:
                                    B += r_term
                                com = True
                                for b in boxes:
                                    if b.__str__() == B.__str__():
                                        com = False
                                if com is True:
                                    boxes += B

                for S in R.ref.metals:
                    R_ply = S.polygon
                    for name, port in D.ports.items():
                        if isinstance(port, spira.Term):
                            if port.gdslayer.number == R_ply.gdslayer.number:
                                B = my_blocks[D.__str__()]
                                if R_ply & port.edge:
                                    edgelayer = deepcopy(port.gdslayer)
                                    edgelayer.number = R_ply.gdslayer.number
                                    edgelayer.datatype = 75
                                    m_term = spira.Term(
                                        name=port.name,
                                        gdslayer=deepcopy(port.gdslayer),
                                        midpoint=deepcopy(port.midpoint),
                                        orientation=deepcopy(port.orientation),
                                        reflection=port.reflection,
                                        edgelayer=edgelayer,
                                        width=port.width,
                                    )

                                    key = (port.name, port.gdslayer.number)
                                    # key = port.node_id
                                    D.port_locks[key] = False

                                    commit = True
                                    for p in B.ports:
                                        if p.__str__() == m_term.__str__():
                                            commit = False
                                    if commit is True:
                                        B += m_term
                                    com = True
                                    for b in boxes:
                                        if b.__str__() == B.__str__():
                                            com = False
                                    if com is True:
                                        boxes += B

        end = time.time()
        print('Block calculation time {}:'.format(end - start))
        return boxes




    # def create_boxes(self, boxes):

    #     start = time.time()

    #     print('[*] Connecting routes with devices')

    #     my_blocks = {}

    #     for D in self.devices:
    #         B = BoundingBox(S=D)
    #         my_blocks[D.__str__()] = B

    #     for R_ply, R_edges in self._new_routes.items():
    #         for D in self.devices:

    #             for S in D.ref.metals:
    #                 M = deepcopy(S)
    #                 M_ply = M.polygon
    #                 tf = {
    #                     'midpoint': D.midpoint,
    #                     'rotation': D.rotation,
    #                     'magnification': D.magnification,
    #                     'reflection': D.reflection
    #                 }
    #                 M_ply.transform(tf)
    #                 for route_edge_port in R_edges:
    #                     rp = route_edge_port
    #                     for mp in M_ply.shape.points:
    #                         if rp.encloses(mp):
    #                             edgelayer = deepcopy(rp.gdslayer)
    #                             edgelayer.number = R_ply.gdslayer.number
    #                             edgelayer.datatype = 76
    #                             r_term = spira.Term(
    #                                 name=rp.name,
    #                                 gdslayer=deepcopy(rp.gdslayer),
    #                                 midpoint=deepcopy(rp.midpoint),
    #                                 orientation=deepcopy(rp.orientation),
    #                                 reflection=rp.reflection,
    #                                 edgelayer=edgelayer,
    #                                 width=rp.width,
    #                             )
                                
    #                             # key = (port.name, port.gdslayer.number)
    #                             D.port_locks[key] = False

    #                             commit = True
    #                             for p in B.ports:
    #                                 if p.__str__() == r_term.__str__():
    #                                     commit = False
    #                             if commit is True:
    #                                 B += r_term
    #                             com = True
    #                             for b in boxes:
    #                                 if b.__str__() == B.__str__():
    #                                     com = False
    #                             if com is True:
    #                                 boxes += B

    #             for name, port in D.ports.items():
    #                 if isinstance(port, spira.Term):
    #                     if port.gdslayer.number == R_ply.gdslayer.number:
    #                         B = my_blocks[D.__str__()]
    #                         if R_ply & port.edge:
    #                             edgelayer = deepcopy(port.gdslayer)
    #                             edgelayer.number = R_ply.gdslayer.number
    #                             edgelayer.datatype = 75
    #                             m_term = spira.Term(
    #                                 name=port.name,
    #                                 gdslayer=deepcopy(port.gdslayer),
    #                                 midpoint=deepcopy(port.midpoint),
    #                                 orientation=deepcopy(port.orientation),
    #                                 reflection=port.reflection,
    #                                 edgelayer=edgelayer,
    #                                 width=port.width,
    #                             )

    #                             key = (port.name, port.gdslayer.number)
    #                             D.port_locks[key] = False

    #                             commit = True
    #                             for p in B.ports:
    #                                 if p.__str__() == m_term.__str__():
    #                                     commit = False
    #                             if commit is True:
    #                                 B += m_term
    #                             com = True
    #                             for b in boxes:
    #                                 if b.__str__() == B.__str__():
    #                                     com = False
    #                             if com is True:
    #                                 boxes += B

    #     end = time.time()
    #     print('Block calculation time {}:'.format(end - start))
    #     return boxes

    # def create_boxes(self, boxes):

    #     start = time.time()

    #     print('[*] Connecting routes with devices')

    #     my_blocks = {}

    #     for D in self.devices:
    #         B = BoundingBox(S=D)
    #         print(B)
    #         my_blocks[D.__str__()] = B

    #     for R_ply, R_edges in self._new_routes.items():
    #         for key, ports in self.metal_ports.items():
    #             D_str, M_ply = key[0], key[1]
    #             if M_ply.gdslayer.number == R_ply.gdslayer.number:

    #                 B = my_blocks[D_str]

    #                 # for route_edge_port in R_edges:
    #                 #     rp = route_edge_port
    #                 #     for mp in M_ply.shape.points:
    #                 #         if rp.encloses(mp):
    #                 #             edgelayer = deepcopy(rp.gdslayer)
    #                 #             edgelayer.number = R_ply.gdslayer.number
    #                 #             edgelayer.datatype = 76
    #                 #             r_term = spira.Term(
    #                 #                 name=rp.name,
    #                 #                 gdslayer=deepcopy(rp.gdslayer),
    #                 #                 midpoint=deepcopy(rp.midpoint),
    #                 #                 orientation=deepcopy(rp.orientation),
    #                 #                 reflection=rp.reflection,
    #                 #                 edgelayer=edgelayer,
    #                 #                 width=rp.width,
    #                 #             )

    #                 #             commit = True
    #                 #             for p in B.ports:
    #                 #                 if p.__str__() == r_term.__str__():
    #                 #                     commit = False

    #                 #             if commit is True:
    #                 #                 B += r_term

    #                 #                 if B not in boxes:
    #                 #                     boxes += B

    #                 for port in ports:
    #                     if R_ply & port.edge:
    #                         edgelayer = deepcopy(port.gdslayer)
    #                         edgelayer.number = R_ply.gdslayer.number
    #                         edgelayer.datatype = 75
    #                         m_term = spira.Term(
    #                             name=port.name,
    #                             gdslayer=deepcopy(port.gdslayer),
    #                             midpoint=deepcopy(port.midpoint),
    #                             orientation=deepcopy(port.orientation),
    #                             reflection=port.reflection,
    #                             edgelayer=edgelayer,
    #                             width=port.width,
    #                         )

    #                         commit = True
    #                         for p in B.ports:
    #                             if p.__str__() == m_term.__str__():
    #                                 commit = False

    #                         if commit is True:
    #                             B += m_term

    #                         com = True
    #                         for b in boxes:
    #                             if b.__str__() == B.__str__():
    #                                 com = False

    #                         if com is True:
    #                             boxes += B

    #                             # if B not in boxes:
    #                             #     boxes += B

    #     print('--------------------')
    #     for b in boxes:
    #         print(b)

    #     end = time.time()
    #     print('Block calculation time {}:'.format(end - start))
    #     return boxes

    def create_ports(self, ports):

        # # FIXME!!! Needed for terminal detection in the Mesh.
        # if self.cell is not None:
        #     cell = deepcopy(self.cell)
        #     flat_elems = cell.flat_copy()
        #     port_elems = flat_elems.get_polygons(layer=RDD.PURPOSE.TERM)
        #     label_elems = flat_elems.labels
        #     for port in port_elems:
        #         for label in label_elems:
        #             lbls = label.text.split(' ')
        #             s_p1, s_p2 = lbls[1], lbls[2]
        #             p1, p2 = None, None
        #             for m1 in RDD.PLAYER.get_physical_layers(purposes=['METAL', 'GND']):
        #                 if m1.layer.name == s_p1:
        #                     p1 = spira.Layer(name=lbls[0],
        #                         number=m1.layer.number,
        #                         datatype=RDD.GDSII.TEXT
        #                     )
        #                 if m1.layer.name == s_p2:
        #                     p2 = spira.Layer(name=lbls[0],
        #                         number=m1.layer.number,
        #                         datatype=RDD.GDSII.TEXT
        #                     )
        #             if p1 and p2 :
        #                 if label.encloses(ply=port.polygons[0]):
        #                     ports += spira.Term(
        #                         name=label.text,
        #                         layer1=p1, layer2=p2,
        #                         width=port.dx,
        #                         # length=port.dy,
        #                         midpoint=label.position
        #                     )

        return ports

    def create_terminals(self, ports):

        # # FIXME!!! Needed for terminal detection in the Mesh.
        # if self.cell is not None:
        #     cell = deepcopy(self.cell)
        #     flat_elems = cell.flat_copy()
        #     port_elems = flat_elems.get_polygons(layer=RDD.PURPOSE.TERM)
        #     label_elems = flat_elems.labels
        #     for port in port_elems:
        #         for label in label_elems:
        #             lbls = label.text.split(' ')
        #             s_p1, s_p2 = lbls[1], lbls[2]
        #             p1, p2 = None, None
        #             for m1 in RDD.PLAYER.get_physical_layers(purposes=['METAL', 'GND']):
        #                 if m1.layer.name == s_p1:
        #                     p1 = spira.Layer(name=lbls[0],
        #                         number=m1.layer.number,
        #                         datatype=RDD.GDSII.TEXT
        #                     )
        #                 if m1.layer.name == s_p2:
        #                     p2 = spira.Layer(name=lbls[0],
        #                         number=m1.layer.number,
        #                         datatype=RDD.GDSII.TEXT
        #                     )
        #             if p1 and p2 :
        #                 if label.encloses(ply=port.polygons[0]):
        #                     ports += spira.Term(
        #                         name=label.text,
        #                         layer1=p1, layer2=p2,
        #                         width=port.dx,
        #                         # length=port.dy,
        #                         midpoint=label.position
        #                     )

        return ports




def __wrapper__(c, c2dmap):
    for e in c.elementals.sref:
        if e.ref in c2dmap.keys():
            e.ref = c2dmap[e.ref]
            e._parent_ports = e.ref.ports
            e._local_ports = {(port.name, port.gdslayer.number):deepcopy(port) for port in e.ref.ports}
            e.port_locks = {(port.name, port.gdslayer.number):port.locked for port in e.ref.ports}
            # e._local_ports = {port.node_id:deepcopy(port) for port in e.ref.ports}
            # e.port_locks = {port.node_id:port.locked for port in e.ref.ports}


def device_detector(cell):
    c2dmap = {}
    for C in cell.dependencies():
        cc = deepcopy(C)
        L = DeviceLayout(name=C.name, cell=cc, level=1)
        if L.__type__ is not None:
            for key in RDD.DEVICES.keys:
                if L.__type__ == key:
                    D = RDD.DEVICES[key].PCELL(metals=L.metals, contacts=L.contacts)
                    c2dmap.update({C: D})
            for key in RDD.VIAS.keys:
                if L.__type__ == key:
                    D = RDD.VIAS[key].DEFAULT(metals=L.metals, contacts=L.contacts)
                    c2dmap.update({C: D})
        else:
            c2dmap.update({C: C})
    for c in cell.dependencies():
        __wrapper__(c, c2dmap)
    return c2dmap[cell]


def circuit_detector(cell):
    c2dmap = {}
    for C in cell.dependencies():
        if not issubclass(type(C), Device):
            if ('Metal' not in C.name) and ('Native' not in C.name):
                D = Mask(cell=C, level=2)
                c2dmap.update({C: D})
        else:
            c2dmap.update({C: C})
    for c in cell.dependencies():
        __wrapper__(c, c2dmap)
    return c2dmap[cell]


if __name__ == '__main__':

    start = time.time()

    # name = 'jj_mitll_2'
    # name = 'mitll_jtl_double'
    # name = 'mitll_dsndo_xic'
    # name = 'mitll_SFQDC_draft'
    # name = 'splitt_v0.3'
    # name = 'ex5'
    # name = 'LSmitll_DCSFQ_new'
    # name = 'LSmitll_NOT_new'
    # name = 'LSmitll_MERGET_new'
    # name = 'LSmitll_jtl_new'
    # name = 'LSmitll_SFQDC'
    # name = 'LSmitll_SPLITT_new'
    name = 'LSmitll_ptlrx_new'
    # name = 'LSmitll_DFFT_new'

    filename = current_path(name)
    input_cell = spira.import_gds(filename=filename)

    cv_cell = device_detector(cell=input_cell)
    ms_cell = circuit_detector(cell=cv_cell)
    circuit = Circuit(cell=ms_cell)

    # circuit.netlist
    circuit.output()

    # --- Debugging ---
    # input_cell.output()
    # cv_cell.output()
    # ms_cell.output()

    end = time.time()
    print(end - start)

