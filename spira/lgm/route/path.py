import spira
import gdspy
from spira import param
from spira.lgm.shapes.shape import __Shape__, Shape


class __Path__(gdspy.Path, Shape):

    width = param.FloatField(default=1)
    initial_point = param.PointField()
    number_of_paths = param.IntegerField(default=1)
    distance = param.FloatField(default=0)

    def __init__(self, **kwargs):

        Shape.__init__(self, **kwargs)
        gdspy.Path.__init__(self,
            width=self.width,
            initial_point=self.initial_point,
            number_of_paths=self.number_of_paths,
            distance=self.distance
        )

    def __repr__(self):
        if self is None:
            return 'Path is None!'
        return ("[SPiRA: Path] (width {}, distance {})").format(self.width, self.distance)

    def __str__(self):
        return self.__repr__()


class PathShape(__Path__):

    def create_points(self, points):
        return self.polygons


def Path(shape):
    return spira.Polygons(shape=shape.points)












