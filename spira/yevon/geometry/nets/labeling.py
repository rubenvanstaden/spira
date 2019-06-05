

__all__ = ['net_nodes_devices', 'net_nodes_process_polygons']


def net_nodes_process_polygons(net, process_polygons):
    triangles = net.process_triangles()
    for key, nodes in triangles.items():
        for n in nodes:
            for poly in net.elementals:
                if poly.encloses(net.g.node[n]['position']):
                    net.g.node[n]['process_polygon'] = poly


def net_nodes_devices(net, ports):
    for n, triangle in net.triangle_nodes().items():
        points = [geom.c2d(net.mesh_data.points[i]) for i in triangle]
        for D in net.ports:
            if isinstance(D, (Port, Port)):
                if D.encloses(points):
                    net.g.node[n]['device_reference'] = D
            else:
                for p in D.ports:
                    if p.gds_layer.number == net.layer.number:
                        if p.encloses(points):
                            if 'device_reference' in net.g.node[n]:
                                net.add_new_node(n, D, p.midpoint)
                            else:
                                # TODO: Maybe to net.node_device = D
                                net.g.node[n]['device_reference'] = D


# def route_nodes(net):
#     """  """
#     from spira import pc

#     def r_func(R):
#         if issubclass(type(R), pc.ProcessLayer):
#             R_ply = R.elementals[0]
#             for n in net.g.nodes():
#                 if R_ply.encloses(net.g.node[n]['position']):
#                     net.g.node[n]['route'] = R
#         else:
#             for pp in R.ref.metals:
#                 R_ply = pp.elementals[0]
#                 for n in net.g.nodes():
#                     if R_ply.encloses(net.g.node[n]['position']):
#                         net.g.node[n]['route'] = pp

#     for R in net.route_nodes:
#         if isinstance(R, spira.ElementalList):
#             for r in R:
#                 r_func(r)
#         else:
#             r_func(R)


# def boundary_nodes(net):
#     if net.level > 1:
#         for B in net.bounding_boxes:
#             for ply in B.elementals.polygons:
#                 for n in net.g.nodes():
#                     if ply.encloses(net.g.node[n]['position']):
#                         net.g.node[n]['device_reference'] = B.S
#                         net.g.node[n]['device_reference'].node_id = '{}_{}'.format(B.S.ref.name, B.S.midpoint)

