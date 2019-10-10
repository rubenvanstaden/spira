import spira.all as spira


class RouteExample(spira.Cell):
    
    @spira.cache()
    def get_io_ports(self):
        p1 = spira.Port(name='P1_M1', midpoint=(0,0), orientation=180)
        p2 = spira.Port(name='P2_M1', midpoint=(20,10), orientation=0)
        return [p1, p2]

    def create_elements(self, elems):
        ports = self.get_io_ports()
        elems += spira.RouteManhattan(ports=ports, layer=spira.RDD.PLAYER.M1.METAL)
        return elems

    def create_ports(self, ports):
        ports += self.get_io_ports()
        return ports


D = RouteExample()
D.gdsii_view()

