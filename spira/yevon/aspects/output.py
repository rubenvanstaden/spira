from spira.yevon.aspects.base import __Aspects__
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


class OutputGdsiiAspect(__Aspects__):
    """  """

    def gdsii_output(self, file_name=None, viewer=True, unit=RDD.GDSII.UNIT, grid=RDD.GDSII.GRID, layer_map=None):
        from spira.log import SPIRA_LOG as LOG
        from spira.yevon.gdsii.library import Library
        from spira.yevon.io.output_gdsii import OutputGdsii
        my_lib = Library(name=self.name, unit=unit, grid=grid)
        my_lib += self
        # print(my_lib.cells)
        if layer_map is None:
            layer_map = RDD.GDSII.EXPORT_LAYER_MAP
        output = OutputGdsii(file_name=file_name, layer_map=layer_map)
        output.write(my_lib)
        LOG.debug("Finished writing structure to GDS2.")
        if viewer is True:
            output.viewer()
        
       
class OutputPlotlyNetlist(__Aspects__):
    pass


class OutputBokehNetlist(__Aspects__):
    pass
    