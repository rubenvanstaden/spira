import spira.all as spira


class GroupExample(spira.Cell):

    def create_elements(self, elems):

        group = spira.Group()
        # group += spira.Rectangle(p1=(0,0), p2=(10,10), layer=spira.Layer(1))
        # group += spira.Rectangle(p1=(0,15), p2=(10,30), layer=spira.Layer(1))
        group += spira.Rectangle(p1=(0,0), p2=(10,10), layer=spira.RDD.PLAYER.M1.METAL)
        group += spira.Rectangle(p1=(0,15), p2=(10,30), layer=spira.RDD.PLAYER.M1.METAL)

        group.transform(spira.Rotation(-45))

        elems += group

        bbox_shape = group.bbox_info.bounding_box(margin=1)
        # elems += spira.Polygon(shape=bbox_shape, layer=spira.Layer(2))
        elems += spira.Polygon(shape=bbox_shape, layer=spira.RDD.PLAYER.M2.METAL)

        return elems


D = GroupExample()
D.gdsii_view()
D.gdsii_output(file_name='bbox')

