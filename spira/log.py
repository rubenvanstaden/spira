import sys
import gdspy
import logging

import logging
import sys


SPIRA_LOGGING_HANDLER = logging.StreamHandler(sys.stderr)
SPIRA_LOG = logging.getLogger('SPiRA')
SPIRA_LOG.setLevel(logging.ERROR)
SPIRA_LOG.addHandler(SPIRA_LOGGING_HANDLER)


from colorama import init, Fore, Back, Style
init(autoreset=True)


def print_cellrefs(cell):
    print('')
    magenta_print('CellReferences')
    for element in cell.elements:
        if isinstance(element, gdspy.CellReference):
            print(element)
            print('')


def list_layout_cells(gds):
    """ List the Cells in the GDS layout. """

    gdsii = gdspy.GdsLibrary()
    gdsii.read_gds(gds, unit=1.0e-12)

    print('Cell List:')
    for key in gdsii.cell_dict.keys():
        print('      -> ' + key)
    print('')


def list_ntron_cells(gds):
    """ List the Cells in the GDS layout. """

    gdsii = gdspy.GdsLibrary()
    gdsii.read_gds(gds, unit=1.0e-12)

    print('Cell List:')
    for key in gdsii.cell_dict.keys():
        print('      -> ' + key)
    print('')


def list_jj_cells(gds):
    """ List the Cells in the GDS layout. """

    gdsii = gdspy.GdsLibrary()
    gdsii.read_gds(gds, unit=1.0e-12)

    print('Cell List:')
    for key in gdsii.cell_dict.keys():
        print('      -> ' + key)
    print('')


def list_via_cells(gds):
    """ List the Cells in the GDS layout. """

    gdsii = gdspy.GdsLibrary()
    gdsii.read_gds(gds, unit=1.0e-12)

    print('Cell List:')
    for key in gdsii.cell_dict.keys():
        print('      -> ' + key)
    print('')


def parameter_print(arguments):
    print ('Parameters:')
    for key, value in arguments.items():
        print('      ' + str(key) + ' : ' + str(value))


def drc_fail(text):
    string = '[{}]'.format(Fore.LIGHTRED_EX + 'FAIL')
    return string

    # print('')
    # print('[', end='')
    # print(Fore.LIGHTRED_EX + 'FAIL', end='')
    # print('] ', end='')
    # print(text)
    # print('')


def header(text):
    print('')
    print('[', end='')
    print(Fore.LIGHTGREEN_EX + '*', end='')
    print('] ', end='')
    print(text)
    print('')


def section(text):
    print('')
    print(Fore.LIGHTMAGENTA_EX + '->', end='')
    print(' ', end='')
    print(text)


def success(text):
    print('[', end='')
    print(Fore.LIGHTGREEN_EX + 'Success', end='')
    print('] ', end='')
    print(text)


def start(name, text):
    print('')
    print('[', end='')
    print(Fore.LIGHTGREEN_EX + name, end='')
    print('] ', end='')
    print(text)
    print('---------------------------------------------')


def rdd(text):
    print('\n---------------------------------------------')
    print('[', end='')
    print(Fore.LIGHTCYAN_EX + 'RDD', end='')
    print('] ', end='')
    print(text)


def a_print(text):
    print('')
    print(Fore.LIGHTGREEN_EX + '*', end='')
    print('*', end='')
    print('* ', end='')
    print(text)
    print('')


def b_print(text):
    print('')
    print('*', end='')
    print(Fore.LIGHTGREEN_EX + '*', end='')
    print('* ', end='')
    print(text)
    print('')


def c_print(text):
    print('')
    print('*', end='')
    print('* ', end='')
    print(Fore.LIGHTGREEN_EX + '*', end='')
    print(text)
    print('')


def begin_print(text):
    print(Fore.GREEN + '--------------------------', end='')


def end_print(text):
    print('')
    print(Fore.LIGHTCYAN_EX + '>> ', end='')
    print(text)
    print('')