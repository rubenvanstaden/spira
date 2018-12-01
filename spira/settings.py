import os
import gdspy
import pyclipper

from termcolor import colored
from collections import defaultdict

from spira import log as LOG

import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.offline as offline

# ---------------------------------------------------------------------------

LIB_NAME = 'SPiRA'
LIB_DESCRIPTION = 'SPiRA: The Virtuoso'
VERSION = 'version 0.0,1-alpha'
COPYRIGHT_INFO = 'MIT License'
AUTHOR = 'Ruben van Staden'
AUTHOR_EMAIL = 'rubenvanstaden@gmail.com'

START_MESSAGE = '\n{} {} - {}'.format(LIB_NAME, VERSION, COPYRIGHT_INFO)

GRID = 5e-9
UM = 10e-6
NM = 10e-9
PM = 10e-12

UNITS = UM
SCALE = NM

_library = None

LIB = None
DEVICES = None
PDK_FILE = None

# ---------------------------------------------------------------------------

def set_library(library):
    """ Set the working library. """
    global _library
    _library = library


def get_library():
    """ Return current working library. """
    global _library
    return _library


def init(path, library=None, gdsname=None, pdkname='ldf'):

    pdk_file = path + pdkname + '.json'
    gds_file = path + gdsname + '.gds'

    default_devices = {'path': 0, 'via': 1, 'jj': 3, 'ntron': 7}

    global PDK_FILE
    PDK_FILE = pdk_file
    global DEVICES
    DEVICES = default_devices
    global LIB
    LIB = library(gds_file=gds_file)

    print('\nInitializing library -> {}\n'.format(LIB.name))


def invert_dict(d):
    return dict([ (v, k) for k, v in d.items() ])


def get_polygons(elements, device_type):
    from spira.kernel.elemental.polygons import Polygons
    from spira.kernel.parameters.field.element_list import ElementList
    polygons = ElementList()
    for e in elements:
        if isinstance(e, Polygons):
            if e.gdsdatatype == DEVICES[device_type]:
                polygons += e
    return polygons


def get_device_name(datatype):
    idevices = invert_dict(DEVICES)
    name = idevices[datatype]
    return name[0].upper() + name[1:]


def check_terminal_duplicates(edgelabels):
    duplicates = defaultdict(list)

    for i, item in enumerate(edgelabels):
        duplicates[item].append(i)

    duplicates = {k:v for k, v in duplicates.items() if len(v) > 1}

    for key, value in duplicates.items():
        if key is not None:
            if len(value) > 1:
                raise('Terminal duplicates!')
