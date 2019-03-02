import spira
from spira import param
from copy import deepcopy
from spira.lpe.containers import __CellContainer__


RDD = spira.get_rule_deck()


class BoundingBox(__CellContainer__):
    """ Add a GROUND bbox to Device for primitive and DRC
    detection, since GROUND is only in Mask Cell. """

    S = param.DataField()

    def create_elementals(self, elems):
        setter = {}
        c_cell = deepcopy(self.S.ref)
        polygons = c_cell.elementals.flat_copy()
        for p in polygons:
            layer = p.gdslayer.number
            setter[layer] = 'not_set'
        for p in polygons:
            for pl in RDD.PLAYER.get_physical_layers(purposes=['METAL', 'GND']):
                if pl.layer == p.gdslayer:
                    if setter[pl.layer.number] == 'not_set':
                        l1 = spira.Layer(name='BoundingBox', number=pl.layer.number, datatype=9)
                        ply = spira.Polygons(shape=self.S.ref.pbox, gdslayer=l1)
                        if self.S.rotation:
                            ply.rotate(angle=self.S.rotation)
                        if self.S.reflection:
                            ply.reflect()
                        ply.center = self.S.midpoint
                        elems += ply
                        setter[pl.layer.number] = 'already_set'
        return elems

    def create_ports(self, ports):
        """ Commit the unlocked ports of the Device to the Block. """

        for name, port in self.S.ports.items():
            if port.locked is False:
                edgelayer = deepcopy(port.gdslayer)
                edgelayer.datatype = 75
                m_term = spira.Term(
                    name=port.name,
                    gdslayer=deepcopy(port.gdslayer),
                    midpoint=deepcopy(port.midpoint),
                    orientation=deepcopy(port.orientation),
                    reflection=port.reflection,
                    edgelayer=edgelayer,
                    width=port.width,
                    connections=deepcopy(port.connections)
                )
                ports += m_term
                
        # for name, port in self.S.ports.items():
        #     if port.locked is False:
        #         edgelayer = deepcopy(port.gdslayer)
        #         edgelayer.datatype = 75
        #         m_term = spira.Term(
        #             name=port.name,
        #             gdslayer=deepcopy(port.gdslayer),
        #             midpoint=deepcopy(port.midpoint),
        #             orientation=deepcopy(port.orientation),
        #             reflection=port.reflection,
        #             edgelayer=edgelayer,
        #             width=port.width,
        #         )
        #         ports += m_term

        return ports
