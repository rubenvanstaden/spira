import spira
from spira import param
from demo.pdks import ply
from spira.lpe import mask


RDD = spira.get_rule_deck()


class __TemplateCell__(spira.Cell):
    pass


class ViaTemplate(__TemplateCell__):

    layer1 = param.LayerField(number=3)
    layer2 = param.LayerField(number=8)
    via_layer = param.LayerField(number=9)

    def create_elementals(self, elems):
        M1 = spira.ElementList()
        M2 = spira.ElementList()

        for S in elems:
        # for e in elems:
            # # assert isinstance(e, ply.Polygon)
            # if e.player.purpose == RDD.PURPOSE.METAL:
            #     if e.player.layer == self.layer1:
            #         M1 += e
            #     elif e.player.layer == self.layer2:
            #         M2 += e

            # if e.player.purpose in [RDD.PURPOSE.PRIM.VIA, RDD.PURPOSE.PRIM.JUNCTION]:
            #     if e.player.layer == self.via_layer:
            #         for M in M1:
            #             if e.polygon | M.polygon:
            #                 prev_port = e.ports[0]
            #                 e.ports[0] = spira.Port(
            #                     name=e.name, 
            #                     midpoint=prev_port.midpoint,
            #                     orientation=prev_port.orientation,
            #                     gdslayer=M.player.layer
            #                 )

            #         for M in M2:
            #             if e.polygon | M.polygon:
            #                 prev_port = e.ports[1]
            #                 e.ports[1] = spira.Port(
            #                     name=e.name, 
            #                     midpoint=prev_port.midpoint,
            #                     orientation=prev_port.orientation,
            #                     gdslayer=M.player.layer
            #                 )

            if issubclass(type(S.ref), mask.__Mask__):
                for e in S.ref.elementals:
                    # assert isinstance(e, ply.Polygon)
                    if e.player.purpose == RDD.PURPOSE.METAL:
                        if e.player.layer == self.layer1:
                            M1 += e
                        elif e.player.layer == self.layer2:
                            M2 += e

                    if e.player.purpose in [RDD.PURPOSE.PRIM.VIA, RDD.PURPOSE.PRIM.JUNCTION]:
                        if e.player.layer == self.via_layer:
                            for M in M1:
                                if e.polygon | M.polygon:
                                    prev_port = e.ports[0]
                                    e.ports[0] = spira.Port(
                                        name=e.name, 
                                        midpoint=prev_port.midpoint,
                                        orientation=prev_port.orientation,
                                        gdslayer=M.player.layer
                                    )

                            for M in M2:
                                if e.polygon | M.polygon:
                                    prev_port = e.ports[1]
                                    e.ports[1] = spira.Port(
                                        name=e.name, 
                                        midpoint=prev_port.midpoint,
                                        orientation=prev_port.orientation,
                                        gdslayer=M.player.layer
                                    )

        return elems

