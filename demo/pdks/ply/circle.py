import spira
from spira import param, shapes
from demo.pdks.ply.base import ProcessLayer


class Circle(ProcessLayer):

    center = param.PointField()
    box_size = param.PointField(default=(1.0*1e6, 1.0*1e6))
    angle_step = param.FloatField(default=20)
    color = param.ColorField(default='#C0C0C0')
    points = param.DataField(fdef_name='create_points')

    def __repr__(self):
        if hasattr(self, 'elementals'):
            elems = self.elementals
            return ("[SPiRA: CirclePC(\'{}\')] " +
                    "({} elementals: {} sref, {} cells, {} polygons, " +
                    "{} labels, {} ports)").format(
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

    def __str__(self):
        return self.__repr__()

    # def validate_parameters(self):
    #     pd = self.player.data
    #     if RDD == 'MiTLL':
    #         if (self.w < pd.MIN_SIZE*1e6) or (self.w > pd.MAX_WIDTH*1e6):
    #             return False
    #         if (self.h < pd.MIN_SIZE*1e6) or (self.h > pd.MAX_WIDTH*1e6):
    #             return False
    #     else:
    #         if (self.w < pd.WIDTH) or (self.h < pd.WIDTH):
    #             return False
    #     return True

    def create_polygon(self):
        shape = shapes.CircleShape(box_size=self.box_size, angle_step=self.angle_step)
        ply = spira.Polygons(shape=shape, gdslayer=self.player.layer)
        ply.center = self.center
        return ply

    def create_points(self):
        return self.polygon.shape.points