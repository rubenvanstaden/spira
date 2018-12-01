import os
import spira
import gdspy
import pathlib 
import numpy as np
from spira.kernel.utils import c3d


def current_path(filename):
    return '{}/{}.gds'.format(os.getcwd(), filename)


def debug_path(filename):
    debug_dir = os.getcwd() + '/debug/'
    pathlib.Path(debug_dir).mkdir(parents=True, exist_ok=True)
    path = debug_dir + filename + '.gds'
    return path


def wrap_labels(cell, c2dmap):
    for l in cell.get_labels():
        D = c2dmap[cell]
        if isinstance(l, gdspy.Label):
            layer = spira.Layer(name='', number=l.layer)
            params = {}
            params['text'] = l.text
            params['gdslayer'] = layer
            params['str_anchor'] = l.anchor

            lbl = spira.Label(position=l.position, **params)
            lbl.scale_up()
            D += lbl


def wrap_references(cell, c2dmap):
    for e in cell.elements:
        if isinstance(e, gdspy.CellReference):
            D = c2dmap[cell]
            ref_device = c2dmap[e.ref_cell]
            D += spira.SRef(structure=ref_device,
                            origin=c3d(e.origin),
                            rotation=e.rotation,
                            magnification=e.magnification,
                            x_reflection=e.x_reflection)


def create_spira_cell(cell):
    if cell.name.startswith('jj'):
        D = spira.Junction(name=cell.name)
    elif cell.name.startswith('via'):
        D = spira.Via(name=cell.name)
    else:
        D = spira.Cell(name=cell.name)
    return D


def import_gds(filename, cellname=None, flatten=False, duplayer={}):

    from spira.kernel.utils import scale_coord_up as scu
    from spira import LOG

    LOG.header('Imported GDS file -> \'{}\''.format(filename))

    gdsii_lib = gdspy.GdsLibrary(name='SPiRA-Cell')
    gdsii_lib.read_gds(filename)
    top_level_cells = gdsii_lib.top_level()

    if cellname is not None:
        if cellname not in gdsii_lib.cell_dict:
            raise ValueError('[SPiRA] import_gds() The requested cell' +
                             '(named {}) is not present in file' +
                             '{}'.format(cellname, filename))
        topcell = gdsii_lib.cell_dict[cellname]
    elif cellname is None and len(top_level_cells) == 1:
        topcell = top_level_cells[0]
    elif cellname is None and len(top_level_cells) > 1:

        # TODO: Add this to logger.
        print('Multiple toplevel cells found:')
        for cell in top_level_cells:
            print(cell)

        raise ValueError('[SPiRA] import_gds() There are multiple' +
                         'top-level cells, you must specify cellname' +
                         'to select of one of them')

    cell_list = spira.ElementList()
    c2dmap = {}
    for cell in gdsii_lib.cell_dict.values():
        D = create_spira_cell(cell)

        for e in cell.elements:
            if isinstance(e, gdspy.PolygonSet):
                for points in e.polygons:
                    layer = spira.Layer(number=e.layers[0], datatype=e.datatypes[0])
                    ply = spira.Polygons(polygons=[points],
                                         gdslayer=layer)
                    ply.scale_up()
                    D += ply
            elif isinstance(e, gdspy.Polygon):
                layer = spira.Layer(number=e.layers, datatype=e.datatype)
                ply = spira.Polygons(polygons=[e.points],
                                     gdslayer=layer)
                ply.scale_up()
                D += ply

        c2dmap.update({cell:D})
        cell_list += cell

    for cell in cell_list:
        wrap_references(cell, c2dmap)
        wrap_labels(cell, c2dmap)

    top_spira_cell = c2dmap[topcell]

    # for ply in top_spira_cell.elementals.polygons:
    #     print(ply.polygons)

    # print('Toplevel Cell: {}\n'.format(top_spira_cell))
    # print('\n---------- Cells --------------')
    # for i, D in enumerate(top_spira_cell.dependencies()):
    #     print('{}. {}'.format(i, D.name))
    # print('')

    if flatten == True:
        D = spira.Cell(name='import_gds')

        # for key, polygon in top_spira_cell.get_polygons(True).items():
        #     layer, datatype = key[0], key[1]
        #     for l1, l2 in duplayer.items():
        #         if layer == l1: layer = l2
        #     poly = spira.Polygons(polygons=polygon, gdslayer=layer, gdsdatatype=datatype)
        #     poly.scale_up()
        #     D += poly

        # for l in top_spira_cell.lbls:
        #     params = {}
        #     params['text'] = l.text
        #     params['gdslayer'] = l.gdslayer
        #     params['str_anchor'] = l.str_anchor

        #     D += spira.Label(position=scu(l.position), **params)
        return D
    else:
        return top_spira_cell






