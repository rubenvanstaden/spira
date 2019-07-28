from spira.yevon import constants
from spira.log import SPIRA_LOG as LOG
from spira.yevon.filters.filter import Filter
from spira.yevon.gdsii.elem_list import ElementList
from spira.yevon.geometry.edges.edges import EdgeAdapter
from spira.core.parameters.variables import IntegerParameter
from spira.yevon.process.purpose_layer import PurposeLayerParameter
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = ['EdgeFilter']


class __EdgeFilter__(Filter):
    """ Base class for edge filters. """
    purpose = PurposeLayerParameter()
    edge_type = IntegerParameter(default=constants.EDGE_TYPE_NORMAL)


class EdgeFilter(__EdgeFilter__):
    """ Filter only passes edges with the specified purpose. """

    def filter___Cell__(self, item):
        from copy import deepcopy
        from spira.yevon.gdsii.cell import Cell

        elems = ElementList()
        for p1 in deepcopy(item.elements.polygons):
            if p1.layer.purpose == RDD.PURPOSE.METAL:
                for edge in p1.edges:
                    elems += EdgeAdapter(original_edge=edge, edge_type=self.edge_type)
                elems += p1

        cell = Cell(elements=elems)
        return cell

    def __repr__(self):
        return "[SPiRA: EdgeFilter] ())".format()

