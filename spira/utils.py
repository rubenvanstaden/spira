import spira
import gdspy
import math
import pyclipper
import numpy as np
import networkx as nx

from spira.settings import SCALE_DOWN, SCALE_UP, OFFSET


st = pyclipper.scale_to_clipper
sf = pyclipper.scale_from_clipper


def nodes_combine(g, algorithm):
    """ Combine all nodes of the same type into one node. """

    def compare_d2s(u, v):
        if ('device' in g.node[u]):
            if ('device' not in g.node[v]):
                if g.node[u]['device'].node_id == g.node[v]['surface'].node_id:
                    return True
        if ('device' in g.node[v]):
            if ('device' not in g.node[u]):
                if g.node[v]['device'].node_id == g.node[u]['surface'].node_id:
                    return True
                    
    def compare_s2s(u, v):
        if ('surface' in g.node[u]) and ('surface' in g.node[v]):
            if ('device' not in g.node[u]) and ('device' not in g.node[v]):
                if g.node[u]['surface'].node_id == g.node[v]['surface'].node_id:
                    return True

    def compare_d2d(u, v):
        if ('device' in g.node[u]) and ('device' in g.node[v]):
            if g.node[u]['device'].node_id == g.node[v]['device'].node_id:
                return True

    def compare_b2b(u, v):
        if ('branch' in g.node[u]) and ('branch' in g.node[v]):
            if g.node[u]['branch'].node_id == g.node[v]['branch'].node_id:
                return True

    def sub_nodes(b):
        S = g.subgraph(b)
        device = nx.get_node_attributes(S, 'device')
        surface = nx.get_node_attributes(S, 'surface')
        center = nx.get_node_attributes(S, 'pos')
        route = nx.get_node_attributes(S, 'route')
        branch = nx.get_node_attributes(S, 'branch')
        sub_pos = list()
        for value in center.values():
            sub_pos = [value[0], value[1]]
        return dict(device=device, surface=surface, branch=branch, route=route, pos=sub_pos)

    if algorithm == 'd2s':
        Q = nx.quotient_graph(g, compare_d2s, node_data=sub_nodes)
    elif algorithm == 's2s':
        Q = nx.quotient_graph(g, compare_s2s, node_data=sub_nodes)
    elif algorithm == 'd2d':
        Q = nx.quotient_graph(g, compare_d2d, node_data=sub_nodes)
    elif algorithm == 'b2b':
        Q = nx.quotient_graph(g, compare_b2b, node_data=sub_nodes)
    else:
        raise ValueError('Compare algorithm not implemented!')

    Pos = nx.get_node_attributes(Q, 'pos')
    Device = nx.get_node_attributes(Q, 'device')
    Polygon = nx.get_node_attributes(Q, 'surface')
    Route = nx.get_node_attributes(Q, 'route')
    Branches = nx.get_node_attributes(Q, 'branch')

    Edges = nx.get_edge_attributes(Q, 'weight')

    g1 = nx.Graph()

    for key, value in Edges.items():
        n1, n2 = list(key[0]), list(key[1])
        g1.add_edge(n1[0], n2[0])

    for n in g1.nodes():
        for key, value in Pos.items():
            if n == list(key)[0]:
                g1.node[n]['pos'] = [value[0], value[1]]
        for key, value in Device.items():
            if n == list(key)[0]:
                if n in value:
                    g1.node[n]['device'] = value[n]
        for key, value in Branches.items():
            if n == list(key)[0]:
                if n in value:
                    g1.node[n]['branch'] = value[n]
        for key, value in Polygon.items():
            if n == list(key)[0]:
                g1.node[n]['surface'] = value[n]
        for key, value in Route.items():
            if n == list(key)[0]:
                if n in value:
                    g1.node[n]['route'] = value[n]
    return g1
    

# def boolean(subj, clip=None, method=None, closed=True, scale=0.00001):
def boolean(subj, clip=None, method=None, closed=True, scale=1):
    from spira.gdsii.elemental.polygons import PolygonAbstract

    if clip is None and len(subj) <= 1:
        return subj

    sc = 1/scale

    pc = pyclipper.Pyclipper()
    if issubclass(type(subj), PolygonAbstract):
        subj = subj.polygons
    if issubclass(type(clip), PolygonAbstract):
        clip = clip.polygons
    if clip is not None:
        # pc.AddPaths(st(clip, sc), pyclipper.PT_CLIP, True)
        pc.AddPaths(clip, pyclipper.PT_CLIP, True)
    # pc.AddPaths(st(subj, sc), pyclipper.PT_SUBJECT, closed)
    pc.AddPaths(subj, pyclipper.PT_SUBJECT, closed)

    if method == 'not':
        value = pc.Execute(pyclipper.CT_DIFFERENCE, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)
    elif method == 'or':
        value = pc.Execute(pyclipper.CT_UNION, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)
    elif method == 'and':
        value = pc.Execute(pyclipper.CT_INTERSECTION, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)
    elif method == 'xor':
        value = pc.Execute(pyclipper.CT_XOR, pyclipper.PFT_NONZERO, pyclipper.PFT_NONZERO)
    else:
        raise ValueError('Please specify a clipping method')

    return value

    # PTS = []
    # mc = sf(value, sc)
    # for pts in pyclipper.SimplifyPolygons(mc):
    #     PTS.append(np.array(pts))
    # points = pyclipper.CleanPolygons(PTS)

    # return np.array(points)


def offset(points, offset_type=None, scale=OFFSET):
    """ Apply polygon offsetting using Angusj.
    Either blow up polygons or blow it down. """
    pco = pyclipper.PyclipperOffset()
    pco.AddPath(points, pyclipper.JT_MITER, pyclipper.ET_CLOSEDPOLYGON)
    pp = None
    if offset_type == 'down':
        pp = pco.Execute(-10000)[0]
    elif offset_type == 'up':
        pp = pco.Execute(scale * SCALE_UP)
    else:
        raise ValueError('Please select the Offset function to use')
    points = []
    for pts in pp:
        points.append(np.array(pts))
    return np.array(points)


def encloses(points, position):
    assert position is not None, 'No label position found.'
    if pyclipper.PointInPolygon(position, points) != 0:
        return True
    return False


def labeled_polygon_id(position, polygons):
    for i, spira_polygon in enumerate(polygons):
        for j, points in enumerate(spira_polygon.polygons):
            if encloses(points, position):
                # return spira_polygon.id
                return spira_polygon.node_id
    return None


def snap_points(points, grids_per_unit=None):
    """ Round a list of points to a grid value. """
    if grids_per_unit is None:
        grids_per_unit = _grids_per_unit()
    else:
        raise ValueError('please define grids per unit')
    points = _points_to_float(points)
    polygons = list()
    for coords in points:
        poly = list()
        for coord in coords:
            p1 = (math.floor(coord[0] * grids_per_unit + 0.5)) / grids_per_unit
            p2 = (math.floor(coord[1] * grids_per_unit + 0.5)) / grids_per_unit
            poly.append([int(p1), int(p2)])
        polygons.append(poly)

    return polygons


def c2d(coord):
    RDD = spira.get_rule_deck()

    """ Convert coordinate to 2D. """
    # pp = [coord[i]*1e+8 for i in range(len(list(coord))-1)]
    pp = [(coord[i]/(RDD.GDSII.GRID)) for i in range(len(list(coord))-1)]
    return pp


def c3d(coord):
    """ Convert coordinate to 3D. """
    pp = [coord[i]*1e+6 for i in range(len(list(coord)))]
    return pp


def scale_coord_up(coord):
    return [c*SCALE_UP for c in coord]


def scale_coord_down(coord):
    return [c*SCALE_DOWN for c in coord]


def scale_polygon_up(polygons, value=None):
    if value is None:
        value = SCALE_UP
    new_poly = []
    for points in polygons:
        # pp = [[float(p[0]*value), float(p[1]*value)] for p in points]
        # pp = np.array([np.array([float(p[0]*value), float(p[1]*value)]) for p in points])
        pp = np.array([np.array([np.floor(float(p[0]*value)), np.floor(float(p[1]*value))]) for p in points])
        new_poly.append(pp)
    return new_poly


def scale_polygon_down(polygons, value=None):
    if value is None:
        value = SCALE_DOWN
        # value = 1
    # value = 1
    new_poly = []
    for points in polygons:
        # pp = [[float(p[0]*value), float(p[1]*value)] for p in points]
        # pp = np.array([np.array([float(p[0]*value), float(p[1]*value)]) for p in points])
        # pp = np.array([np.array([np.floor(float(p[0]*value)), np.floor(float(p[1]*value))]) for p in points])
        pp = np.array([np.array([np.floor(np.int32(p[0]*value)), np.floor(np.int32(p[1]*value))]) for p in points])
        new_poly.append(pp)
    return new_poly


def numpy_to_list(points, start_height, unit=None):
    # return np.array([[np.int32(p[0]*unit), np.int32(p[1]*unit), start_height] for p in points])
    return [[float(p[0]*unit), float(p[1]*unit), start_height] for p in points]

    # pts = []
    # for p in points:
    #     p1 = round(float(p[0]*unit), 6)
    #     p2 = round(float(p[1]*unit), 6)
    #     pts.append([p1, p2, start_height])
    # return pts


def cut(ply, position, axis):
    from spira import process as pc
    plys = spira.ElementList()
    gp = ply.commit_to_gdspy()
    pl = gdspy.slice(objects=[gp], position=position, axis=axis)
    for p in pl:
        if len(p.polygons) > 0:
            plys += spira.Polygons(shape=p.polygons)
    return plys




