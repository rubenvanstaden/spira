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
    purpose = PurposeLayerParameter()
    edge_type = IntegerParameter(default=constants.EDGE_TYPE_NORMAL)


class EdgeFilter(__EdgeFilter__):
    """ Filter only passes edges with the specified purpose. """

    def __filter___Cell____(self, item):
        from copy import deepcopy
        from spira.yevon.gdsii.cell import Cell

        elems = ElementList()
        for p1 in deepcopy(item.elements):
            if p1.layer.purpose == RDD.PURPOSE.METAL:
                for edge in p1.edges:
                    e = EdgeAdapter(original_edge=edge, edge_type=self.edge_type)
                    # print(e)
                    elems += e
                    # elems += edge.outside.transform(edge.transformation)
                elems += p1

        cell = Cell(elements=elems)
        return cell

    def __repr__(self):
        return "[SPiRA: EdgeFilter] ())".format()

