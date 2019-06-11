from spira.log import SPIRA_LOG as LOG
from spira.yevon.filters.filter import Filter
# from spira.yevon.process.layer_list import LayerList, LayerListField
from spira.yevon.process.gdsii_layer import LayerList, LayerListField


__all__ = ['LayerFilterAllow', 'LayerFilterDelete']


class __LayerFilter__(Filter):
    layers = LayerListField()


class LayerFilterAllow(__LayerFilter__):
    def __filter___LayerElemental____(self, item):
        if item.layer in self.layers:
            return [item]
        else:
            LOG.debug("LayerFilterAllow is filtering out item %s" %item)
            return []

    def __repr__(self):
        return "[SPiRA: LayerFilterDelete] (layer count {})".format(len(self.layers))


class LayerFilterDelete(__LayerFilter__):
    def __filter___LayerElemental____(self, item):
        if item.layer in self.layers:
            LOG.debug("LayerFilterDelete is filtering out item %s" %item)
            return []
        else:
            return [item]

    def __repr__(self):
        return "[SPiRA: LayerFilterDelete] (layer count {})".format(len(self.layers))



