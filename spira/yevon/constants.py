import numpy as np


DEG2RAD = np.pi / 180.0
RAD2DEG = 180.0 / np.pi

SCALE_UP = 1e+6
SCALE_DOWN = 1e-6
OFFSET = 0.3

PATH_TYPE_NORMAL = 0
PATH_TYPE_ROUNDED = 1
PATH_TYPE_EXTENDED = 2
PATH_TYPES = [PATH_TYPE_NORMAL, PATH_TYPE_ROUNDED, PATH_TYPE_EXTENDED]

# NORTH = [0.0, 1.0]
# SOUTH = (0.0, -1.0)
# EAST = (1.0, 0.0)
# WEST = (-1.0, 0.0)

CLIPPER_SCALE = 2**30

from spira.yevon.geometry.coord import Coord
NORTH = Coord(0.0, 1.0)
SOUTH = Coord(0.0, -1.0)
EAST = Coord(1.0, 0.0)
WEST = Coord(-1.0, 0.0)





