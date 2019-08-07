from spira.log import SPIRA_LOG as LOG
from spira.yevon.filters.filter import Filter
from spira.yevon.process.gdsii_layer import LayerList, LayerListParameter
from spira.yevon.gdsii.elem_list import ElementListParameter, ElementList
from spira.yevon.geometry.ports.port_list import PortListParameter
from spira.yevon.geometry.ports import Port
from spira.yevon.geometry.ports.port_list import PortList
from spira import settings
from spira.yevon.utils import geometry
from copy import deepcopy
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = [
    'DeviceMetalFilter',
]


class __DeviceFilter__(Filter):
    pass


class DeviceMetalFilter(__DeviceFilter__):
    """  """

    def wrap_references(self, cell, c2dmap, devices):
        from spira.yevon.gdsii.pcell import Device
        for e in cell.elements.sref:
            if isinstance(e.reference, Device):
                D = deepcopy(e.reference)
                D.elements.transform(e.transformation)
                D.ports.transform(e.transformation)
                devices[D] = D.elements

                D.elements = ElementList()
                S = deepcopy(e)
                S.reference = D
                c2dmap[cell] += S
            else:
                S = deepcopy(e)
                S.reference = c2dmap[e.reference]
                c2dmap[cell] += S

    def filter_Cell(self, item):
        from spira.yevon.gdsii.cell import Cell

        ports = PortList()
        elems = ElementList()

        c2dmap, devices = {}, {}

        for cell in item.dependencies():
            # FIXME: Why can I not use Cell?
            # ERC Port doesn't connect.
            D = item.__class__(
                name=cell.name,
                elements=deepcopy(cell.elements.polygons),
                ports=deepcopy(cell.ports)
            )
            c2dmap.update({cell: D})

        for cell in item.dependencies():
            self.wrap_references(cell, c2dmap, devices)

        D = c2dmap[item]

        for e in D.elements.polygons:
            if e.layer.purpose.symbol == 'METAL':
                e.layer.purpose = RDD.PURPOSE.CIRCUIT_METAL
                # e.layer.purpose = RDD.PURPOSE.METAL

        for d in D.dependencies():
            if d in devices.keys():
                d.elements = devices[d]

                for e in d.elements.polygons:
                    if e.layer.purpose.symbol == 'METAL':
                        e.layer.purpose = RDD.PURPOSE.DEVICE_METAL
                        # e.layer.purpose = RDD.PURPOSE.METAL

        return D

        # elems = D.elements

        # for p in item.ports:
        #     ports += p

        # cell = Cell(elements=elems, ports=ports)
        # return cell

    def __repr__(self):
        return "[SPiRA: DeviceMetalFilter] (layer count {})".format(0)

