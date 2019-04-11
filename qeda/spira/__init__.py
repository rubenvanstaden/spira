import sys

import spira.log as LOG

from spira.rdd import get_rule_deck
RDD = get_rule_deck()

from spira.rdd import *

from spira.gdsii.cell import Cell
# from spira.gdsii.cell import Connector
from spira.gdsii.library import Library
# from spira.gdsii.cell_list import CellList

from spira.layer import Layer
from spira.gdsii import *
from spira.netex import *
from spira.geometry import *
from spira.geometry import shapes
from spira import process as pc
from spira.geometry.route.routing import Route
from spira.geometry.ports import *
from spira.netex.devices import Device
from spira.netex.circuits import Circuit
from spira import io

from core.elem_list import ElementList
from core.port_list import PortList


def initialize():
    from spira import log as LOG
    from . import settings
    LOG.start(name=settings.LIB_NAME, text=settings.START_MESSAGE)


initialize()


