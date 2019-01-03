import os
import gdspy
import spira

from spira import settings
from spira import log as LOG
from .graph_output import DrawGraphAbstract


glib = gdspy.GdsLibrary(name='s2g')


class DrawLayoutAbstract(object):
    """ Class that generates output formates
    for a layout or library containing layouts. """

    def _wrapper(self, c, c2dmap):
        for e in c.elementals.flat_elems():
            G = c2dmap[c]
            if isinstance(e, spira.SRef):
                G.add(gdspy.CellReference(
                    ref_cell=c2dmap[e.ref],
                    midpoint=e.midpoint,
                    rotation=e.rotation,
                    magnification=e.magnification,
                    x_reflection=e.reflection))

    def _construct_gdspy_tree(self):
        d = self.dependencies()
        c2dmap = {}
        for c in d:
            G = c.commit_to_gdspy()
            c2dmap.update({c:G})
#             for p in c.get_ports():
#                 p.commit_to_gdspy(cell=c2dmap[c])
        for c in d:
            self._wrapper(c, c2dmap)
            # cell = c2dmap[c]
            if c.name in glib.cell_dict.keys():
                pass
                # glib.cell_dict[c.name] = cell
                # self.add(self.cell_dict[c.name])
            else:
                glib.add(c2dmap[c])
            # glib.add(c2dmap[c])
        for p in self.get_ports():
            p.commit_to_gdspy(cell=c2dmap[self])
        return c2dmap[self]

    def output(self, name=None, path='current'):
        """ Plot the cell or library using gdspy viewer. """

        global glib

        if isinstance(self, spira.Library):
            # library = settings.get_library()
            # library += self
            # library.to_gdspy
            glib = settings.get_library()
            glib += self
            glib.to_gdspy
        elif isinstance(self, spira.Cell):
            self._construct_gdspy_tree()
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










