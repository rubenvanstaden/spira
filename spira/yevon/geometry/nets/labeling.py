

def polygon_nodes(net):
    triangles = net.__layer_triangles_dict__()
    for key, nodes in triangles.items():
        for n in nodes:
            for poly in net.elementals:
                if poly.encloses(net.g.node[n]['position']):
                    net.g.node[n]['polygon'] = poly


def device_nodes(net):
    for n, triangle in net.__triangle_nodes__().items():
        points = [geom.c2d(net.mesh_data.points[i]) for i in triangle]
        for D in net.ports:
            if isinstance(D, (Port, Port)):
                if D.encloses(points):
                    net.g.node[n]['device'] = D
            else:
                for p in D.ports:
                    if p.gds_layer.number == net.layer.number:
                        if p.encloses(points):
                            if 'device' in net.g.node[n]:
                                net.__add_new_node__(n, D, p.midpoint)
                            else:


                                # TODO: Maybe to net.node_device = D
                                net.g.node[n]['device'] = D


def route_nodes(net):
    """  """
    from spira import pc

    def r_func(R):
        if issubclass(type(R), pc.ProcessLayer):
            R_ply = R.elementals[0]
            for n in net.g.nodes():
                if R_ply.encloses(net.g.node[n]['position']):
                    net.g.node[n]['route'] = R
        else:
            for pp in R.ref.metals:
                R_ply = pp.elementals[0]
                for n in net.g.nodes():
                    if R_ply.encloses(net.g.node[n]['position']):
                        net.g.node[n]['route'] = pp

    for R in net.route_nodes:
        if isinstance(R, spira.ElementalList):
            for r in R:
                r_func(r)
        else:
            r_func(R)


def boundary_nodes(net):
    if net.level > 1:
        for B in net.bounding_boxes:
            for ply in B.elementals.polygons:
                for n in net.g.nodes():
                    if ply.encloses(net.g.node[n]['position']):
                        net.g.node[n]['device'] = B.S
                        net.g.node[n]['device'].node_id = '{}_{}'.format(B.S.ref.name, B.S.midpoint)

