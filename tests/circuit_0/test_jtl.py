import pytest
import os
import yuna


@pytest.fixture(scope='module')
def geometry():
    basedir = os.getcwd() + '/tests/data' + '/jtl'
    return yuna.grand_summon('jtl', 'extract_sqModMN1w2l100', 'pdf', basedir)


def test_user_labels(geometry):
    """
    Test the number of user label before filtering.
    This is the original amount of components detected. 
    """

    from yuna.masternodes.terminal import Terminal

    num_terms = 0
    for label in geometry.labels:
        if isinstance(label, Terminal):
            num_terms += 1
    assert num_terms == 3


def test_cell_labels(geometry):
    """
    Test the number of cell label before filtering.
    This is the original amount of components detected. 
    """

    import yuna.masternodes as mn

    num_vias = 0
    for label in geometry.labels:
        if isinstance(label, mn.via.Via):
            num_vias += 1
    assert num_vias == 9


def test_M2_polygons(geometry):
    """
    Get the number of polygons in the NbN mask.
    Only testing for Path and Ntron masks.
    """

    layer = 6
    pnum, vnum = 0, 0
    for datatype, polygon in geometry.polygons[layer].items():
        if datatype == 0:
            for pp in polygon:
                pnum += 1
        elif datatype == 1:
            for pp in polygon:
                vnum += 1

    assert pnum == 8
    assert vnum == 9


def test_RES_polygons(geometry):
    """
    Get the number of polygons in the NbN mask.
    Only testing for Path and Via masks.
    """

    layer = 9
    pnum, vnum, jnum = 0, 0, 0
    for datatype, polygon in geometry.polygons[layer].items():
        if datatype == 0:
            for pp in polygon:
                pnum += 1
        elif datatype == 1:
            for pp in polygon:
                vnum += 1
        elif datatype == 3:
            for pp in polygon:
                jnum += 1

    assert pnum == 3
    assert vnum == 6
    assert jnum == 2


def test_MN1_polygons(geometry):
    """
    Get the number of polygons in the NbN mask.
    Only testing for Path and Via masks.
    """

    layer = 34
    pnum, vnum = 0, 0
    for datatype, polygon in geometry.polygons[layer].items():
        if datatype == 0:
            for pp in polygon:
                pnum += 1
        elif datatype == 1:
            for pp in polygon:
                vnum += 1

    assert pnum == 1
    assert vnum == 3


def test_masks(geometry):
    """
    Make sure both NbN and Al layers are parsed 
    into Masks. 
    
    Note
    ----
    M2 has Path, Via and JJ
    MN1 has Path and Via
    RES has Path, Via and JJ
    """

    # TODO: This list check has to be ordered. Change this.
    assert list(geometry.maskset.keys()) == [6, 34, 9]
    assert len(geometry.maskset[6]) == 3
    assert len(geometry.maskset[34]) == 2
    assert len(geometry.maskset[9]) == 3