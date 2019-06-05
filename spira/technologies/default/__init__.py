from spira.yevon.process import get_rule_deck


__all__ = ['RDD']


RDD = get_rule_deck()

# --- Initialize -------------------------------------------------------------------------------

RDD.name = 'SPiRA-DEFAULT'
RDD.desc = 'Default SPiRA process information, that mimics a general SFQ fabrication process.'

# --- Imports ----------------------------------------------------------------------------------

from .general import *
from .database import *
from .display_resources import *

