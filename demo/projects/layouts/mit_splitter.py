import os
import spira
from spira.gdsii.io import current_path
from spira.lpe.primitives import SLayout
from demo.pdks.process.mitll_pdk.database import RDD


if __name__ == '__main__':
    name = 'splitt_v0.3'
    filename = current_path(name)
    cell = spira.import_gds(filename=filename)
    # cell.output()

    layout = SLayout(cell=cell, level=2)
    layout.output()


