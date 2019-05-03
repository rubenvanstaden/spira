import spira.all as spira
from copy import copy, deepcopy
import os
from spira.yevon import io


if __name__ == '__main__':

    # name = 'ex5'
    # name = 'jj_mitll_2'
    # name = 'splitt_v0.3'
    # name = 'mitll_dsndo_xic'
    # name = 'mitll_jtl_double'
    # name = 'mitll_SFQDC_draft'

    # Level 2 circuits
    # ----------------
    # name = 'Dcsfq'
    name = 'LSmitll_jtl_new'
    # name = 'LSmitll_jtlt_new'
    # name = 'LSmitll_ptlrx_new'
    # name = 'LSmitll_DCSFQ_original'
    # name = 'LSmitll_SPLITT_new'
    # name = 'LSmitll_SFQDC'
    # name = 'LSmitll_MERGET_new'
    # name = 'LSmitll_DFFT_new'
    # FIXME
    # name = 'LSmitll_NOT_new'
    # FIXME
    # name = 'FabJTL'
    # FIXME
    # name = 'FabJTL_T_v0.3'

    # Level 3 circuits
    # ----------------
    # name = 'LSmitll_DCSFQ_new'
    # file_name = '/home/therealtyler/code/phd/spira/spira/technologies/aist/layouts/stable/jj.gds'
    # file_name = '/home/therealtyler/code/phd/spira/spira/technologies/aist/layouts/stable/jj_rotated.gds'
    # file_name = '/home/therealtyler/code/phd/spira/spira/technologies/aist/layouts/stable/jj_reflected.gds'
    # file_name = '/home/therealtyler/code/phd/spira/spira/technologies/aist/layouts/stable/dff.gds'
    # file_name = '/home/therealtyler/code/phd/spira/spira/technologies/aist/layouts/stable/and.gds'
    # file_name = '/home/therealtyler/code/phd/spira/spira/technologies/aist/layouts/stable/jj_hierarchy.gds'
    file_name = '/home/therealtyler/code/phd/spira/spira/technologies/aist/layouts/stable/jj_hierarchy_lvl3.gds'
    # file_name = '/home/therealtyler/code/phd/spira/spira/technologies/aist/layouts/stable/jj_hierarchy_v0.1.gds'
    # file_name = '{}/technologies/{}.gds'.format(os.getcwd(), name)
    print(file_name)
    # filename = io.current_path(name)
    input_cell = io.import_gds(filename=file_name)
    input_cell.output()

