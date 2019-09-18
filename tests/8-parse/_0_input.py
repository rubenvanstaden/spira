import os
from spira.technologies.mit.process import RDD
import spira.all as spira
import spira.yevon.io.input_gdsii as io
from copy import copy, deepcopy


if __name__ == '__main__':

    # file_name = '/home/therealtyler/code/phd/spira/tests/8-parse/jj_mitll.gds'
    # file_name = '/home/therealtyler/code/phd/spira/tests/8-parse/mit/ruben/jtl_mitll_diff.gds'
    file_name = '/home/therealtyler/code/phd/spira/tests/8-parse/mit/lieze/jtl.gds'
    # file_name = '/home/therealtyler/code/phd/spira/tests/8-parse/mit/lieze/LSmitll_jtlt.gds'
    # file_name = '/home/therealtyler/code/phd/spira/tests/8-parse/mit/lieze/ptlrx_gs.gds'
    # file_name = '/home/therealtyler/code/phd/spira/tests/8-parse/mit/lieze/dfft.gds'
    # file_name = '/home/therealtyler/code/phd/spira/tests/8-parse/mit/lieze/circuit.gds'

    # input_gdsii = spira.InputGdsii(file_name=file_name)
    # input_gdsii.layer_map = RDD.GDSII.IMPORT_LAYER_MAP

    input_gdsii = spira.InputGdsii(file_name=file_name, layer_map=RDD.GDSII.IMPORT_LAYER_MAP)
    D = input_gdsii.parse()

    D.gdsii_view()
    # D.gdsii_output(file_name='input')

