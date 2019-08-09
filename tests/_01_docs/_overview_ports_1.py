import spira.all as spira
from spira.yevon.geometry import shapes


class BoxDevice(spira.Cell):

    width = spira.NumberParameter(default=1)
    height = spira.NumberParameter(default=1)
    layer = spira.LayerParameter(default=spira.Layer(1))

    def create_elements(self, elems):
        shape = shapes.BoxShape(width=self.width, height=self.height)
        elems += spira.Polygon(shape=shape, layer=self.layer)
        return elems

    def create_ports(self, ports):
        ports += spira.Port(name='P1', midpoint=(-0.5,0), orientation=180, width=1)
        ports += spira.Port(name='P2', midpoint=(0.5,0), orientation=0, width=1)
        return ports


D = BoxDevice()
D.gdsii_view()

