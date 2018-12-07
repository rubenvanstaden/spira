import os
import gdspy

# ------------------------------ SPiRA Information -----------------------------

LIB_NAME = 'SPiRA'
LIB_DESCRIPTION = 'SPiRA: The Virtuoso'
VERSION = 'Version 0.0.1-Auron'
COPYRIGHT_INFO = 'MIT License'
AUTHOR = 'Ruben van Staden'
AUTHOR_EMAIL = 'rubenvanstaden@gmail.com'

START_MESSAGE = '{} - {}'.format(VERSION, COPYRIGHT_INFO)

# ----------------------------- Default Globals --------------------------------

GRID = 5e-9
UM = 10e-6
NM = 10e-9
PM = 10e-12

UNITS = UM
SCALE = NM

_current_library = None

DEFAULT_LIBRARY = None

# ----------------------------- Initialize Library -----------------------------

def initialize():
    from .kernel.library import Library
    from .rdd.settings import RDD
    # from .templates.templates import JunctionTemplate
    # from .default.templates import JunctionTemplate

    global DEFAULT_LIBRARY 
    DEFAULT_LIBRARY = Library('SPiRA-default',
                              unit=RDD.GDSII.UNIT,
                              precision=RDD.GDSII.PRECISION)

    # DEFAULT_LIBRARY.add_pcell(pcell=RDD.DEVICES.JJ.PCELL)

    set_library(DEFAULT_LIBRARY)


def set_library(library):
    """ Set the working library. """
    global _current_library
    _current_library = library


def get_library():
    """ Return current working library. """
    if _current_library is None:
        initialize()
    return _current_library

# --------------------------------- Extras -------------------------------------

