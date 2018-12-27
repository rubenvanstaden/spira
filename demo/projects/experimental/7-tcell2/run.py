import spira
from spira import RDD
from spira import param
from spira import shapes
from spira.core.default.templates import ViaTemplate
from spira.lpe.primitives import Device


class ViaPCell(spira.Cell):

    spacing = param.FloatField(default=RDD.BC.SPACING)

    def create_elementals(self, elems):

        ply_elems = spira.ElementList()

        s1 = shapes.BoxShape(center=(0,0),
                               width=RDD.BAS.WIDTH,
                               height=RDD.BAS.WIDTH,
                               gdslayer=RDD.BAS.LAYER)
        ply_elems += shapes.Box(shape=s1)
        s2 = shapes.BoxShape(center=(0,0),
                               width=RDD.COU.WIDTH,
                               height=RDD.COU.WIDTH,
                               gdslayer=RDD.COU.LAYER)
        ply_elems += shapes.Box(shape=s2)
        s3 = shapes.BoxShape(center=(0,0),
                               width=RDD.BAS.WIDTH - self.spacing,
                               height=RDD.BAS.WIDTH - self.spacing,
                               gdslayer=RDD.BC.LAYER)
        ply_elems += shapes.Box(shape=s3)

        for ply in ply_elems:
            elems += ply

        # elems += spira.SRef(Device(cell_elems=ply_elems))

        return elems


# ----------------------------------------------------------------------


via = ViaPCell()

# ViaTemplate().create_elementals(elems=via.elementals)

via.output()




