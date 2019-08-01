from spira.yevon.aspects.base import __Aspects__
from spira.log import SPIRA_LOG as LOG
from spira.yevon import filters
from spira.yevon.gdsii.library import Library
from spira.yevon.io.output_gdsii import OutputGdsii
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


class OutputGdsiiAspect(__Aspects__):
    """  """

    def gdsii_view(self, unit=RDD.GDSII.UNIT, grid=RDD.GDSII.GRID, layer_map=None):
        my_lib = Library(name=self.name, unit=unit, grid=grid)
        # F = filters.ToggledCompositeFilter()

        # f1 = filters.PortCellFilter()
        # f2 = filters.PortPolygonFilter()
        # F = f1 + f2

        # F = filters.PortCellFilter(name='cell_ports')
        F = filters.PortPolygonFilter(name='polygon_ports')
        
        # D = F(self)
        # print(D.elements)
        # my_lib += D
        # my_lib += self

        my_lib += F(self)

        if layer_map is None:
            layer_map = RDD.GDSII.EXPORT_LAYER_MAP

        output = OutputGdsii(file_name='', layer_map=layer_map)
        output.viewer(my_lib)

    def gdsii_output(self, file_name=None, unit=RDD.GDSII.UNIT, grid=RDD.GDSII.GRID, layer_map=None):
        my_lib = Library(name=self.name, unit=unit, grid=grid)
        my_lib += self
        if layer_map is None:
            layer_map = RDD.GDSII.EXPORT_LAYER_MAP
        output = OutputGdsii(file_name=file_name, layer_map=layer_map)
        output.write(my_lib)
        LOG.debug("Finished writing structure to GDS2.")


class OutputPlotlyNetlist(__Aspects__):

    def netlist_output(self):
        from spira.yevon.io.output_netlist import PlotlyGraph
        output = PlotlyGraph()
        output._plotly_netlist(G=self.netlist.g, graphname=self.name)


class OutputBokehNetlist(__Aspects__):
    pass
    