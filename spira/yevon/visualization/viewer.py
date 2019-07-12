import spira.all as spira
from spira.yevon.geometry import shapes
from spira.core.parameters.descriptor import Parameter
from spira.yevon.process.physical_layer import PLayer
from spira.yevon.process import get_rule_deck
from spira.yevon.geometry.vector import transformation_from_vector


RDD = get_rule_deck()


__all__ = ['PortLayout']


class PortLayout(spira.Cell):
    """  """

    port = spira.PortParameter()

    edge = Parameter(fdef_name='create_edge')
    arrow = Parameter(fdef_name='create_arrow')
    label = Parameter(fdef_name='create_label')

    def create_edge(self):
        dw = self.port.width
        dl = self.port.length/10
        layer = PLayer(process=self.port.process, purpose=self.port.purpose)
        p = spira.Box(width=dw, height=dl, layer=layer)
        # T = transformation_from_vector(self.port) + spira.Rotation(-90)
        T = transformation_from_vector(self.port) + spira.Rotation(rotation=-90, rotation_center=self.port.midpoint)
        p.transform(T)
        return p

    def create_arrow(self):
        layer = PLayer(self.port.process, RDD.PURPOSE.PORT.DIRECTION)
        # w = self.port.length * 3
        w = 0.01
        # l = 2
        # l = self.port.length * 3
        l = 0.2
        arrow_shape = shapes.ArrowShape(width=w, length=l, head=l*0.2)
        p = spira.Polygon(shape=arrow_shape, layer=layer, enable_edges=False)
        T = transformation_from_vector(self.port)
        p.transform(T)
        return p

    def create_label(self):
        # enabled_purposes = (RDD.PURPOSE.PORT.INSIDE_EDGE_ENABLED, RDD.PURPOSE.PORT.OUTSIDE_EDGE_ENABLED)
        # disabled_purposes = (RDD.PURPOSE.PORT.INSIDE_EDGE_DISABLED, RDD.PURPOSE.PORT.OUTSIDE_EDGE_DISABLED)
        # if self.port.purpose in enabled_purposes:
        #     layer = PLayer(self.port.process, RDD.PURPOSE.PORT.TEXT_ENABLED)
        # elif self.port.purpose is disabled_purposes:
        #     layer = PLayer(self.port.process, RDD.PURPOSE.PORT.TEXT_DISABLED)
        # else:
        #     layer = PLayer(self.port.process, RDD.PURPOSE.TEXT)
        purpose = RDD.PURPOSE.TEXT[self.port.purpose.symbol+'T']
        layer = PLayer(self.port.process, purpose)
        return spira.Label(
            position=self.port.midpoint,
            text=self.port.name,
            orientation=self.port.orientation,
            layer=layer
        )

    def create_elements(self, elems):
        elems += self.edge
        elems += self.label
        # if not isinstance(self.port, ContactPort):
        if self.port.purpose.name != 'ContactPort':
            elems += self.arrow
        return elems

