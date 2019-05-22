import spira.all as spira
from spira.yevon.geometry import shapes
from spira.yevon.geometry.coord import Coord
from spira.yevon.rdd import get_rule_deck


RDD = get_rule_deck()


def debug_view(cell):
    D = cell.flat_expand_transform_copy()
    print('\n---------------------------------')
    print('[*] List of Ports:')
    print(D.ports)
    print('---------------------------------\n')
    D.output()


def test_polygon():
    ply = spira.Cross(ps_layer=RDD.PLAYER.COU)
    # ply = spira.Wedge(ps_layer=RDD.PLAYER.COU)
    # ply = spira.Parabolic(ps_layer=RDD.PLAYER.RC)

    # ply = ply.stretch_port(port=ply.ports['COU_e6'], destination=(20*1e6, 0))
    ply = ply.stretch_port(port=ply.ports[' COU_e3'], destination=(0*1e6, 20*1e6))
    # ply = ply.stretch_port(port=ply.ports['COU_e1'], destination=(0*1e6, 10*1e6))

    cell = spira.Cell(name='StretchPolygon')
    cell += ply
    cell.output()


def test_cell():

    D = spira.Cell(name='Device')
    p1 = spira.Cross(ps_layer=RDD.PLAYER.COU)
    p2 = spira.Wedge(ps_layer=RDD.PLAYER.BAS)
    D += p1
    D += p2

    # D = D.stretch_port(port=D.ports['COU_e6_Device_0_(T (0.0,0.0), R 0.0, RF=False, M=1.0)_2'], destination=(20*1e6, 0))

    E = D.flat_expand_transform_copy()
    # print(D.ports)
    # print(E.ports['COU_e6_Device_0'])
    # print(E.ports['COU_e6_Device_0'].local_pid)
    # print('-----')

    newCell = E.stretch_port(port=E.ports['COU_e6_Device_0'], destination=(50*1e6, 0))
    # newCell = E.stretch_port(port=D.bbox_info.ports['BBOX_e1'], destination=(50*1e6, 0))

    cell = spira.Cell(name='StretchCell')
    # cell += spira.SRef(reference=D)
    cell += spira.SRef(reference=newCell)
    cell.output()
    # debug_view(cell=cell)


def test_reference():

    D = spira.Cell(name='Device')
    p1 = spira.Cross(ps_layer=RDD.PLAYER.COU)
    p2 = spira.Wedge(ps_layer=RDD.PLAYER.BAS)
    D += p1
    D += p2

    S = spira.SRef(reference=D)

    E = S.flat_expand_transform_copy()
    # debug_view(E.ref)
    print(E.ports)
    print(E.ports['BAS_e2'])

    newCell = E.stretch_port(port=E.ports['BAS_e2'], destination=(50*1e6, 0))
    # # newCell = E.stretch_port(port=D.bbox_info.ports['BBOX_e1'], destination=(50*1e6, 0))

    cell = spira.Cell(name='StretchCell')
    # cell += spira.SRef(reference=D)
    # cell += spira.SRef(reference=newCell)
    cell += newCell
    cell.output()
    # debug_view(cell=cell)


def test_reference_manual():

    D = spira.Cell(name='Device')
    p1 = spira.Cross(ps_layer=RDD.PLAYER.COU)
    p2 = spira.Wedge(ps_layer=RDD.PLAYER.BAS)
    D += [p1, p2]

    S = spira.SRef(reference=D)

    T = spira.Stretch(stretch_factor=(5,1))
    E = S.stretch(T)

    # E = S.flat_expand_transform_copy()
    # # print(E.ports)
    # print(E.ports['BAS_e2'])

    # T = spira.Stretch(stretch_factor=(5,1))
    # # T = spira.Stretch(stretch_factor=(1,5), stretch_center=E.ports['BAS_e0'])
    # print(T)
    # print(E)
    # E = T.apply(E)
    # print(E)
    # # newCell = T(E)

    # newCell = E.stretch_port(port=E.ports['BAS_e2'], destination=(50*1e6, 0))
    # # newCell = E.stretch_port(port=D.bbox_info.ports['BBOX_e1'], destination=(50*1e6, 0))

    cell = spira.Cell(name='StretchCell')
    # cell += newCell
    cell += E
    cell.output()


if __name__ == '__main__':

    # test_polygon()
    # test_cell()
    # test_reference()
    test_reference_manual()
