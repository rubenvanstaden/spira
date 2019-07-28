import gdspy
from spira.yevon.io.output import OutputBasic
from spira.core.transforms import Translation
from spira.core.transformation import CompoundTransform
from spira.yevon.geometry.coord import Coord
# from spira.yevon.io.collector import GdspyCollector
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


class OutputGdsii(OutputBasic):
    """ Writes GDS output to a stream """

    # name_filter = RestrictedProperty(
    #     default=TECH.GDSII.NAME_FILTER,
    #     restriction=RestrictType(Filter),
    #     doc="filter class which is applied to all names")

    def __init__(self, file_name=None, **kwargs):
        if file_name is None:
            raise ValueError('No GDSII file name specified.')
        super().__init__(file_name=file_name, **kwargs)
        self.file_name = file_name
        # if 'flatten_structure_container' in kwargs:
        #     self.flatten_structure_container = kwargs.get('flatten_structure_container')
        # elif hasattr(TECH.GDSII, 'FLATTEN_STRUCTURE_CONTAINER'):
        #     self.flatten_structure_container = TECH.GDSII.FLATTEN_STRUCTURE_CONTAINER
        # else:
        #     self.flatten_structure_container = False
        self._collected_ref_cells = set()

    # def __init_collector__(self):
    #     gdspy_library = gdspy.GdsLibrary(name=self.file_name)
    #     self.collector = GdspyCollector(library=gdspy_library)

    def write(self, item):
        self.collect(item)
        print(self.collector.output())
        writer = gdspy.GdsWriter('{}.gds'.format(self.file_name), unit=1.0e-6, precision=1.0e-12)
        for cell in self.collector.output():
            writer.write_cell(cell)
            del cell
        writer.close()

    def viewer(self):
        library = gdspy.GdsLibrary(name=self.file_name)
        for c in self.collector.output():
            library.add(c)
        gdspy.LayoutViewer(library=library)

    def collect_Library(self, library, **kwargs):
        referenced_cells = self.library.referenced_cells()
        self.collect(referenced_cells, **kwargs)
        collected_referenced_cells = []
        # print(referenced_cells)
        while len(self._collected_ref_cells) > 0:
            for rs in referenced_cells:
                # print(rs)
                # print(self._collected_ref_cells)
                # print(type(self._collected_ref_cells))
                if rs in self._collected_ref_cells:
                    self.collect(rs, **kwargs)
                    collected_referenced_cells.append(rs)
            for crs in collected_referenced_cells:
                referenced_cells.remove(crs)
            self._collected_ref_cells.clear()
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

        e = gdspy.CellReference(
            ref_cell=self._current_cell,
            origin=origin,
            rotation=rotation,
            magnification=magnification,
            x_reflection=reflection)

        self._collected_ref_cells.add(item.reference)
        return self

    def collect_label(self, text, position, rotation):
        layer = self.map_layer(item.layer)
        if layer is None: return self
        e = gdspy.Label(text=text, position=position, rotation=orientation, layer=layer.number, texttype=layer.datatype)
        self._current_cell.add(e)
        return self

    def collect_polygon(self, points, layer):
        layer = self.map_layer(layer)
        if layer is None: return self
        e = gdspy.Polygon(points=points, layer=layer.number, datatype=layer.datatype)
        self._current_cell.add(e)
        return self

