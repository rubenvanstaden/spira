import gdspy
from spira.yevon.io.output import OutputBasic
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = ['OutputGdsii']


class OutputGdsii(OutputBasic):
    """ Writes GDS output to a stream """

    def __init__(self, file_name=None, **kwargs):
        if file_name is None:
            raise ValueError('No GDSII file name specified.')
        super().__init__(file_name=file_name, **kwargs)

    def write(self, item):
        self.collect(item)
        writer = gdspy.GdsWriter('{}.gds'.format(self.file_name), unit=1.0e-6, precision=1.0e-12)
        for cell in self.collector.values():
            writer.write_cell(cell)
            del cell
        writer.close()

    def viewer(self, item):
        self.collect(item)
        library = gdspy.GdsLibrary(name=self.file_name)
        for c in self.collector.values():
            library.add(c)
        gdspy.LayoutViewer(library=library)

    def collect_reference(self, ref_cell, origin, rotation, reflection, magnification):
        e = gdspy.CellReference(
            ref_cell=ref_cell,
            origin=origin,
            rotation=rotation,
            magnification=magnification,
            x_reflection=reflection
        )
        self.collector[self._current_cell].add(e)
        return self

    def collect_label(self, text, position, rotation, layer):
        layer = self.map_layer(layer)
        if layer is None: return self
        e = gdspy.Label(
            text=text,
            position=position,
            rotation=rotation,
            layer=layer.number,
            texttype=layer.datatype
        )
        self.collector[self._current_cell].add(e)
        return self

    def collect_polygon(self, points, layer):
        layer = self.map_layer(layer)
        if layer is None: return self
        e = gdspy.Polygon(
            points=points,
            layer=layer.number,
            datatype=layer.datatype
        )
        self.collector[self._current_cell].add(e)
        return self

