import spira.all as spira
from spira.core import param
from copy import deepcopy
from spira.netex.containers import __CellContainer__


RDD = spira.get_rule_deck()


class BoundingBox(__CellContainer__):
    """ Add a GROUND bbox to Device for primitive and DRC
    detection, since GROUND is only in Mask Cell. """

    S = param.DataField()

    def create_elementals(self, elems):
        setter = {}
        c_cell = self.S.ref
        polygons = c_cell.elementals.flat_copy()
        for p in polygons:
            layer = p.gds_layer.number
            setter[layer] = 'not_set'
        for p in polygons:
            for pl in RDD.PLAYER.get_physical_layers(purposes=['METAL', 'GND']):
                if pl.layer.is_equal_number(p.gds_layer):
                    if setter[pl.layer.number] == 'not_set':
                        l1 = spira.Layer(name='BoundingBox', number=pl.layer.number, datatype=9)
                        ply = spira.Polygon(shape=self.S.ref.pbox, gds_layer=l1)
                        elems += ply.transform(self.S.tf)
                        setter[pl.layer.number] = 'already_set'
        return elems

    def create_ports(self, ports):
        """ Commit the unlocked ports of the Device to the Block. """

        # for name, port in self.S.ports.items():
        #     if port.locked is False:
        #         edgelayer = deepcopy(port.gds_layer)
        #         edgelayer.datatype = 75
        #         m_term = spira.Term(
        #             name=port.name,
        #             gds_layer=deepcopy(port.gds_layer),
        #             midpoint=deepcopy(port.midpoint),
        #             orientation=deepcopy(port.orientation),
        #             reflection=port.reflection,
        #             edgelayer=edgelayer,
        #             width=port.width,
        #             connections=deepcopy(port.connections)
        #         )
        #         ports += m_term
                
        # # for name, port in self.S.ports.items():
        # #     if port.locked is False:
        # #         edgelayer = deepcopy(port.gds_layer)
        # #         edgelayer.datatype = 75
        # #         m_term = spira.Term(
        # #             name=port.name,
        # #             gds_layer=deepcopy(port.gds_layer),
        # #             midpoint=deepcopy(port.midpoint),
        # #             orientation=deepcopy(port.orientation),
        # #             reflection=port.reflection,
        # #             edgelayer=edgelayer,
        # #             width=port.width,
        # #         )
        # #         ports += m_term

        return ports
