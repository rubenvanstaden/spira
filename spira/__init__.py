import sys

import spira.log as LOG

from spira.rdd import get_rule_deck
RDD = get_rule_deck()

from spira.rdd import *

from spira.gdsii.cell import Cell
from spira.gdsii.cell import Connector
from spira.gdsii.library import Library
from spira.gdsii.lists.cell_list import CellList

from spira.layers import *
from spira.gdsii import *
from spira.lne import *
from spira.lgm import *
from spira.lgm import shapes
from spira.lgm.route.routing import Route

from spira.core.lists import ElementList

def initialize():
    from spira import log as LOG
    from . import settings
    LOG.start(name=settings.LIB_NAME, text=settings.START_MESSAGE)

initialize()


