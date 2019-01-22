import spira
from spira import param
from copy import copy, deepcopy


RDD = spira.get_rule_deck()


class __TemplateCell__(spira.Cell):
    pass


class __TempatePrimitive__(__TemplateCell__):
    pass

from spira.lpe.primitives import NLayer
from spira.lpe.primitives import MLayer

class ViaTemplate(__TempatePrimitive__):

    layer1 = param.LayerField(number=3)
    layer2 = param.LayerField(number=8)
    via_layer = param.LayerField(number=9)

    def create_elementals(self, elems):
        M1 = spira.ElementList()
        M2 = spira.ElementList()
        contacts = spira.ElementList()

        # for e in elems:
        #     if e.player.purpose == RDD.PURPOSE.METAL:
        #         if e.player.layer == self.layer1:
        #             M1 += e
        #         elif e.player.layer == self.layer2:
        #             M2 += e
        #     if e.player.purpose == RDD.PURPOSE.PRIM.VIA:
        #         if e.player.layer == self.via_layer:
        #             contacts += e

        for ce in elems:
            for e in ce.ref.elementals:
                if isinstance(e, (MLayer, NLayer)):

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




        # # ce = compose elemental
        # for ce in elems:
        #     for e in ce.ref.elementals:
        #         if isinstance(e, spira.SRef):
        #             # e.ref.ports[0] = spira.Port(name='GOD!!!')
        #         # print(e)
        #     #     if isinstance(e, (MLayer, NLayer)):

        #             if e.ref.player.purpose == RDD.PURPOSE.METAL:
        #                 if e.ref.player.layer == self.layer1:
        #                     M1 += e
        #                 elif e.ref.player.layer == self.layer2:
        #                     M2 += e
                        
        #             # print(M1)

        #             if e.ref.player.purpose == RDD.PURPOSE.PRIM.VIA:
        #                 if e.ref.player.layer == self.via_layer:
        #                     # pass
        #                     # contacts += e
        #                     # e.ref.ports[0] = spira.Port(name=e.ref.name)

        #                     for M in M1:
        #                         if e.ref.polygon | M.ref.polygon:
        #                             print(self.via_layer)
        #                             pp = e.ref.polygon | M.ref.polygon
        #                             # TODO: Apply DRC enclosure rule here.
        #                     #         # print(e.ports[0])
        #                             # D.ports[0]._update(name=D.name, layer=M.player.layer)
        #                             prev_port = e.ref.ports[0]
        #                             e.ref.ports[0] = spira.Port(
        #                                 name=e.ref.name, 
        #                                 midpoint=prev_port.midpoint,
        #                                 orientation=prev_port.orientation,
        #                                 gdslayer=M.ref.player.layer
        #                             )
        #                     #         # print(e.ports[0])
        #                     #         # print('')

        #                     for M in M2:
        #                         if e.ref.polygon | M.ref.polygon:
        #                             # print('2222222222222222222')
        #                             pp = e.ref.polygon | M.ref.polygon
        #                             # TODO: Apply DRC enclosure rule here.
        #                             # e.ref.ports[1]._update(name=e.ref.name, layer=M.ref.player.layer)
        #                             prev_port = e.ref.ports[1]
        #                             e.ref.ports[1] = spira.Port(
        #                                 name=e.ref.name, 
        #                                 midpoint=prev_port.midpoint,
        #                                 orientation=prev_port.orientation,
        #                                 gdslayer=M.ref.player.layer
        #                             )




        # for D in contacts:
        #     print(D)
        #     for M in M1:
        #         if D.polygon | M.polygon:
        #             # print('1111111111111111111')
        #             pp = D.polygon | M.polygon
        #             # TODO: Apply DRC enclosure rule here.
        #             print(D.ports[0])
        #             # D.ports[0]._update(name=D.name, layer=M.player.layer)
        #             D.ports[0] = spira.Port(name=D.name, gdslayer=M.player.layer)
        #             print(D.ports[0])
        #     for M in M2:
        #         if D.polygon | M.polygon:
        #             # print('2222222222222222222')
        #             pp = D.polygon | M.polygon
        #             # TODO: Apply DRC enclosure rule here.
        #             D.ports[1]._update(name=D.name, layer=M.player.layer)
        #     print('')



        return elems

