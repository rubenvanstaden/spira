from spira.core.transformable import Transformable
from spira.core.parameters.initializer import ParameterInitializer
from spira.core.parameters.initializer import MetaInitializer
from spira.core.parameters.descriptor import FunctionParameter
from spira.yevon.process.gdsii_layer import LayerParameter
from spira.yevon.geometry.shapes import ShapeParameter
from spira.core.parameters.variables import *
from spira.yevon.geometry.coord import Coord
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


class MetaElement(MetaInitializer):
    """  """

    def __call__(cls, *params, **keyword_params):
        kwargs = cls.__map_parameters__(*params, **keyword_params)
        cls = super().__call__(**kwargs)
        cls.__keywords__ = kwargs
        return cls


class __Element__(Transformable, ParameterInitializer, metaclass=MetaElement):
    """ Base class for all transformable elements. """

    def get_node_id(self):
        if self.__id__:
            return self.__id__
        else:
            return self.__str__()

    def set_node_id(self, value):
        self.__id__ = value

    node_id = FunctionParameter(get_node_id, set_node_id)

    def __init__(self, transformation=None, **kwargs):
        super().__init__(transformation=transformation, **kwargs)

    def __add__(self, other):
        from spira.yevon.gdsii.elem_list import ElementList
        if isinstance(other, list):
            l = ElementList([self])
            l.extend(other)
            return l
        elif isinstance(other, __Element__):
            return ElementList([self, other])
        else:
            raise TypeError("Wrong type of argument for addition in __Element__: " + str(type(other)))

    def __radd__(self, other):
        from spira.yevon.gdsii.elem_list import ElementList
        if isinstance(other, list):
            l = ElementList(other)
            l.append(self)
            return l
        elif isinstance(other, __Element__):
            return ElementList([other, self])
        else:
            raise TypeError("Wrong type of argument for addition in __Element__: " + str(type(other)))

    def flatten(self):
        return [self]

    def dependencies(self):
        return None


class __LayerElement__(__Element__):
    """  """

    layer = LayerParameter()

    def __init__(self, layer=0, transformation=None, **kwargs):
        super().__init__(layer=layer, transformation=transformation, **kwargs)

    def __eq__(self, other):
        if other == None:
            return False
        if not isinstance(other, __LayerElement__):
            return False
        if other.layer.key != self.layer.key:
            return False                
        if self.shape.transform_copy(self.transformation) != other.shape.transform_copy(other.transformation):
            return False
        return True

    def __ne__(self,other):
        return not self.__eq__(other)      


class __ShapeElement__(__LayerElement__):
    """ Base class for an edge element. """

    shape = ShapeParameter()

    @property
    def points(self):
        return self.shape.points

    @property
    def area(self):
        import gdspy 
        return gdspy.Polygon(self.shape.points).area()

    @property
    def count(self):
        return np.size(self.shape.points, 0)

    @property
    def bbox_info(self):
        return self.shape.bbox_info.transform_copy(self.transformation)

    @property
    def center(self):
        return self.bbox_info.center

    @center.setter
    def center(self, destination):
        self.move(midpoint=self.center, destination=destination)

    def id_string(self):
        return '{} - hash {}'.format(self.short_string(), self.shape.hash_string)

    def is_empty(self):
        """ Returns `False` is the polygon shape has no points. """
        return self.shape.is_empty()

    def encloses(self, point):
        """ Returns `True` if the polygon encloses the point. """
        from spira.yevon.utils import clipping
        shape = self.shape.transform_copy(self.transformation)
        return clipping.encloses(coord=point, points=shape.points)

    def expand_transform(self):
        """ Expand the transform by applying it to the shape. """
        from spira.core.transforms.identity import IdentityTransform
        if not self.transformation.is_identity():
            self.shape = self.shape.transform_copy(self.transformation)
            self.transformation = IdentityTransform()
        return self

    def flatten(self, level=-1, name_tree=[]):
        """ Flatten the polygon without creating a copy. """
        return self.expand_transform()

    def stretch(self, factor=(1,1), center=(0,0)):
        """ Stretches the polygon by a factor. """
        T = spira.Stretch(stretch_factor=factor, stretch_center=center)
        return T.apply(self)

    def stretch_copy(self, factor=(1,1), center=(0,0)):
        """ Stretches a copy of the polygon by a factor. """
        T = spira.Stretch(stretch_factor=factor, stretch_center=center)
        return T.apply_copy(self)

    def stretch_port(self, port, destination):
        """ The element by moving the subject port, without 
        distorting the entire element. Note: The opposite 
        port position is used as the stretching center. """
        opposite_port = bbox_info.bbox_info_opposite_boundary_port(self, port)
        T = stretching.stretch_element_by_port(self, opposite_port, port, destination)
        T.apply(self)
        return self

    def move(self, midpoint=(0,0), destination=None, axis=None):
        """ Moves the polygon from `midpoint` to a `destination`. """
        from spira.yevon.geometry.ports import Port

        if destination is None:
            destination = midpoint
            midpoint = Coord(0,0)

        if isinstance(midpoint, Coord):
            m = midpoint
        elif np.array(midpoint).size == 2:
            m = Coord(midpoint)
        # elif issubclass(type(midpoint), __Port__):
        elif isinstance(midpoint, Port):
            m = midpoint.midpoint
        else:
            raise ValueError('Midpoint error')

        # if issubclass(type(destination), __Port__):
        if isinstance(destination, Port):
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

