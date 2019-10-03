from spira.yevon.process import get_rule_deck


__all__ = ['RDD']


RDD = get_rule_deck()

# --- Initialize -------------------------------------------------------------------

RDD.name = 'MiTLL'
RDD.desc = 'The MIT LL SFQ5ee fabrication process.'

# --- Imports ----------------------------------------------------------------------

from .general import *
from .database import *
from .display_resources import *

