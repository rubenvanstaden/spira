import spira
from spira import param
from spira import shapes
from demo.pdks.ply.base import ProcessLayer


class Box(ProcessLayer):

    w = param.FloatField(default=1)
    h = param.FloatField(default=1)
    center = param.PointField()
    color = param.ColorField(default='#C0C0C0')

    def __repr__(self):
        if hasattr(self, 'elementals'):
            elems = self.elementals
            return ("[SPiRA: BoxPC(\'{}\')] " +
                    "({} elementals: {} sref, {} cells, {} polygons, " +
                    "{} labels, {} ports)").format(
                        # self.name,
                        self.player.layer.number,
                        elems.__len__(),
                        elems.sref.__len__(),
                        elems.cells.__len__(),
                        elems.polygons.__len__(),
                        elems.labels.__len__(),
                        self.ports.__len__()
                    )
        else:
            return "[SPiRA: Cell(\'{}\')]".format(self.__class__.__name__)

    # FIXME: Has to be placed here for deepcopy().
    def __str__(self):
        return self.__repr__()

    def validate_parameters(self):
        if self.w < self.player.data.WIDTH:
            return False
        if self.h < self.player.data.WIDTH:
            return False
        return True

    def create_layer(self):
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
        shape = shapes.BoxShape(center=self.center, width=self.w, height=self.h)
        ply = spira.Polygons(shape=shape, gdslayer=self.player.layer)
        return ply

