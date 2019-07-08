import numpy as np
from spira.yevon.geometry.coord import Coord
from spira.core.transformable import Transformable
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = [
    'BoundaryInfo',
    'BoundaryInfoParameter',
    'bbox_info_from_point_list',
    'bbox_info_from_numpy_array',
    'bbox_info_from_coord',
    'bbox_info_opposite_boundary_port',
    'bbox_info_cell'
]


class BoundaryInfo(Transformable):
    """ Object which describes the bounding box of a shape, element or structure. """

    def __init__(self, west=None, east=None, north=None, south=None):
        self.__west = west
        self.__east = east
        self.__north = north
        self.__south = south

    def __is_initialized__(self):
        """ Checks whether the internal data makes sense. """
        return not ((self.__west is None) or
                    (self.__east is None) or
                    (self.__north is None) or
                    (self.__south is None))

    def __contains__(self, other):
        """ Checks whether point(s) is in bounding box. """
        return self.encloses(other, inclusive=True)

    def __add__(self, other):
        """ Gives the sizeinfo of the box enclosing the union of both boxes """
        if self.__is_initialized__() and other.__is_initialized__():
            west = min(self.__west, other.__west)
            east = max(self.__east, other.__east)
            south = min(self.__south, other.__south)
            north = max(self.__north, other.__north)
        elif other.__is_initialized__():
            west = other.__west
            east = other.__east
            south = other.__south
            north = other.__north
        elif self.__is_initialized__():
            west = self.__west
            east = self.__east
            south = self.__south
            north = self.__north
        else:        
            west, east, north, south = None, None, None, None
        return BoundaryInfo(west, east, north, south)

    def __iadd__(self, other):
        """ Expands the sizeinfo to include the other box """
        if self.__is_initialized__() and other.__is_initialized__():
            self.__west = min(self.__west, other.__west)
            self.__east = max(self.__east, other.__east)
            self.__south = min(self.__south, other.__south)
            self.__north = max(self.__north, other.__north)
        elif other.__is_initialized__():
            self.__west = other.__west
            self.__east = other.__east
            self.__south = other.__south
            self.__north = other.__north
        return self

    def __eq__(self, other):
        return (self.west == other.west and self.east == other.east and self.north == other.north and self.south == other.south and self.center == other.center and self.size == other.size and self.width == other.width and self.height == other.height )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "[SPiRA: Bbox Info] (west: {}, east: {}, south: {}, north: {})".format(self.west, self.east, self.south, self.north)

    def __str__(self):
        return self.__repr__()

    def get_west(self):
        return self.__west
    def set_west(self, value):
        self.__west = value
        if not self.__east is None:
            self.__east = max(self.__west, self.__east)
    west = property(get_west, set_west)
    """ westmost x-coordinate """

    def get_east(self): 
        return self.__east
    def set_east(self, value):
        self.__east = value
        if not self.__west is None:
            self.__west = min(self.__west, self.__east)
    east = property(get_east, set_east)
    """ eastmost x coordinate """

    def get_north(self): 
        return self.__north
    def set_north(self, value):
        self.__north = value
        if not self.__south is None:
            self.__south = min(self.__north, self.__south)
    north = property(get_north, set_north)
    """ highest y coordinate """

    def get_south(self): 
        return self.__south
    def set_south(self, value):
        self.__south = value
        if not self.__north is None:
            self.__north = max(self.__north, self.__south)
    south = property(get_south, set_south)
    """ lowest y coordinate """

    def get_center(self):
        if not self.__is_initialized__(): 
            return None
        return Coord(0.5 * (self.__west + self.__east), 0.5 * (self.__south + self.__north))
    def set_center(self, value):
        # change center but keep height and width
        if self.__is_initialized__():
            wo2 = 0.5 * (self.__east - self.__west)
            self.__west = value[0] - wo2
            self.__east = value[0] + wo2
            ho2 = 0.5 * (self.__north - self.__south)
            self.__north = value[1] + ho2
            self.__south = value[1] - ho2
        else:
            self.__west = value[0]
            self.__east = value[0]
            self.__north = value[1]
            self.__south = value[1]
    center = property(get_center, set_center)
    """ center coordinate """

    def get_size(self):
        if not self.__is_initialized__():
            return (0.0, 0.0)
        return Coord(self.__east - self.__west, self.__north - self.__south)
    def set_size(self, value):
        # change width and height but keep the center
        if self.__is_initialized__():
            cw = 0.5 * (value[0] - self.__east + self.__west)
            self.__west -= cw
            self.__east += cw
            ch = 0.5 * (value[1] - self.__north + self.__south)
            self.__south -= ch
            self.__north += ch
    size = property(get_size, set_size)
    """ size: (width, height)"""

    def get_width(self):
        if not self.__is_initialized__():
            return 0.0
        return self.__east - self.__west
    def set_width(self, value):
        # change width but keep center
        if self.__is_initialized__():
            cw = 0.5 * (value - self.__east + self.__west)
            self.__west -= cw
            self.__east += cw
    width = property(get_width, set_width)
    """ width """

    def get_height(self):
        if not self.__is_initialized__(): 
            return 0.0
        return self.__north - self.__south
    def set_height(self, value):
        # change height but keep center
        if self.__is_initialized__():
            ch = 0.5 * (value - self.__north + self.__south)
            self.__south -= ch
            self.__north += ch
    height = property(get_height, set_height)
    """ height """

    @property
    def north_west(self):
        return (self.__west, self.__north)

    @property
    def north_east(self):
        return (self.__east, self.__north)

    @property
    def south_west(self):
        return (self.__west, self.__south)

    @property
    def south_east(self):
        return (self.__east, self.__south)

    def get_border_on_one_side(self, side):
        from spira.yevon.constants import NORTH, SOUTH, EAST, WEST
        if side == NORTH: 
            return self.north
        elif side == SOUTH:
            return self.south
        elif side == EAST:
            return self.east
        elif side == WEST:
            return self.west
        else:
            raise AttributeError("side in size_info.get_border_on_one_side() should be EAST, WEST NORTH or SOUTH")

    @property
    def box(self):
        if not self.__is_initialized__(): return None
        from spira.yevon.geometry import shapes
        return shapes.Shape([(self.__west, self.__south), (self.__east, self.__north)])

    def __bounding_box_array__(self):
        """ Numpy array with the corner points of the enclosing rectangle. """
        if not self.__is_initialized__(): return None
        return np.array([(self.__west, self.__south),
                         (self.__east, self.__south),
                         (self.__east, self.__north),
                         (self.__west, self.__north)])

    def bounding_box(self, margin=0):
        from spira.yevon.geometry import shapes
        if not self.__is_initialized__(): return None
        return shapes.Shape([(self.__west-margin, self.__south-margin),
                             (self.__east+margin, self.__south-margin),
                             (self.__east+margin, self.__north+margin),
                             (self.__west-margin, self.__north+margin)])

    @property
    def area(self):
        return self.width * self.height

    def id_string(self):
        return self.__repr__()

    @property
    def ports(self):
        return shape_edge_ports(self.bounding_box(), RDD.PLAYER.BBOX, self.id_string())

    def snap_to_grid(self, grids_per_unit=None):
        """ Snaps the boundary box to a given grid or the current grid. """
        from spira import settings
        if not self.__is_initialized__(): return self
        if grids_per_unit is None: grids_per_unit = settings.get_grids_per_unit()
        self.__west = settings.snap_value(self.__west, grids_per_unit)
        self.__east = settings.snap_value(self.__east, grids_per_unit)
        self.__north = settings.snap_value(self.__north, grids_per_unit)
        self.__south = settings.snap_value(self.__south, grids_per_unit)
        return self

    def move(self, coordinate):
        if self.__is_initialized__():
            self.west += coordinate[0]
            self.east += coordinate[0]
            self.north += coordinate[1]
            self.south += coordinate[1]
        else:
            self.west, self.east, self.north, self.south = None, None, None, None
        return self

    def movecopy(self, coordinate):
        if self.__is_initialized__():
            west = self.__west + coordinate[0]
            east = self.__east + coordinate[0]
            north = self.__north + coordinate[1]
            south = self.__south + coordinate[1]
        else:
            west, east, north, south = None, None, None, None
        return BoundaryInfo(west, east, north, south)

    def transform(self, transformation):
        if self.__is_initialized__():
            BB = transformation.apply_to_array(self.__bounding_box_array__())
            LB = np.min(BB, 0)
            TR = np.max(BB, 0)
            self.__init__(LB[0], TR[0], TR[1], LB[1])
        return self

    def transform_copy(self, transformation):
        if self.__is_initialized__():
            return bbox_info_from_numpy_array(transformation.apply_to_array(self.__bounding_box_array__()))
        else:
            return BoundaryInfo()

    def grow_absolute(self, growth):
        self.__west = self.__west - growth
        self.__east = self.__east + growth
        self.__north = self.__north + growth
        self.__south = self.__south - growth


def bbox_info_from_point_list(point_list):
    """ Generate bounding box info from a point list. """
    if len(point_list) == 0:
        return BoundaryInfo()
    x = [c[0] for c in point_list]
    y = [c[1] for c in point_list]
    return BoundaryInfo(min(x), max(x), max(y), min(y))


def bbox_info_from_numpy_array(points):
    """ Generate bounding box info from a np array. """
    if len(points) == 0:
        return BoundaryInfo()
    LB = np.min(points, 0)
    TR = np.max(points, 0)
    return BoundaryInfo(LB[0], TR[0], TR[1], LB[1])


def bbox_info_from_coord(coord):
    """ Generate bounding box info from a single coordinate """
    return BoundaryInfo(coord[0], coord[0], coord[1], coord[1])


def bbox_info(shape):
    """ Generate bounding box info from a shape-like object """
    from spira.yevon.geometry import shapes
    if isinstance(shape, shapes.Shape):
        return shape.size_info()
    elif isinstance(shape, np.ndarray):
        return bbox_info_from_numpy_array(shape)
    elif isinstance(shape, list):
        return bbox_info_from_pointlist(shape)
    elif isinstance(shape, Coord):
        return bbox_info_from_coord(shape)
    else:
        raise TypeError("Invalid type for size_info(): " + str(type(shape)))


def bbox_info_opposite_boundary_port(elem, subj_port):
    """ 
    Get the bounding box port that has the 
    opposite direction of the subject port. 
    """
    from spira.yevon.utils import geometry as geom
    from spira.yevon.geometry.shapes import shape_edge_ports
    bbox_shape = elem.bbox_info.bounding_box()
    for p in shape_edge_ports(shape=bbox_shape, layer=RDD.PLAYER.BBOX):
        if geom.angle_diff(p.orientation, subj_port.orientation) == 180:
            return p
    return None


def bbox_info_cell(elem):
    from spira.yevon.gdsii.cell import Cell
    from spira.yevon.gdsii.polygon import Polygon
    bbox_shape = elem.bbox_info.bounding_box()
    bbox_ply = Polygon(shape=bbox_shape)
    D = Cell(name='BBoxCell')
    D += bbox_ply
    return D


from spira.core.parameters.restrictions import RestrictNothing
def BoundaryInfoParameter(restriction=RestrictNothing(), **kwargs):
    R = RestrictType(BoundaryInfo) & restriction
    return RestrictedProperty(internal_member_name=internal_member_name, restriction=R, **kwargs)


EMPTY_BOUNDARY_INFO = BoundaryInfo(west=0.0, east=0.0, south=0.0, north=0.0)





