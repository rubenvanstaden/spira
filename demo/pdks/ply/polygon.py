import spira
from spira import param
from spira import shapes
from demo.pdks.ply.base import ProcessLayer


class Polygon(ProcessLayer):

    points = param.ElementalListField()
    color = param.ColorField(default='#C0C0C0')

    # def validate_parameters(self):
    #     if self.w < self.player.data.WIDTH:
    #         return False
    #     if self.h < self.player.data.WIDTH:
    #         return False
    #     return True

    def create_layer(self):
        # print(self.level)
        # layer = spira.Layer(
        #     name=self.name,
        #     number=self.player.layer.number,
        #     datatype=self.player.layer.datatype
        # )

        if self.error != 0:
            layer = spira.Layer(
                name=self.name,
                number=self.player.layer.number,
                datatype=self.error
            )
        elif self.level != 0:
            layer = spira.Layer(
                name=self.name,
                number=self.player.layer.number,
                datatype=self.level
            )
        else:
            layer = spira.Layer(
                name=self.name,
                number=self.player.layer.number,
                datatype=self.player.layer.datatype
            )

        return layer

    def create_polygon(self):
        ply = spira.Polygons(shape=self.points, gdslayer=self.layer)
        return ply


