import os
import spira.all as spira
from spira.yevon import io
from copy import copy, deepcopy


from spira.technologies.mit.process.database import RDD


if __name__ == '__main__':

    # file_name = '/home/therealtyler/code/phd/spira/tests/8-parse/jj_mitll.gds'
    # file_name = '/home/therealtyler/code/phd/spira/tests/8-parse/mit/ruben/jtl_mitll_diff.gds'
    # file_name = '/home/therealtyler/code/phd/spira/tests/8-parse/mit/lieze/jtl.gds'
    # file_name = '/home/therealtyler/code/phd/spira/tests/8-parse/mit/lieze/LSmitll_jtlt.gds'
    file_name = '/home/therealtyler/code/phd/spira/tests/8-parse/mit/lieze/ptlrx_gs.gds'
    # file_name = '/home/therealtyler/code/phd/spira/tests/8-parse/mit/lieze/dfft.gds'
    # file_name = '/home/therealtyler/code/phd/spira/tests/8-parse/mit/lieze/circuit.gds'

    D = io.import_gds(filename=file_name, pcell=False)

    # for e in D.elements.sref:
    #     print(e)
    #     for i in e.reference.elements:
    #         print(i)
    #     print('')

    # D.gdsii_output()
    D.gdsii_output_expanded()

