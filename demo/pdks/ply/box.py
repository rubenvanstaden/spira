import spira
import numpy as np
from spira import param, shapes
from demo.pdks.ply.base import ProcessLayer


RDD = spira.get_rule_deck()


class Box(ProcessLayer):

    w = param.FloatField(default=1)
    h = param.FloatField(default=1)
    center = param.PointField()
    points = param.DataField(fdef_name='create_points')

    __port_compass__ = ['North', 'East', 'South', 'West']

    def __repr__(self):
        if hasattr(self, 'elementals'):
            elems = self.elementals
            return ("[SPiRA: BoxPC(\'{}\')] {} center " + 
                    "({} elementals: {} sref, {} cells, {} polygons, " +
                    "{} labels, {} ports)").format(
                        self.player.layer.number,
                        self.center,
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

    def create_edge_ports(self, edges):
        xpts = list(self.points[0][:, 0])
        ypts = list(self.points[0][:, 1])

        n = len(xpts)
        xpts.append(xpts[0])
        ypts.append(ypts[0]) 

        clockwise = 0
        for i in range(0, n):
            clockwise += ((xpts[i+1] - xpts[i]) * (ypts[i+1] + ypts[i]))

        for i in range(0, n):
            # name = self.__port_compass__[i]
            name = 'e{}'.format(i)
            x = np.sign(clockwise) * (xpts[i+1] - xpts[i])
            y = np.sign(clockwise) * (ypts[i] - ypts[i+1])
            # orientation = (np.arctan2(x, y) * 180/np.pi) + 90
            orientation = (np.arctan2(x, y) * 180/np.pi) - 90
            midpoint = [(xpts[i+1] + xpts[i])/2, (ypts[i+1] + ypts[i])/2]
            width = np.abs(np.sqrt((xpts[i+1] - xpts[i])**2 + (ypts[i+1]-ypts[i])**2))

            # orientation = (-1) * orientation

            # edges += spira.Term(
            edges += spira.EdgeTerm(
                name=name,
                gdslayer=self.layer,
                midpoint=midpoint,
                orientation=orientation,
                width=width,
                edgelayer=spira.Layer(number=65),
                arrowlayer=spira.Layer(number=78),
                local_connect=self.polygon.node_id,
                is_edge=True
            )

        return edges

    def create_polygon(self):
        shape = shapes.BoxShape(width=self.w, height=self.h)
        shape.apply_merge
        ply = spira.Polygons(shape=shape, gdslayer=self.player.layer)
        ply.center = self.center
        return ply

    def create_points(self):
        return self.polygon.shape.points

    # def create_ports(self, ports):
    #     ports = super().create_ports(ports)
    #     return ports