import os
import spira
from spira.gdsii.io import current_path
from spira.lpe.primitives import SLayout


if __name__ == '__main__':
    name = 'aist_junction'
    filename = current_path(name)
    cell = spira.import_gds(filename=filename)
    # cell.output()

    layout = SLayout(cell=cell, level=2)
    layout.output()


