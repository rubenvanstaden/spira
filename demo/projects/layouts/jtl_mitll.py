import spira
import time
from spira import io
from spira.lpe.mask import Mask
from copy import copy, deepcopy


if __name__ == '__main__':

    start = time.time()

    # name = 'ex5'
    # name = 'jj_mitll_2'
    # name = 'splitt_v0.3'
    # name = 'mitll_dsndo_xic'
    # name = 'mitll_jtl_double'
    # name = 'mitll_SFQDC_draft'

    # Level 2 circuits
    # ----------------
    # name = 'LSmitll_jtl_new'
    # name = 'LSmitll_jtlt_new'
    # name = 'LSmitll_ptlrx_new'
    # name = 'LSmitll_DCSFQ_original'
    # name = 'LSmitll_SPLITT_new'
    # name = 'LSmitll_DFFT_new'
    # name = 'LSmitll_MERGET_new'
    name = 'LSmitll_SFQDC'
    # name = 'LSmitll_NOT_new'

    # Level 3 circuits
    # ----------------
    # name = 'LSmitll_DCSFQ_new'

    filename = io.current_path(name)
    input_cell = io.import_gds(filename=filename)

    cv_cell = io.device_detector(cell=input_cell)
    ms_cell = io.circuit_detector(cell=cv_cell)

    mask = Mask(name=input_cell.name, cell=ms_cell)

    mask.netlist
    mask.output()

    # input_cell.output()
    # cv_cell.output()
    # ms_cell.output()

    end = time.time()
    print(end - start)

