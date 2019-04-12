import sys

# from spira.core import *
# from spira.yevon import *
# from spira.yevon.geometry import shapes
# from spira.yevon.gdsii.cell import Cell


def initialize():
    from spira import log as LOG
    from . import settings
    LOG.start(name=settings.LIB_NAME, text=settings.START_MESSAGE)


initialize()


