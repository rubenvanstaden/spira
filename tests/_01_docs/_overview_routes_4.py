import spira.all as spira


class RouteExample(spira.Cell):

    layer = spira.LayerParameter(default=spira.RDD.PLAYER.M1.METAL, doc='Layer to be used when creating the route object.')

    p1 = spira.Parameter(fdef_name='create_p1')
    p2 = spira.Parameter(fdef_name='create_p2')
    
    def create_p1(self):
        return spira.Port(name='P1', midpoint=(0,0), orientation=180, process=self.layer.process)

    def create_p2(self):
        return spira.Port(name='P2', midpoint=(20,10), orientation=0, process=self.layer.process)
 
    def create_elements(self, elems):
        elems += spira.RouteManhattan(ports=[self.p1, self.p2], layer=self.layer)
        return elems

    def create_ports(self, ports):
        ports += self.p1
        ports += self.p2
        return ports


D = RouteExample()
D.gdsii_view()

