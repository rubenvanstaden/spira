import os
import spira
from spira import settings
from copy import copy, deepcopy

path = os.getcwd() + '/'

from spira.lpe.primitives import SLayout
if __name__ == '__main__':

#     name = 'LSmitll_jtlt_new'
#     name = 'LSmitll_SFQDC_new'

#     name = '0_jj_aist'
    name = 'ex3'

#     name = 'jtl_mitll'
#     name = 'jtl_mitll_density_pass'
#     name = 'jtl_mitll_density_max'
#     name = 'jtl_mitll_density_fail'
#     name = 'jtl_mitll_diff'
#     name = 'jtl_mitll_diff_errors'
#     name = 'jj_mitll_drc_errors'

#     name = 'splitt'
#     name = 'splitt_v0.2'
#     name = 'splitt_v0.3'

#     name = 'coils_ind'
#     name = 'jtl_dr'
#     name = 'lesfq'
#     name = 't12'
#     name = 'medium_ex9'
#     name = 'large_ex6'
#     name = 'large_ex7'

    file_name = path + name + '.gds'

    layout = spira.import_gds(filename=file_name, flatten=False)
#     layout.construct_gdspy_tree()

#     struct = Circuit(cell=layout, library=settings.get_library())
#     struct.construct_gdspy_tree()

#     mask = MaskCell(cell=layout, library=settings.get_library(), lcar=10, algorithm=1, level=2)
#     mask.construct_gdspy_tree()

    mask = SLayout(cell=layout, library=settings.get_library(), lcar=10, algorithm=1, level=2)
    mask.construct_gdspy_tree()








