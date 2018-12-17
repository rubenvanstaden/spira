import os
import gdspy
import spira

from spira import log as LOG

from spira.gdsii.utils import scale_coord_down as scd

from spira.param.field.typed_graph import EdgeCapacitor
from spira.param.field.typed_graph import EdgeInductor

import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.offline as offline

from spira import settings
from .graph_output import DrawGraphAbstract


class DrawLayoutAbstract(object):
    import spira

    def output(self, name=None, path='current'):
        if name is None:
            raise ValueError('GDS file not named.')

        library = settings.get_library()
        library += self
        library.to_gdspy

        # writer = gdspy.GdsWriter('out-file.gds', unit=1.0e-6, precision=1.0e-9)
        # cell = self.gdspycell
        # writer.write_cell(cell)
        # del cell
        # writer.close()

        # gdspy.write_gds(outfile=write_path, name=name, unit=1.0e-6)
        # gdspy.LayoutViewer(library=library, cells=cell)
        gdspy.LayoutViewer(library=library)


class OutputMixin(DrawLayoutAbstract, DrawGraphAbstract):
    pass
