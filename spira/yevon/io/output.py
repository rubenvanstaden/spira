import gdspy

from spira import log as LOG
from spira.core.parameters.initializer import ParameterInitializer
from spira.core.parameters.descriptor import RestrictedParameter
from spira.core.parameters.restrictions import RestrictType
from spira.core.parameters.variables import StringParameter
from spira.core.transforms import Translation
from spira.core.transformation import CompoundTransform
from spira.yevon.geometry.coord import Coord
from spira.yevon.filters import Filter
from spira.yevon.io.collector import ListCollector
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


class __OutputBasic__(ParameterInitializer):
    """  """

    file_name = StringParameter()

    output_filter = RestrictedParameter(
        default=Filter(),
        # restriction=RestrictType(Filter),
        doc="filter class which is applied to all output items")

    def __init__(self, file_name=None, **kwargs):
        super().__init__(file_name=file_name, **kwargs)
        self.__init_collector__()
        self.__collect_method_dict__ = {}

    def __init_collector__(self):
        self.collector = {}

    def write(self, item):
        raise NotImplementedError('Must provide implementation in subclass.')

    def collect(self, item, **kwargs):
        self.do_collect(item, **kwargs)
        return self

    def do_collect(self, item, **kwargs):
        """ Collects each element using the Visitor Design Pattern. """

        import inspect

        items = self.output_filter(item)
        if len(items) == 1:
            item = items[0]
        else:
            item = items

        T = type(item)
        if inspect.isclass(T):
            collect_method = self.__collect_method_dict__.get(T, None)
            if collect_method is None:
                for cls in inspect.getmro(T):
                    collect_method_name = 'collect_{}'.format(cls.__name__)
                    if hasattr(self, collect_method_name):
                        collect_method = getattr(self, collect_method_name)
                        self.__collect_method_dict__[T] = collect_method
                        break
            if collect_method is None:
                LOG.warn("No collect method found for object of type %s" %T)
            else:
                collect_method(item, **kwargs)

        return self


class OutputBasic(__OutputBasic__):
    """  """

    layer_map = RestrictedParameter(default=RDD.GDSII.EXPORT_LAYER_MAP)

    def __init__(self, file_name=None, **kwargs):
        super().__init__(file_name=file_name, **kwargs)
        self.library = None
        self._current_cell = None
        self.__collect_method_dict__ = {}

    def set_current_cell(self, item):
        self._current_cell = item

    def do_collect(self, item, **kwargs):
        from spira.yevon.gdsii.library import Library
        if isinstance(item, Library):
            self.library = item
            self.grids_per_unit = self.library.grids_per_unit 
            self.unit = self.library.unit 
        if self.library == None:
            self.library = get_current_library()
        super().do_collect(item, **kwargs)
        return self

    def collect_list(self, item, **kwargs):
        for i in item:
            self.collect(i, **kwargs)
        return self

    def collect_Library(self, library, usecache = False, **kwargs):
        referenced_cells = self.library.referenced_cells()
        for rc in referenced_cells:
            c = gdspy.Cell(rc.name, exclude_from_current=True)
            self.collector.update({rc: c})
        self.collect(referenced_cells, **kwargs)
        return self

    def collect_CellList(self, item, **kwargs):
        for s in item:
            self.collect(s, **kwargs)
        return self

    def collect_Cell(self, item, **kwargs):
        self.set_current_cell(item)
        self.collect(item.elements, **kwargs)
        return self

    def collect_ElementList(self, item, additional_transform=None, **kwargs):
        for s in item:
            self.collect(s, additional_transform=additional_transform, **kwargs)
        return self

    def collect_Group(self, item, additional_transform=None, **kwargs):
        T = item.transformation + additional_transform
        self.collect(item.elements, additional_transform=T, **kwargs)
        return self

    def collect_SRef(self, item, additional_transform=None):
        T = item.transformation + Translation(item.midpoint)
        origin = Coord(0,0).transform(T).to_numpy_array()

        rotation = 0
        reflection = False
        magnification = 1.0

        if isinstance(T, CompoundTransform):
            for t in T.__subtransforms__:
                if isinstance(t, GenericTransform):
                    rotation = t.rotation
                    reflection = t.reflection
                    magnification = t.magnification
        else:
            rotation = T.rotation
            reflection = T.reflection
            magnification = T.magnification

        ref_cell = self.collector[item.reference]
        self.collect_reference(ref_cell, origin, rotation, reflection, magnification)

        return self

    def collect_Polygon(self, item, additional_transform=None, **kwargs):
    # def collect___ShapeElement__(self, item, additional_transform=None, **kwargs):
        T = item.transformation + additional_transform
        shape = item.shape.transform_copy(T)
        shape.snap_to_grid(self.grids_per_unit)
        coordinates = shape
        if len(shape) < 3:
            LOG.warning("Polygon cannot have less than 4 points.")
            return self
        if not (coordinates[0] == coordinates[-1]):
            coordinates.append(coordinates[0])
        self.collect_polygon(points=coordinates.points, layer=item.layer)
        return self

    def collect_Label(self, item, additional_transform=None):
        T = item.transformation + additional_transform
        item.position = T.apply_to_coord(item.position)
        item.orientation = T.apply_to_angle(item.orientation)
        position = item.position.to_numpy_array()
        self.collect_label(text=item.text, position=position, rotation=item.orientation, layer=item.layer)
        return self

    def map_layer(self, layer):
        from spira.yevon.process.gdsii_layer import Layer
        L = self.layer_map.get(layer, None)
        if isinstance(L, Layer):
            return L
        elif L is None:
            return L
        else:
            return Layer(number = L)




