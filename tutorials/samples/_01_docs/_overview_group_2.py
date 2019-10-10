import spira.all as spira


class GroupExample(spira.Cell):

    group_transform = spira.TransformationParameter(doc='Transform parameter for a group of elements.')

    def create_elements(self, elems):

        group = spira.Group()
        group += spira.Rectangle(p1=(0,0), p2=(10,10), layer=spira.Layer(1))
        group += spira.Rectangle(p1=(0,15), p2=(10,30), layer=spira.Layer(1))

        group.transform(self.group_transform)

        elems += group

        bbox_shape = group.bbox_info.bounding_box(margin=1)
        elems += spira.Polygon(shape=bbox_shape, layer=spira.Layer(2))

        return elems


# D = GroupExample()
D = GroupExample(group_transform=spira.Rotation(45))
D.gdsii_view()

