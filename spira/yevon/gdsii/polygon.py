import gdspy
import pyclipper
import numpy as np

from spira.core.transforms import stretching
from spira.yevon.geometry import bbox_info
from spira.yevon.utils import clipping
from copy import copy, deepcopy
from spira.yevon.gdsii.elem_list import ElementalList
from spira.yevon.visualization import color
from spira.yevon.gdsii.base import __LayerElemental__
from spira.yevon.geometry.coord import CoordField, Coord
from spira.yevon.visualization.color import ColorField
from spira.core.parameters.descriptor import DataFieldDescriptor, FunctionField, DataField
from spira.yevon.geometry.ports.base import __Port__
from spira.core.parameters.variables import *
from spira.core.transforms.stretching import *
from spira.yevon.geometry.shapes import Shape, ShapeField
from spira.yevon.geometry import shapes
from spira.yevon.gdsii.group import Group
from spira.yevon.process.gdsii_layer import Layer
from spira.yevon.process.physical_layer import PhysicalLayer
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = [
    'Polygon',
    'Rectangle',
    'Box',
    'Circle',
    'Convex',
    'Cross',
    'Wedge',
    'Parabolic',
    'PolygonGroup'
]


class __Polygon__(__LayerElemental__):

    shape = ShapeField()
    enable_edges = BoolField(default=True)

    def __hash__(self):
        return hash(self.id)

    def encloses(self, point):
        # return not pyclipper.PointInPolygon(point, self.points) == 0
        shape = self.shape.transform_copy(self.transformation)
        return not pyclipper.PointInPolygon(point, shape.points) == 0

    def expand_transform(self):
        from spira.core.transforms.identity import IdentityTransform
        if not self.transformation.is_identity():
            self.shape = self.shape.transform_copy(self.transformation)
            self.transformation = IdentityTransform()
        return self

    def flat_copy(self, level = -1):
        S = Polygon(layer=self.layer, shape=self.shape, transformation=self.transformation)
        S.expand_transform()
        return S

    def fillet(self, radius, angle_resolution=128, precision=0.001):
        super().fillet(radius=radius, points_per_2pi=angle_resolution, precision=precision)
        self.shape.points = self.polygons
        return self

    def stretch(self, factor=(1,1), center=(0,0)):
        T = spira.Stretch(stretch_factor=factor, stretch_center=center)
        return T.apply(self)

    def stretch_copy(self, factor=(1,1), center=(0,0)):
        T = spira.Stretch(stretch_factor=factor, stretch_center=center)
        return T.apply_copy(self)

    def stretch_port(self, port, destination):
        """
        The elemental by moving the subject port, without 
        distorting the entire elemental. Note: The opposite 
        port position is used as the stretching center.
        """
        opposite_port = bbox_info.get_opposite_boundary_port(self, port)
        T = stretching.stretch_elemental_by_port(self, opposite_port, port, destination)
        T.apply(self)
        return self

    def move(self, midpoint=(0,0), destination=None, axis=None):
        """  """

        if destination is None:
            destination = midpoint
            midpoint = Coord(0,0)

        if isinstance(midpoint, Coord):
            m = midpoint
        elif np.array(midpoint).size == 2:
            m = Coord(midpoint)
        elif issubclass(type(midpoint), __Port__):
            m = midpoint.midpoint
        else:
            raise ValueError('Midpoint error')

        if issubclass(type(destination), __Port__):
            d = destination.midpoint
        if isinstance(destination, Coord):
            d = destination
        elif np.array(destination).size == 2:
            d = Coord(destination)
        else:
            raise ValueError('Destination error')

        dxdy = d - m 
        self.translate(dxdy)
        return self


class Polygon(__Polygon__):
    """ 
    Elemental that connects shapes to the GDSII file format.
    Polygon are objects that represents the shapes in a layout.

    Examples
    --------
    >>> layer = spira.Layer(number=99)
    >>> rect_shape = spira.RectangleShape(p1=[0,0], p2=[1,1])
    >>> ply = spira.Polygon(shape=rect_shape, layer=layer)
    """

    edges = DataField(fdef_name='create_edges')

    def get_alias(self):
        if not hasattr(self, '__alias__'):
            self.__alias__ = self.process
        return self.__alias__

    def set_alias(self, value):
        if value is not None:
            self.__alias__ = value

    alias = FunctionField(get_alias, set_alias, doc='Functions to generate an alias for cell name.')

    _next_uid = 0

    def __init__(self, shape, layer, **kwargs):
        super().__init__(shape=shape, layer=layer, **kwargs)
        
        self.uid = Polygon._next_uid
        Polygon._next_uid += 1

    def __repr__(self):
        if self is None:
            return 'Polygon is None!'
        layer = RDD.GDSII.IMPORT_LAYER_MAP[self.layer]
        class_string = "[SPiRA: Polygon \'{}\'] (center {}, vertices {}, process {}, purpose {})"
        return class_string.format(self.alias, self.center, self.count, self.process, self.purpose)

    def __str__(self):
        return self.__repr__()

    def id_string(self):
        sid = '{} - hash {}'.format(self.__repr__(), self.shape.hash_string)
        return sid

    # NOTE: We are not copying the ports, so they
    # can be re-calculated for the transformed shape.
    def __deepcopy__(self, memo):
        # return Polygon(
        return self.__class__(
            shape=deepcopy(self.shape),
            layer=deepcopy(self.layer),
            transformation=deepcopy(self.transformation)
        )

    def convert_to_gdspy(self, transformation=None):
        """
        Converts a SPiRA polygon to a Gdspy polygon.
        The extra transformation parameter is the
        polygon edge ports.
        """
        layer = RDD.GDSII.EXPORT_LAYER_MAP[self.layer]
        T = self.transformation + transformation
        shape = deepcopy(self.shape).transform(T)
        # shape = self.shape
        return gdspy.Polygon(
            points=shape.points,
            layer=layer.number,
            datatype=layer.datatype,
            verbose=False
        )

    def create_edges(self):
        from spira.yevon.structure.edges import generate_polygon_edges
        return generate_polygon_edges(shape=self.shape, layer=self.layer)

    def nets(self, contacts=None, lcar=100):
        from spira.yevon.geometry.nets.net import Net
        from spira.yevon.vmodel.geometry import GmshGeometry
        from spira.yevon.geometry.ports.port import ContactPort
        from spira.yevon.filters.net_label_filter import NetProcessLabelFilter, NetDeviceLabelFilter, NetEdgeFilter

        if self.purpose == 'METAL':
            # geometry = GmshGeometry(lcar=0.1*1e-6, process=self.layer.process, process_polygons=[deepcopy(self)])
            geometry = GmshGeometry(lcar=1*1e-6, process=self.layer.process, process_polygons=[deepcopy(self)])
    
            net = Net(name=self.process, geometry=geometry)
    
            # # Fs += NetDeviceLabelFilter(device_ports=contacts)
    
            # cc = []
            # for p in self.ports:
            #     if isinstance(p, ContactPort):
            #         cc.append(p)
            # print(cc)
    
            Fs = NetProcessLabelFilter(process_polygons=[deepcopy(self)])
            Fs += NetEdgeFilter(process_polygons=[deepcopy(self)])
            # # Fs += NetDeviceLabelFilter(device_ports=cc)
    
            net = Fs(net)

            return net
    
            # # from spira.yevon.utils.netlist import combine_net_nodes
            # # net.g = combine_net_nodes(g=net.g, algorithm='d2d')
            # # net.g = combine_net_nodes(g=net.g, algorithm='s2s')
    
            # from spira.yevon.geometry.nets.net import CellNet
            # cn = CellNet()
            # cn.g = net.g
            # # cn.generate_branches()
            # # cn.detect_dummy_nodes()
            # return cn

        return []
    


    # def nets(self, contacts):
    #     from spira.yevon.geometry.nets.net import Net
    #     from spira.yevon.geometry.nets.net_list import NetList
    #     from spira.yevon.vmodel.virtual import virtual_process_model
    #     from spira.yevon.filters.net_label_filter import NetProcessLabelFilter, NetDeviceLabelFilter
    #     from spira.yevon.gdsii.cell import Cell
    #     from spira.yevon.gdsii.elem_list import ElementalList

    #     D = Cell(name=self.alias)
    #     D += deepcopy(self)
    #     # shape = self.shape.transform(self.transformation)
    #     # P = Polygon(shape, layer=deepcopy(self.layer))
    #     # D += P
        
    #     # if RDD.ENGINE.GEOMETRY == 'GMSH_ENGINE':
    #     #     process_geom[pg.process] = GmshGeometry(
    #     #         process=pg.process, 
    #     #         process_polygons=pg.elementals
    #     #     )
    #     # else:
    #     #     raise ValueError('Geometry engine type not specificied in RDD.')

    #     vp = virtual_process_model(device=D, process_flow=RDD.VMODEL.PROCESS_FLOW)
    #     for process, geometry in vp.geometry.items():
    #         net = Net(name=self.__repr__(), geometry=geometry)

    #         pp = ElementalList()

    #         for e in geometry.process_polygons:
    #             if e.layer.process == process:
    #                 pp += e
    #         # print(pp)

    #         # for e in D.process_elementals:
    #         #     if e.layer.process == process:
    #         #         pp += e
    #         # print(pp)

    #         # print('\n[*] Contacts:')
    #         # for c in contacts:
    #         #     print(c)
    #         # print('')

    #         Fs = NetProcessLabelFilter(process_polygons=pp)
    #         Fs += NetDeviceLabelFilter(device_ports=contacts)
    #         # Fs += spira.NetBlockLabelFilter(references=self.elementals.sref)

    #         # net = Fs(net).transform(self.transformation)
    #         net = Fs(net)
    #     return net


class PolygonGroup(Group, __LayerElemental__):
    """ 
    Collection of polygon elementals. Boolean
    operation can be applied on these polygons.

    Example
    -------
    >>> cp = spira.PolygonCollection()
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)       

    def __repr__(self):
        class_string = "[SPiRA: PolygonGroup] (polygons {}, process {}, purpose {})"
        return class_string.format(self.count, self.process, self.purpose)

    def __str__(self):
        return self.__repr__()

    def __and__(self, other):
    
        el = ElementalList()
        for e1 in self.elementals:
            for e2 in other.elementals:
                if e1.shape != e2.shape:
                    e1 = deepcopy(e1)
                    e2 = deepcopy(e2)
                    # polygons = e1 & e2
                    polygons = e1.intersection(e2)
                    for p in polygons:
                        p.layer.purpose = RDD.PURPOSE.INTERSECTED
                    for p in polygons:
                        el += p
        self.elementals = el
        return self

    # def __and__(self, other):
    #     pts1, pts2 = [], []
    #     for e in self.elementals:
    #         s1 = e.shape.transform_copy(e.transformation)
    #         pts1.append(s1.points)
    #     for e in other.elementals:
    #         s1 = e.shape.transform_copy(e.transformation)
    #         pts2.append(s1.points)

    #     if (len(pts1) > 0) and (len(pts2) > 0):
    #         p1 = gdspy.PolygonSet(polygons=pts1)
    #         p2 = gdspy.PolygonSet(polygons=pts2)
    #         ply = gdspy.fast_boolean(p1, p2, operation='and')
    #         elems = ElementalList()
    #         if ply is not None:
    #             for points in ply.polygons:
    #                 elems += Polygon(shape=points, layer=self.layer)
    #         self.elementals = elems
    #     return self

    def __xor__(self, other):
        pts1, pts2 = [], []
        for e in self.elementals:
            s1 = e.shape.transform_copy(e.transformation)
            pts1.append(s1.points)
        for e in other.elementals:
            s1 = e.shape.transform_copy(e.transformation)
            pts2.append(s1.points)

        if (len(pts1) > 0) and (len(pts2) > 0):
            p1 = gdspy.PolygonSet(polygons=pts1)
            p2 = gdspy.PolygonSet(polygons=pts2)
    
            ply = gdspy.fast_boolean(p1, p2, operation='not')
            elems = ElementalList()
            for points in ply.polygons:
                elems += Polygon(shape=points, layer=self.layer)
            self.elementals = elems
        return self

    def __or__(self, other):
        raise ValueError('Not Implemented!')

    @property
    def count(self):
        return len(self.elementals)

    @property
    def process(self):
        layer = RDD.GDSII.IMPORT_LAYER_MAP[self.layer]
        return layer.process

    @property
    def purpose(self):
        layer = RDD.GDSII.IMPORT_LAYER_MAP[self.layer]
        return layer.purpose

    @property
    def center(self):
        return self.bbox_info.center

    @property
    def intersect(self):
        elems = ElementalList()
        el1 = deepcopy(self.elementals)
        el2 = deepcopy(self.elementals)
        for i, e1 in enumerate(el1):
            for j, e2 in enumerate(el2):
                if i != j:
                    polygons = e1 & e2
                    for p in polygons:
                        p.layer.purpose = RDD.PURPOSE.INTERSECTED
                    for p in polygons:
                        elems += p
        self.elementals = elems
        return self

    @property

    def merge(self):
        # elems = ElementalList()
        # if len(self.elementals) > 1:
        #     for i, e1 in enumerate(self.elementals):
        #         for j, e2 in enumerate(self.elementals):
        #             if i != j:
        #                 polygons = e1 | e2
        #                 elems += polygons
        # else:
        #     elems = self.elementals
        # self.elementals = elems
        # return self

        elems = ElementalList()
        if len(self.elementals) > 1:
            points = []
            for e in self.elementals:
                shape = e.shape.transform(e.transformation)
                points.append(shape.points)
                # points.append(e.points)
            # merged_points = clipping.union_points(points)
            merged_points = clipping.boolean(subj=points, clip_type='or')
            for uid, pts in enumerate(merged_points):
                elems += Polygon(shape=pts, layer=self.layer)
        else:
            elems = self.elementals
        self.elementals = elems
        return self


def Rectangle(layer, p1=(0,0), p2=(2,2), center=(0,0), alias=None):
    """ Creates a rectangular shape that can be used in 
    GDSII format as a polygon object.

    Example
    -------
    >>> p = spira.Rectangle(p1=(0,0), p2=(10,0), layer=RDD.PLAYER.M6)
    >>> [SPiRA: Rectangle] ()
    """
    shape = shapes.RectangleShape(p1=p1, p2=p2)
    return Polygon(alias=alias, shape=shape, layer=layer)


def Box(layer, width=1, height=1, center=(0,0), alias=None, enable_edges=False):
    """ Creates a box shape that can be used in 
    GDSII format as a polygon object.

    Example
    -------
    >>> p = spira.Box(p1=(0,0), p2=(10,0), layer=RDD.PLAYER.M6)
    >>> [SPiRA: Rectangle] ()
    """
    shape = shapes.BoxShape(width=width, height=height, center=center)
    return Polygon(alias=alias, shape=shape, layer=layer, enable_edges=enable_edges)


def Circle(layer, box_size=(1,1), angle_step=1, center=(0,0), alias=None):
    """ Creates a circle shape that can be used in 
    GDSII format as a polygon object.

    Example
    -------
    >>> p = spira.Circle(p1=(0,0), p2=(10,0), layer=RDD.PLAYER.M6)
    >>> [SPiRA: Rectangle] ()
    """
    shape = shapes.CircleShape(box_size=box_size, angle_step=angle_step)
    return Polygon(alias=alias, shape=shape, layer=layer)


def Convex(layer, radius=1.0, num_sides=6, center=(0,0), alias=None):
    """ Creates a circle shape that can be used in 
    GDSII format as a polygon object.

    Example
    -------
    >>> p = spira.Circle(p1=(0,0), p2=(10,0), layer=RDD.PLAYER.M6)
    >>> [SPiRA: Rectangle] ()
    """
    shape = shapes.ConvexShape(radius=radius, num_sides=num_sides)
    return Polygon(alias=alias, shape=shape, layer=layer)


def Cross(layer, box_size=20, thickness=5, center=(0,0), alias=None):
    """ Creates a circle shape that can be used in 
    GDSII format as a polygon object.

    Example
    -------
    >>> p = spira.Circle(p1=(0,0), p2=(10,0), layer=RDD.PLAYER.M6)
    >>> [SPiRA: Rectangle] ()
    """
    shape = shapes.CrossShape(box_size=box_size, thickness=thickness)
    return Polygon(alias=alias, shape=shape, layer=layer)


def Wedge(layer, begin_coord=(0,0), end_coord=(10,0), begin_width=3, end_width=1, center=(0,0), alias=None):
    """ Creates a circle shape that can be used in 
    GDSII format as a polygon object.

    Example
    -------
    >>> p = spira.Circle(p1=(0,0), p2=(10,0), layer=RDD.PLAYER.M6)
    >>> [SPiRA: Rectangle] ()
    """
    shape = shapes.WedgeShape(
        begin_coord=begin_coord, 
        end_coord=end_coord, 
        begin_width=begin_width, 
        end_width=end_width
    )
    return Polygon(alias=alias, shape=shape, layer=layer)


def Parabolic(layer, begin_coord=(0,0), end_coord=(10,0), begin_width=3, end_width=1, center=(0,0), alias=None):
    """ Creates a circle shape that can be used in 
    GDSII format as a polygon object.

    Example
    -------
    >>> p = spira.Circle(p1=(0,0), p2=(10,0), layer=RDD.PLAYER.M6)
    >>> [SPiRA: Rectangle] ()
    """
    shape = shapes.ParabolicShape(
        begin_coord=begin_coord, 
        end_coord=end_coord, 
        begin_width=begin_width, 
        end_width=end_width
    )
    return Polygon(alias=alias, shape=shape, layer=layer)

