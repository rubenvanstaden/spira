import os
import gdspy
import numpy as np
from math import floor


# ----------------------------- SPiRA Information -----------------------------


__version__ = '0.1.1'
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
        # precision=RDD.GDSII.PRECISION
    )

    set_current_library(DEFAULT_LIBRARY)
    set_current_layerlist(LayerList())


def set_current_library(library):
    """ Set the working library. """
    global _current_gdsii_library
    _current_gdsii_library = library


def get_current_library():
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


# ----------------------------- Snap to Grid -----------------------------


def get_grids_per_unit(library=None):
    if library is None:
        library = get_current_library()
    return library.grids_per_unit


def snap_value(value, grids_per_unit=None):
    """ Round a distance to a grid value. """
    if grids_per_unit is None:
        grids_per_unit = get_grids_per_unit()
    return floor(value * grids_per_unit + 0.5) / (grids_per_unit)


def snap_coordinate(coordinate, grids_per_unit=None):
    """ Round a coordinate to a grid value. """
    from spira.yevon.geometry.coord import Coord
    if grids_per_unit is None:
        grids_per_unit = get_grids_per_unit()
    x = floor(coordinate[0] * grids_per_unit + 0.5) / (grids_per_unit)
    y = floor(coordinate[1] * grids_per_unit + 0.5) / (grids_per_unit)
    return Coord(x, y)


def snap_shape(coordinates, grids_per_unit=None):
    """ Round the coordinates of a shape to a grid value. """
    from spira.yevon.geometry import shapes
    if grids_per_unit is None:
        grids_per_unit == get_grids_per_unit()
    shape = shapes.Shape(coordinates).snap_to_grid(grids_per_unit)
    return shape


def snap_points(points, grids_per_unit=None):
    """ Round a list of points to a grid value. """
    if grids_per_unit is None: 
        grids_per_unit == get_grids_per_unit()
    pts = (floor(points * grids_per_unit + 0.5)) / grids_per_unit
    return pts