import spira
from spira.gdsii.io import current_path
from spira.lpe.circuits import Circuit
from demo.pdks.process.mitll_pdk.database import RDD


if __name__ == '__main__':

    # name = 'jj_mitll_2'
    name = 'mitll_jtl_double'
    # name = 'mitll_dsndo_xic'
    # name = 'mitll_SFQDC_draft'

    filename = current_path(name)
    cell = spira.import_gds(filename=filename)
    # cell.output()

    layout = Circuit(cell=cell, level=2)
    # layout.netlist
    layout.mask.output()


