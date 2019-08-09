import spira.all as spira


class GroupExample(spira.Cell):

    def create_elements(self, elems):

        group = spira.Group()
        group += spira.Rectangle(p1=(0,0), p2=(10,10), layer=spira.Layer(1))
        group += spira.Rectangle(p1=(0,15), p2=(10,30), layer=spira.Layer(1))

        group.rotate(30)

        elems += group

        bbox_shape = group.bbox_info.bounding_box(margin=1)
        elems += spira.Polygon(shape=bbox_shape, layer=spira.Layer(2))

        return elems


D = GroupExample()
D.gdsii_view()

