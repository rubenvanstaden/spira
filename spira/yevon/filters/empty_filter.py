from spira.log import SPIRA_LOG as LOG
from spira.yevon.filters.filter import Filter


__all__ = ['EmptyFilter']


class EmptyFilter(Filter):
    """ Empty filter used for concatenation. """

    def filter_default(self, item):
        if hasattr(item, 'is_empty'):
            if item.is_empty():
                LOG.debug('Emptyfilter is filtering out : {}'.format(item))
                return []
        return [item]

    def __repr__(self):
        return '<EmptyFilter>'