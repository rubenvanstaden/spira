import spira.all as spira
from spira.yevon.rdd import get_rule_deck
from copy import deepcopy


RDD = get_rule_deck()


__all__ = ['device_detector', 'circuit_detector']


def map_references(c, c2dmap):
    for e in c.elementals.sref:
        if e.ref in c2dmap.keys():
            e.ref = c2dmap[e.ref]
            e._parent_ports = e.ref.ports
            e._local_ports = {(port.name, port.gds_layer.number, port.midpoint[0], port.midpoint[1]):deepcopy(port) for port in e.ref.ports}
            e.port_locks = {(port.name, port.gds_layer.number, port.midpoint[0], port.midpoint[1]):port.locked for port in e.ref.ports}
            # e._local_ports = {port.node_id:deepcopy(port) for port in e.ref.ports}
            # e.port_locks = {port.node_id:port.locked for port in e.ref.ports}


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
            
    # for c in cell.dependencies():
    #     map_references(c, c2dmap)

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

    # for c in cell.dependencies():
    #     map_references(c, c2dmap)
        
    return c2dmap[cell]
