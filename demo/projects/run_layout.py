import os
import spira
from spira import settings
from copy import copy, deepcopy

path = os.getcwd() + '/layouts/'

from spira.lpe.primitives import SLayout
from demo.pdks.process.mitll_pdk import database
if __name__ == '__main__':

#     name = 'aist_junction'
    name = 'mitll_jtl_single'

    file_name = path + name + '.gds'

    layout = spira.import_gds(filename=file_name, flatten=False)
#     layout.construct_gdspy_tree()

    mask = SLayout(cell=layout, library=settings.get_library(), lcar=10, algorithm=1, level=2)
    mask.construct_gdspy_tree()

