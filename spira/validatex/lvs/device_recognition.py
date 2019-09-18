import spira.all as spira
from copy import deepcopy
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = ['device_detector', 'circuit_detector']


def device_detector(cell):
    from spira.netex.devices import Device
    from spira.netex.contact import DeviceTemplate

    c2dmap = {}
    for C in cell.dependencies():
        cc = deepcopy(C)
        L = DeviceTemplate(name=C.name, cell=cc, level=1)
        if L.__type__ is not None:
            for key in RDD.DEVICES.keys:
                if L.__type__ == key:
                    D = RDD.DEVICES[key].PCELL(
                        metals=L.metals,
                        contacts=L.contacts,
                        ports=L.ports
                    )
                    c2dmap.update({C: D})
            for key in RDD.VIAS.keys:
                if L.__type__ == key:
                    D = RDD.VIAS[key].DEFAULT(
                        metals=L.metals,
                        contacts=L.contacts,
                        ports=L.ports
                    )
                    c2dmap.update({C: D})
        else:
            c2dmap.update({C: C})

    return c2dmap[cell]


def circuit_detector(cell):
    from spira.netex.devices import Device
    from spira.netex.circuits import Circuit

    c2dmap = {}
    for C in cell.dependencies():
        if not issubclass(type(C), Device):
            if ('Metal' not in C.name) and ('Native' not in C.name):
                D = Circuit(cell=C, level=2)
                c2dmap.update({C: D})
        else:
            c2dmap.update({C: C})

    return c2dmap[cell]
