import spira.all as spira
from spira.yevon.geometry import shapes
from spira.yevon.geometry.coord import Coord
from spira.yevon.rdd import get_rule_deck
from spira.yevon.geometry.bbox_info import bbox_info_cell


RDD = get_rule_deck()


def test_polygon():
    p = spira.Cross(ps_layer=RDD.PLAYER.COU)
    # ply = spira.Wedge(ps_layer=RDD.PLAYER.COU)
    # ply = spira.Parabolic(ps_layer=RDD.PLAYER.RC)

    # ply = ply.stretch_port(port=ply.ports['COU_e6'], destination=(20*1e6, 0))
    p.stretch_port(port=p.ports['COU_e3'], destination=(0*1e6, 20*1e6))
    # ply = ply.stretch_port(port=ply.ports['COU_e1'], destination=(0*1e6, 10*1e6))

    cell = spira.Cell(name='StretchPolygon', elementals=p)
    cell.output()


def test_cell():

    p1 = spira.Cross(ps_layer=RDD.PLAYER.COU)
    p2 = spira.Wedge(ps_layer=RDD.PLAYER.BAS)

    D = spira.Cell(name='Device', elementals=[p1, p2])

    F= D.flat_expand_transform_copy()

    E = F.stretch_port(port=F.ports['COU_e6_Device_0'], destination=(50*1e6, 0))
    # E = F.stretch_port(port=D.bbox_info.ports['BBOX_e1'], destination=(50*1e6, 0))

    cell = spira.Cell(name='StretchCell')
    cell += spira.SRef(reference=E)
    cell.output()


def test_reference():
    
    p1 = spira.Cross(ps_layer=RDD.PLAYER.COU)
    p2 = spira.Wedge(ps_layer=RDD.PLAYER.BAS)

    D = spira.Cell(name='Device', elementals=[p1, p2])

    S = spira.SRef(reference=D)

    F = S.flat_expand_transform_copy()
    # debug_view(E.ref)

    E = F.stretch_port(port=F.ports['BAS_e2'], destination=(50*1e6, 0))

    cell = spira.Cell(name='StretchCell', elementals=E)
    cell.output()


def test_reference_manual():

    p1 = spira.Cross(ps_layer=RDD.PLAYER.COU)
    p2 = spira.Wedge(ps_layer=RDD.PLAYER.BAS)

    D1 = spira.Cell(name='Device', elementals=p1)
    D2 = spira.Cell(name='SubDevice', elementals=p2)

    D1 += spira.SRef(D2)

    S = spira.SRef(reference=D1)

    # # NOTE: Stretch entire reference structure.
    # E = S.stretch(factor=(3,1))

    F = S.flat_expand_transform_copy()

    # NOTE: Stretch a specific polygon.
    E = F.stretch_port(port=F.ports['BAS_e2'], destination=(50*1e6, 0))

    # NOTE: Stretch the entire reference using the bounding box ports.
    # E = F.stretch_port(port=D.bbox_info.ports['BBOX_e1'], destination=(50*1e6, 0))

    cell = spira.Cell(name='StretchCell')
    # cell += E
    cell += S
    cell.output()


if __name__ == '__main__':

    test_polygon()
    # test_cell()
    # test_reference()
    # test_reference_manual()
