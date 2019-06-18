import sys


def initialize():
    from spira import log as LOG
    from . import settings
    LOG.start(name=settings.LIB_NAME, text=settings.START_MESSAGE)


initialize()


