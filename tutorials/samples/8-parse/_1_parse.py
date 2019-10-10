import os
from spira.technologies.mit.process import RDD
import spira.all as spira
import spira.yevon.io.input_gdsii as io
from copy import copy, deepcopy


def wrap_references(cell, c2dmap, devices):
    """  """
    for e in cell.elements.sref:
        if e.reference in c2dmap.keys():
            e.reference = c2dmap[e.reference]
    return cell


def device_detector(cell):
    """
    We are working with the presupposition that JJ cells
    are flattend. Future versions can automate this process.
    """

    c2dmap, devices = {}, {}

    for c in cell.dependencies():
        c2dmap.update({c: c})

    for c in cell.dependencies():

        cc = deepcopy(c)

        # FIXME: Seems like there is a lack of
        # transformations in the parsed cells.
        # D = spira.Cell(elements=cc.elements).flat_copy()
        # elems = RDD.FILTERS.PCELL.DEVICE(D).elements
        # c.elements = elems
        # c.elements = D.elements

        cell_types = {0: 'JUNCTION', 1: 'VIA'}

        _type = None

        for p in cc.elements:
            if p.alias == 'J5':
                _type = cell_types[0]

        for key in RDD.VIAS.keys:
            # via_layer = RDD.VIAS[key].LAYER_STACK['VIA_LAYER']
            for p in cc.elements:
                if p.alias == key:
                    pcell = RDD.VIAS[key].PCELLS.DEFAULT

                    D = spira.Cell(elements=deepcopy(cc).elements.flat_copy())
                    elems = RDD.FILTERS.PCELL.DEVICE(D).elements

                    D = pcell(elements=elems)

                    c2dmap[c] = D

        for key in RDD.DEVICES.keys:

            if _type == key:
                pcell = RDD.DEVICES[key].PCELLS.DEFAULT

                D = spira.Cell(elements=deepcopy(cc).elements.flat_copy())
                elems = RDD.FILTERS.PCELL.DEVICE(D).elements

                D = pcell(elements=elems)

                c2dmap[c] = D

    for c in cell.dependencies():
        wrap_references(c, c2dmap, devices)

    return cell


if __name__ == '__main__':

    # file_name = '/home/therealtyler/code/phd/spira/tests/8-parse/jj_mitll.gds'
    # file_name = '/home/therealtyler/code/phd/spira/tests/8-parse/mit/ruben/jtl_mitll_diff.gds'
    # file_name = '/home/therealtyler/code/phd/spira/tests/8-parse/mit/lieze/jtl.gds'
    file_name = '/home/therealtyler/code/phd/spira/tests/8-parse/mit/lieze/ptlrx.gds'
    # file_name = '/home/therealtyler/code/phd/spira/tests/8-parse/mit/lieze/dfft.gds'
    # file_name = '/home/therealtyler/code/phd/spira/tests/8-parse/mit/lieze/circuit.gds'
    # file_name = '/home/therealtyler/code/phd/spira/tests/8-parse/mit/lieze/jtlt.gds'

    # input_gdsii = spira.InputGdsii(file_name=file_name)
    # input_gdsii.layer_map = RDD.GDSII.IMPORT_LAYER_MAP

    input_gdsii = spira.InputGdsii(file_name=file_name, layer_map=RDD.GDSII.IMPORT_LAYER_MAP)
    D = input_gdsii.parse()

    # NOTE: Parse the input layout to SPiRA elements.
    D = device_detector(cell=D)

    D = RDD.FILTERS.PCELL.CIRCUIT(D)

    C = spira.Circuit(elements=D.elements)

    D = RDD.FILTERS.PCELL.MASK(C)

    # from spira.yevon.vmodel.virtual import virtual_connect
    # v_model = virtual_connect(device=D)
    # v_model.view_virtual_connect(show_layers=True, write=True)

    D.gdsii_view()

    net = D.extract_netlist

    D.netlist_view(net=net)


    # FIXME: Add ports to layouts for i/o.


