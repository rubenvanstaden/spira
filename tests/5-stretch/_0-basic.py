import spira.all as spira
from spira.yevon.geometry import shapes
from spira.yevon.geometry.coord import Coord
from spira.yevon.rdd import get_rule_deck
from spira.yevon.geometry.bbox_info import bbox_info_cell


RDD = get_rule_deck()


def test_polygon():
    p = spira.Cross(layer=RDD.PLAYER.M1.METAL)
    p.stretch_port(port=p.ports['M1_e3'], destination=(0, 20))
    cell = spira.Cell(name='StretchPolygon', elementals=p)
    cell.output()


def test_cell():

    p1 = spira.Cross(layer=RDD.PLAYER.M1.METAL)
    p2 = spira.Wedge(layer=RDD.PLAYER.M2.METAL)

    D = spira.Cell(name='Device', elementals=[p1, p2])

    F= D.flat_expand_transform_copy()

    E = F.stretch_port(port=F.ports['COU_e6_Device_0'], destination=(50, 0))
    # E = F.stretch_port(port=D.bbox_info.ports['BBOX_e1'], destination=(50, 0))

    cell = spira.Cell(name='StretchCell')
    cell += spira.SRef(reference=E)
    cell.output()


def test_reference():
    
    p1 = spira.Cross(layer=RDD.PLAYER.M1.METAL)
    p2 = spira.Wedge(layer=RDD.PLAYER.M2.METAL)

    D = spira.Cell(name='Device', elementals=[p1, p2])

    S = spira.SRef(reference=D)

    F = S.flat_expand_transform_copy()

    E = F.stretch_port(port=F.ports['M1_e2'], destination=(50, 0))

    cell = spira.Cell(name='StretchCell', elementals=E)
    cell.output()


def test_reference_manual():

    p1 = spira.Cross(layer=RDD.PLAYER.M1.METAL)
    p2 = spira.Wedge(layer=RDD.PLAYER.M2.METAL)
    
    # p1 = spira.Cross(layer=spira.Layer(name='wewef', number=1, datatype=9))
    # p2 = spira.Wedge(layer=spira.Layer(2))
    # print(p1)

    D1 = spira.Cell(name='Device', elementals=p1)
    D2 = spira.Cell(name='SubDevice', elementals=p2)

    D1 += spira.SRef(D2)

    S = spira.SRef(reference=D1)

    # # NOTE: Stretch entire reference structure.
    # E = S.stretch(factor=(3,1))

    # # NOTE: Stretch a specific polygon.
    # F = S.flat_expand_transform_copy()
    # E = F.stretch_port(port=F.ports['M1_e2'], destination=(50, 0))

    # # NOTE: Stretch the entire reference using the bounding box ports.
    # F = S.flat_expand_transform_copy()
    # print(D1.bbox_info.ports)
    # E = F.stretch_port(port=D1.bbox_info.ports['layer0_e1'], destination=(50, 0))
    # # E = F.stretch_port(port=D1.bbox_info.ports['BBOX_e1'], destination=(50, 0))

    cell = spira.Cell(name='StretchCell')
    # cell += E
    # cell += F
    cell += S
    cell.output()


if __name__ == '__main__':

    # test_polygon()
    # test_cell()
    # test_reference()
    test_reference_manual()
