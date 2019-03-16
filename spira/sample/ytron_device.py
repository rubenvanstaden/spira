import spira
from spira import param, shapes


class YtronPCell(spira.Device):

    sy = param.DataField(fdef_name='create_ytron_shape')

    def create_ytron_shape(self):
        return shapes.YtronShape(rho=1*self.um)

    def create_elementals(self, elems):
        # ply = spira.Polygons(shape=self.sy, gds_layer=RDD.M6.LAYER)
        ply = spira.Polygons(shape=self.sy, gds_layer=spira.Layer(number=9, datatype=10))
        elems += ply
        return elems

    # def create_ports(self, ports):
    #     ports += spira.Term(midpoint=self.sy.arm_x_left) 
    #     return ports


if __name__ == '__main__':

    D = YtronPCell()
    D.output()