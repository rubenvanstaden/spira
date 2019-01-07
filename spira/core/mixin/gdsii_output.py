import os
import gdspy
import spira

from spira import settings
from spira import log as LOG
from .graph_output import DrawGraphAbstract


class DrawLayoutAbstract(object):
    """ Class that generates output formates
    for a layout or library containing layouts. """

    def output(self, name=None, path='current'):
        """ Plot the cell or library using gdspy viewer. """

        glib = gdspy.GdsLibrary(name=self.name)

        if isinstance(self, spira.Library):
            glib = settings.get_library()
            glib += self
            glib.to_gdspy
        elif isinstance(self, spira.Cell):
            self.construct_gdspy_tree(glib)
        gdspy.LayoutViewer(library=glib)

    # def writer(self, name=None, file_type='gdsii'):
        # """ Write layout to gdsii file. """
        # writer = gdspy.GdsWriter('out-file.gds', unit=1.0e-6, precision=1.0e-9)
        # cell = self.gdspycell
        # writer.write_cell(cell)
        # del cell
        # writer.close()

        # gdspy.write_gds(outfile=write_path, name=name, unit=1.0e-6)
        # gdspy.LayoutViewer(library=library, cells=cell)


class OutputMixin(DrawLayoutAbstract, DrawGraphAbstract):
    pass










