import spira
from spira import param
from demo.pdks import ply
from spira.lpe.pcells import Structure


RDD = spira.get_rule_deck()


class ViaTemplate(spira.Cell):

    layer1 = param.LayerField(number=3)
    layer2 = param.LayerField(number=8)
    via_layer = param.LayerField(number=9)

    def create_elementals(self, elems):
        M1 = spira.ElementList()
        M2 = spira.ElementList()

        for e in elems:
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


class DeviceTemplate(Structure):

    def generate_physical_polygons(self, pl):
        elems = spira.ElementList()
        R = self.cell.elementals.flat_copy()
        Rm = R.get_polygons(layer=pl.layer)
        for i, e in enumerate(Rm):
            if len(e.polygons[0]) == 4:
                alias = 'devices_box_{}_{}_{}'.format(pl.layer.number, self.cell.node_id, i)
                poly = spira.Polygons(shape=e.polygons)
                elems += ply.Box(name=alias, player=pl, center=poly.center, w=poly.dx, h=poly.dy, level=self.level)
            else:
                alias = 'ply_{}_{}_{}'.format(pl.layer.number, self.cell.node_id, i)
                elems += ply.Polygon(name=alias, player=pl, points=e.polygons, level=self.level)
        return elems

    def create_metals(self, elems):
        for player in RDD.PLAYER.get_physical_layers(purposes='METAL'):
            for e in self.generate_physical_polygons(player):
                elems += e
        return elems

    def create_contacts(self, elems):
        for player in RDD.PLAYER.get_physical_layers(purposes=['VIA', 'JJ']):
            for e in self.generate_physical_polygons(player):
                elems += e
        return elems

    def create_elementals(self, elems):
        for e in self.merged_layers:
            elems += e
        for e in self.contacts:
            elems += e

        for key in RDD.VIAS.keys:
            RDD.VIAS[key].PCELL.create_elementals(elems)

        return elems

    def determine_type(self):
        self.__type__ = None

        for key in RDD.VIAS.keys:
            default_via = RDD.VIAS[key].DEFAULT()

            is_possibly_match = True
            if len(self.contacts) != len(default_via.contacts):
                is_possibly_match = False
            if len(self.metals) != len(default_via.metals):
                is_possibly_match = False
            # print(is_possibly_match)
            # print(default_via.ports)

            if is_possibly_match:
                default_ports = spira.ElementList()
                for e in default_via.elementals.flatten():
                    if isinstance(e, spira.Port):
                        if e.name != 'P_metal':
                            default_ports += e.gdslayer.node_id
                # print(default_ports)
                # print('--------------------------')

                self_ports = spira.ElementList()
                for e in self.elementals.flatten():
                    if isinstance(e, spira.Port):
                        if e.name != 'P_metal':
                            self_ports += e.gdslayer.node_id
                # print(self_ports)

                # for p1 in defa
                if set(default_ports) == set(self_ports):
                    # print('YESSSSSSSSSSSSSSSSSSSSS')
                    # print(RDD.VIAS[key].DEFAULT.__name_prefix__)
                    # self.__type__ = RDD.VIAS[key].DEFAULT.__name_prefix__
                    self.__type__ = key

                # print('')



        for key in RDD.DEVICES.keys:
            # print(key)
            default_via = RDD.DEVICES[key].PCELL()
            is_possibly_match = True

            if len(self.contacts) != len(default_via.contacts):
                is_possibly_match = False
            if len(self.merged_layers) != len(default_via.metals):
                is_possibly_match = False
            # print(is_possibly_match)

            if is_possibly_match:
                default_ports = spira.ElementList()
                for e in default_via.elementals.flatten():
                    if isinstance(e, spira.Port):
                        if e.name != 'P_metal':
                            default_ports += e.gdslayer.node_id
                # print(default_ports)
                # print('--------------------------')

                self_ports = spira.ElementList()
                for e in self.elementals.flatten():
                    if isinstance(e, spira.Port):
                        if e.name != 'P_metal':
                            self_ports += e.gdslayer.node_id
                # print(self_ports)

                # # for p1 in defa
                # if set(default_ports) != set(self_ports):
                #     is_possibly_match = False

            if is_possibly_match:
                default_ports = spira.ElementList()
                for e in default_via.contacts:
                    # print(e.player)
                    default_ports += e.player

                # print('--------------------------')

                self_ports = spira.ElementList()
                for e in self.contacts:
                    # print(e.player)
                    self_ports += e.player

                if set(default_ports) != set(self_ports):
                    is_possibly_match = False

            if is_possibly_match:
                # print('YESSSSSSSSSSSSSSSSSSSSS')
                self.__type__ = key
            # print('')