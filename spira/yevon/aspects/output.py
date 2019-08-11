from spira.yevon.aspects.base import __Aspects__
from spira.log import SPIRA_LOG as LOG
from spira.yevon import filters
from copy import deepcopy
from spira.yevon.gdsii.library import Library
from spira.yevon.io.output_gdsii import OutputGdsii
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


class OutputGdsiiAspect(__Aspects__):
    """  """

    def gdsii_view(self, unit=RDD.GDSII.UNIT, grid=RDD.GDSII.GRID, layer_map=None):
        library = Library(name=self.name, unit=unit, grid=grid)

        D = deepcopy(self)

        F = RDD.FILTERS.OUTPUT.PORTS

        library += F(D)

        if layer_map is None:
            layer_map = RDD.GDSII.EXPORT_LAYER_MAP

        output = OutputGdsii(file_name='', layer_map=layer_map)
        output.viewer(library)

    def gdsii_output(self, file_name=None, unit=RDD.GDSII.UNIT, grid=RDD.GDSII.GRID, layer_map=None):
        library = Library(name=self.name, unit=unit, grid=grid)
        
        D = deepcopy(self)

        F = RDD.FILTERS.OUTPUT.PORTS

        library += F(D)
        
        if layer_map is None:
            layer_map = RDD.GDSII.EXPORT_LAYER_MAP

        output = OutputGdsii(file_name=file_name, layer_map=layer_map)
        output.write(library)

        LOG.debug("Finished writing structure to GDS2.")


class OutputPlotlyNetlist(__Aspects__):

    def netlist_view(self, net=None):
        from spira.yevon.io.output_netlist import PlotlyGraph
        output = PlotlyGraph()
        if net is None:
            output._plotly_netlist(G=self.netlist.g, graphname=self.name)
        else:
            output._plotly_netlist(G=net.g, graphname=self.name)


class OutputBokehNetlist(__Aspects__):
    pass
    