import sys

import spira.log as LOG

from spira.rdd import get_rule_deck
RDD = get_rule_deck()

from spira.rdd import *

from spira.gdsii.cell import Cell
from spira.gdsii.primitive import *
from spira.gdsii.io import import_gds
from spira.gdsii.library import Library
from spira.gdsii.lists.cell_list import CellList

from spira.gdsii.layer import Layer

from spira.gdsii import *
from spira.lne import *
from spira.lgm import *
from spira.lgm import shapes

from spira.core.lists import ElementList

def initialize():
    from spira import log as LOG
    from . import settings
    spira.LOG.start(name=settings.LIB_NAME, text=settings.START_MESSAGE)

initialize()


