import spira
from spira import param
from spira import pc
from spira.lpe.structure import Structure


RDD = spira.get_rule_deck()


class ViaTemplate(spira.Cell):

    layer1 = param.LayerField(number=3)
    layer2 = param.LayerField(number=8)
    via_layer = param.LayerField(number=9)

    def create_elementals(self, elems):
        M1 = spira.ElementList()
        M2 = spira.ElementList()

        for e in elems:
            if e.ps_layer.purpose == RDD.PURPOSE.METAL:
                if e.ps_layer.layer == self.layer1:
                    M1 += e
                elif e.ps_layer.layer == self.layer2:
                    M2 += e

            if e.ps_layer.purpose in [RDD.PURPOSE.PRIM.VIA, RDD.PURPOSE.PRIM.JUNCTION]:
                if e.ps_layer.layer == self.via_layer:
                    for M in M1:
                        ll = spira.Layer(
                            number=M.ps_layer.layer.number,
                            datatype=e.ps_layer.purpose.datatype
                        )
                        # if e.polygon | M.polygon:
                        if e.polygon & M.polygon:
                            prev_port = e.ports[0]
                            e.ports[0] = spira.Port(
                                name=e.name,
                                midpoint=prev_port.midpoint,
                                orientation=prev_port.orientation,
                                # gds_layer=M.ps_layer.layer
                                gds_layer=ll
                            )

                    for M in M2:
                        ll = spira.Layer(
                            number=M.ps_layer.layer.number,
                            datatype=e.ps_layer.purpose.datatype
                        )
                        # if e.polygon | M.polygon:
                        if e.polygon & M.polygon:
                            prev_port = e.ports[1]
                            e.ports[1] = spira.Port(
                                name=e.name,
                                midpoint=prev_port.midpoint,
                                orientation=prev_port.orientation,
                                # gds_layer=M.ps_layer.layer
                                gds_layer=ll
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
                elems += pc.Box(name=alias, ps_layer=pl, center=poly.center, w=poly.dx, h=poly.dy, level=self.level)
            else:
                alias = 'ply_{}_{}_{}'.format(pl.layer.number, self.cell.node_id, i)
                elems += pc.Polygon(name=alias, ps_layer=pl, points=e.polygons, level=self.level)
        return elems

    def create_metals(self, elems):
        # for ps_layer in RDD.PLAYER.get_physical_layers(purposes='METAL'):
        for ps_layer in RDD.PLAYER.get_physical_layers(purposes=['METAL', 'GND']):
            for e in self.generate_physical_polygons(ps_layer):
                elems += e
        return elems

    def create_contacts(self, elems):
        for ps_layer in RDD.PLAYER.get_physical_layers(purposes=['VIA', 'JJ']):
            for e in self.generate_physical_polygons(ps_layer):
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

            # print(key)
            # print(self.contacts)
            # print('-------------------')
            # print(default_via.contacts)

            is_possibly_match = True
            if len(self.contacts) != len(default_via.contacts):
                is_possibly_match = False
            # if len(self.metals) != len(default_via.metals):
            if len(self.merged_layers) != len(default_via.merged_layers):
                is_possibly_match = False

            if is_possibly_match:
                default_ports = spira.ElementList()
                for e in default_via.elementals.flatten():
                    if isinstance(e, spira.Port):
                        if e.name != 'P_metal':
                            default_ports += e.gds_layer.node_id

                self_ports = spira.ElementList()
                for e in self.elementals.flatten():
                    if isinstance(e, spira.Port):
                        if e.name != 'P_metal':
                            # print(e)
                            self_ports += e.gds_layer.node_id
                if set(default_ports) == set(self_ports):
                    self.__type__ = key
            # print('')

        for key in RDD.DEVICES.keys:
            default_via = RDD.DEVICES[key].PCELL()
            is_possibly_match = True

            # print(key)
            # print(self.contacts)
            # print('--------------')
            # print(default_via.contacts)

            if len(self.contacts) != len(default_via.contacts):
                is_possibly_match = False
            if len(self.merged_layers) != len(default_via.merged_layers):
                is_possibly_match = False

            # FIXME: Only works for AiST process.
            # if is_possibly_match:
            #     for m1 in self.merged_layers:
            #         same_shape = False
            #         for m2 in default_via.merged_layers:
            #             if m1.polygon.count == m2.polygon.count:
            #                 same_shape = True
            #         if same_shape is False:
            #             is_possibly_match = False

            if is_possibly_match:
                default_ports = spira.ElementList()
                for e in default_via.elementals.flatten():
                    if isinstance(e, spira.Port):
                        if e.name != 'P_metal':
                            default_ports += e.gds_layer.node_id

                self_ports = spira.ElementList()
                for e in self.elementals.flatten():
                    if isinstance(e, spira.Port):
                        if e.name != 'P_metal':
                            self_ports += e.gds_layer.node_id

            if is_possibly_match:
                default_ports = spira.ElementList()
                for e in default_via.contacts:
                    default_ports += e.ps_layer

                self_ports = spira.ElementList()
                for e in self.contacts:
                    self_ports += e.ps_layer

                if set(default_ports) != set(self_ports):
                    is_possibly_match = False

            if is_possibly_match:
                self.__type__ = key

