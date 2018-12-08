import spira
from spira import RDD
from spira.default.templates import ViaTemplate


from spira.lpe.structure import ComposeMLayers
from spira.lpe.structure import ComposeNLayer
class ViaPCell(spira.Cell):

    def create_elementals(self, elems):
        points = [[[0,0], [3,0], [3,1], [0,1]]]
        ply0 = spira.Polygons(polygons=points, gdslayer=RDD.BAS.LAYER)
        ply1 = spira.Polygons(polygons=points, gdslayer=RDD.COU.LAYER)
        ply2 = spira.Polygons(polygons=points, gdslayer=RDD.BC.LAYER)

        el1 = spira.ElementList()
        el2 = spira.ElementList()
        el3 = spira.ElementList()

        el1 += ply0
        el2 += ply1
        el3 += ply2

        elems += spira.SRef(ComposeMLayers(cell_elems=el1))
        elems += spira.SRef(ComposeMLayers(cell_elems=el2))
        elems += spira.SRef(ComposeNLayer(cell_elems=el3))
        return elems


via = ViaPCell()

ViaTemplate().create_elementals(elems=via.elementals)

via.construct_gdspy_tree()

