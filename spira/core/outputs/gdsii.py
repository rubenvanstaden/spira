import os
import gdspy
import spira

from spira import settings
from spira import log as LOG
from spira.core.mixin import MixinBowl
from spira.core.outputs.base import Outputs


class GdsiiLayout(object):
    """ Class that generates output formates
    for a layout or library containing layouts. """

    def output(self, name=None, cell=None):
        from spira.yevon.gdsii.cell import __Cell__

        glib = gdspy.GdsLibrary(name=self.name)

        if isinstance(self, spira.Library):
            glib = settings.get_library()
            glib += self
            glib.to_gdspy
        elif issubclass(type(self), __Cell__):
            self.construct_gdspy_tree(glib)

        if cell is None:
            gdspy.LayoutViewer(library=glib)
        else:
            gdspy.LayoutViewer(library=glib, cells=cell)

        # gdspy.LayoutViewer(library=glib, cells='Circuit_AiST_CELL_1')
        # gdspy.LayoutViewer(library=glib, cells='LayoutConstructor_AiST_CELL_1')

    # FIXME!
    def writer(self, name=None, file_type='gdsii'):
        if name is None:
            file_name = '{}.gds'.format(self.name)
        else:
            file_name = '{}.gds'.format(name)
        glib = gdspy.GdsLibrary(name=self.name)
        writer = gdspy.GdsWriter(file_name, unit=1.0e-6, precision=1.0e-6)
        cell = self.construct_gdspy_tree(glib)
        writer.write_cell(cell)
        del cell
        writer.close()


Outputs.mixin(GdsiiLayout)



