import spira.all as spira


class PortExample(spira.Cell):

    def create_elements(self, elems):
        elems += spira.Rectangle(p1=(0,0), p2=(20,5), layer=spira.Layer(1))
        return elems

    def create_ports(self, ports):
        ports += spira.Port(name='P1', midpoint=(0,2.5), orientation=180)
        ports += spira.Port(name='P2', midpoint=(20,2.5), orientation=0)
        return ports


D = PortExample()
D.gdsii_output()
