from spira.log import SPIRA_LOG as LOG
from spira.yevon.filters.filter import Filter


class PolygonToRouteFilter(Filter):

    def __filter___Polygon____(self, item):
        if item.count > 0:
            LOG.debug("PolygonToRouteFilter is filtering out item {}".format(item))
        else:
            raise ValueError('Polygon has no points.')

    def __repr__(self):
        return "[SPiRA: LayerFilterDelete] (layer count {})".format(len(self.layers))



