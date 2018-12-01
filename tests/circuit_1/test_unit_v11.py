'''
Module showing how doctests can be included with source code
Each '>>>' line is run as if in a python shell, and counts as a test.
The next line, if not '>>>' is the expected output of the previous line.
If anything doesn't match exactly (including trailing spaces), the test fails.
'''

import yuna
import os
import gdspy
import pytest


@pytest.fixture(scope='module')
def geometry():
    basedir = os.getcwd() + '/tests/data' + '/unit_v11'

    return yuna.grand_summon('unit', 'OneBit', 'pdf', basedir)

def test_user_labels(geometry):
    """
    Test the number of user label before filtering.
    This is the original amount of components detected. 
    """

    from yuna.masternodes.capacitor import Capacitor
    from yuna.masternodes.terminal import Terminal

    num_caps = 0
    for label in geometry.labels:
        if isinstance(label, Capacitor):
            num_caps += 1
    assert num_caps == 1

    num_terms = 0
    for label in geometry.labels:
        if isinstance(label, Terminal):
            num_terms += 1
    assert num_terms == 4


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
    assert num_vias == 1

    num_ntrons = 0
    for label in geometry.labels:
        if isinstance(label, mn.ntron.Ntron):
            num_ntrons += 1
    assert num_ntrons == 2


def test_NbN_polygons(geometry):
    """
    Get the number of polygons in the NbN mask.
    Only testing for Path and Ntron masks.
    """

    layer = 5

    num_nbn_path = 0
    num_nbn_ntron = 0

    for datatype, polygon in geometry.polygons[layer].items():
        if datatype == 0:
            for pp in polygon:
                num_nbn_path += 1
        elif datatype == 7:
            for pp in polygon:
                num_nbn_ntron += 1

    # TODO: This should be 4, change the layout.
    assert num_nbn_path == 4
    assert num_nbn_ntron == 2


def test_Al_polygons(geometry):
    """
    Get the number of polygons in the NbN mask.
    Only testing for Path and Via masks.
    """

    layer = 4

    num_al_path = 0
    num_al_via = 0

    for datatype, polygon in geometry.polygons[layer].items():
        if datatype == 0:
            for pp in polygon:
                num_al_path += 1
        elif datatype == 1:
            for pp in polygon:
                num_al_via += 1

    assert num_al_path == 1
    assert num_al_via == 1


def test_masks(geometry):
    """
    Make sure both NbN and Al layers are parsed 
    into Masks. 
    
    Note
    ----
    Al has one Via and Path. 
    NbN has one Via, Path and Ntron.
    """

    assert list(geometry.maskset.keys()) == [4, 5]
    assert len(geometry.maskset[4]) == 2
    assert len(geometry.maskset[5]) == 3

