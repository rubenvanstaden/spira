import spira.all as spira


class RouteExample(spira.Cell):

    layer = spira.LayerParameter(default=spira.RDD.PLAYER.M1.METAL, doc='Layer to be used when creating the route object.')
    
    @spira.cache()
    def get_io_ports(self):
        p1 = spira.Port(name='P1', midpoint=(0,0), orientation=180, process=self.layer.process)
        p2 = spira.Port(name='P2', midpoint=(20,10), orientation=0, process=self.layer.process)
        return [p1, p2]

    def create_elements(self, elems):
        ports = self.get_io_ports()
        elems += spira.RouteManhattan(ports=ports, layer=self.layer)
        return elems

    def create_ports(self, ports):
        ports += self.get_io_ports()
        return ports


D = RouteExample()
D.gdsii_view()
D.gdsii_output(file_name='Route')

