import spira.all as spira
from spira.yevon.geometry import shapes
from spira.core.parameters.descriptor import DataField
from spira.yevon.rdd.physical_layer import PhysicalLayer
from spira.yevon.rdd import get_rule_deck


RDD = get_rule_deck()


__all__ = ['PortLayout']


class PortLayout(spira.Cell):
    """  """

    port = spira.PortField()

    edge = DataField(fdef_name='create_edge')
    arrow = DataField(fdef_name='create_arrow')
    label = DataField(fdef_name='create_label')

    def create_edge(self):
        dw = self.port.width
        dl = self.port.length
        print(dl)
        layer = PhysicalLayer(process=self.port.process, purpose=self.port.purpose)
        p = spira.Box(width=dw, height=dl, layer=layer)
        p.center = (0,0)
        angle = self.port.orientation - 90
        T = spira.Rotation(rotation=angle)
        T += spira.Translation(self.port.midpoint)
        p.transform(T)
        return p

    def create_arrow(self):
        layer = PhysicalLayer(process=self.port.process, purpose=RDD.PURPOSE.PORT.DIRECTION)
        # arrow_shape = shapes.ArrowShape(a=self.port.length, b=self.port.length/2, c=self.port.length*2)
        w = self.port.length * 0.5
        l = 2*1e6
        arrow_shape = shapes.ArrowShape(width=w, length=l, head=l*0.3)
        p = spira.Polygon(shape=arrow_shape, layer=layer, enable_edges=False)
        # p.center = (0,0)
        angle = self.port.orientation
        T = spira.Rotation(rotation=angle)
        T += spira.Translation(self.port.midpoint)
        p.transform(T)
        # p.move(destination=(0,0.5*w))
        return p

    def create_label(self):
        # if self.locked is True:
        #     layer = self.gds_layer
        #     text_type = self.text_type
        # else:
        #     layer = self.unlocked_layer
        #     text_type = self.unlocked_layer
        layer = PhysicalLayer(process=self.port.process, purpose=RDD.PURPOSE.PORT.DIRECTION)
        lbl = spira.Label(
            position=self.port.midpoint,
            text=self.port.name,
            # text=self.alias,
            orientation=self.port.orientation,
            process=self.port.process
        )
        # lbl.__rotate__(angle=self.orientation)
        # lbl.move(midpoint=lbl.position, destination=self.midpoint)
        return lbl

    def create_elementals(self, elems):
        elems += self.edge
        elems += self.arrow
        elems += self.label
        return elems


# class PortViewer(spira.Cell):
#     """  """

#     layer = spira.Layer(default=RDD.PLAYER.PORT)
#     midpoint = CoordField(default=(0,0))
#     orientation = NumberField(default=0)

#     width = NumberField(default=2*1e6)
#     length = NumberField(default=2*1e6)

#     edge = DataField(fdef_name='create_edge')
#     # arrow = DataField(fdef_name='create_arrow')

#     def create_edge(self):
#         dw = self.width
#         dl = self.length
#         p = spira.Box(width=dw, height=dl, layer=self.layer)
#         p.center = (0,0)
#         T = spira.Rotation(rotation=self.orientation) + spira.Translation(self.midpoint)
#         p.transform(T)
#         return p


#         # # from spira.yevon.rdd.layer import PhysicalLayer
#         # # from spira.yevon.geometry import shapes
#         # dx = self.length
#         # dy = self.width - dx
#         # rect_shape = shapes.RectangleShape(p1=[0, 0], p2=[dx, dy])
#         # # if self.locked is True:
#         # #     ply = spira.Polygon(shape=rect_shape, gds_layer=self.edgelayer, enable_edges=False)
#         # # else:
#         # #     ply = spira.Polygon(shape=rect_shape, gds_layer=self.unlocked_layer, enable_edge=False)
#         # ps1 = PhysicalLayer(layer=self.edgelayer)
#         # ps2 = PhysicalLayer(layer=self.unlocked_layer)
#         # if self.locked is True:
#         #     ply = spira.Polygon(shape=rect_shape, ps_layer=ps1, enable_edges=False)
#         # else:
#         #     ply = spira.Polygon(shape=rect_shape, ps_layer=ps2, enable_edges=False)
#         # ply.center = (0,0)
#         # angle = self.orientation
#         # T = spira.Rotation(rotation=angle) + spira.Translation(self.midpoint)
#         # ply.transform(T)
#         # # ply.move_new(self.midpoint)
#         # # ply.move(midpoint=rect_shape.center_of_mass, destination=self.midpoint)
#         # return ply

#     # def create_arrow(self):
#     #     from spira.yevon.geometry import shapes
#     #     arrow_shape = shapes.ArrowShape(a=self.length, b=self.length/2, c=self.length*2)
#     #     # arrow_shape.apply_merge
#     #     ply = spira.Polygon(shape=arrow_shape, gds_layer=self.arrowlayer, enable_edges=False)
#     #     ply.center = (0,0)
#     #     angle = self.orientation - 90
#     #     T = spira.Rotation(rotation=angle) + spira.Translation(self.midpoint)
#     #     ply.transform(T)
#     #     # ply.move_new(self.midpoint)
#     #     return ply

#     def create_elementals(self, elems):
#         elems += self.edge
#         # elems += self.arrow
#         return elems

