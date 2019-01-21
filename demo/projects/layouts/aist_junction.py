import os
import spira
from spira.gdsii.io import current_path
from spira.lpe.primitives import SLayout
from copy import copy, deepcopy


if __name__ == '__main__':
    name = 'aist_junction'
    # name = 'aist_and'
    filename = current_path(name)
    cell = spira.import_gds(filename=filename)
    # cell.output()

    # layout = SLayout(cell=cell, dev=deepcopy(cell), level=2)
    layout = SLayout(cell=cell, level=2)

    # layout.netlist()
    layout.output()


