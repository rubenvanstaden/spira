import os
import gdspy
import numpy as np

# ------------------------------ SPiRA Information -----------------------------

__version__ = '0.0.3'
__release__ = 'Auron [Beta]'

LIB_NAME = 'SPiRA'
LIB_DESCRIPTION = 'SPiRA: The Virtuoso'
VERSION = 'Version {}-{}'.format(__version__, __release__)
COPYRIGHT_INFO = 'MIT License'
AUTHOR = 'Ruben van Staden'
AUTHOR_EMAIL = 'rubenvanstaden@gmail.com'

START_MESSAGE = '{} - {}'.format(VERSION, COPYRIGHT_INFO)

# ----------------------------- Default Globals --------------------------------

_current_gdsii_library = None
_current_layerlist = None

DEFAULT_LIBRARY = None

# ----------------------------- Initialize Library -----------------------------

def initialize():
    from spira.yevon.process.settings import RDD
    from spira.yevon.gdsii.library import Library
    # from spira.yevon.process.layer_list import LayerList
    from spira.yevon.process.gdsii_layer import LayerList

    global DEFAULT_LIBRARY
    DEFAULT_LIBRARY = Library('SPiRA-default',
        unit=RDD.GDSII.UNIT,
        precision=RDD.GDSII.PRECISION
    )

    set_library(DEFAULT_LIBRARY)
    set_current_layerlist(LayerList())


def set_library(library):
    """ Set the working library. """
    global _current_gdsii_library
    _current_gdsii_library = library


def get_library():
    """ Return current working library. """
    if _current_gdsii_library is None:
        initialize()
    return _current_gdsii_library


def get_current_layerlist():
    # from spira.yevon.process.layer_list import LayerList
    from spira.yevon.process.gdsii_layer import LayerList
    if _current_layerlist is None:
        return LayerList()
    return _current_layerlist


def set_current_layerlist(layerlist):
    global _current_layerlist
    _current_layerlist = layerlist

