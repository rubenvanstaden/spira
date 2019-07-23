import networkx as nx


def _combine_nodes(g, algorithm):
    """ Combine all nodes of the same type into one node. """

    def compare_s2s(u, v):
        if ('process_polygon' in g.node[u]) and ('process_polygon' in g.node[v]):
            if ('device_reference' not in g.node[u]) and ('device_reference' not in g.node[v]):
                if g.node[u]['process_polygon'].id_string() == g.node[v]['process_polygon'].id_string():
                    return True

    def compare_d2d(u, v):
        if ('device_reference' in g.node[u]) and ('device_reference' in g.node[v]):
            if g.node[u]['device_reference'].id_string() == g.node[v]['device_reference'].id_string():
                return True

    def compare_b2b(u, v):
        if ('branch_node' in g.node[u]) and ('branch_node' in g.node[v]):
            if g.node[u]['branch_node'].id_string() == g.node[v]['branch_node'].id_string():
                return True

    def sub_nodes(b):
        S = g.subgraph(b)

        device = nx.get_node_attributes(S, 'device_reference')
        process_polygon = nx.get_node_attributes(S, 'process_polygon')
        center = nx.get_node_attributes(S, 'position')
        branch_node = nx.get_node_attributes(S, 'branch_node')
        display = nx.get_node_attributes(S, 'display')

        sub_pos = list()
        for value in center.values():
            sub_pos = [value[0], value[1]]

        return dict(
            device_reference=device,
            process_polygon=process_polygon,
            branch_node=branch_node,
            position=sub_pos,
            display=display
        )

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

    Pos = nx.get_node_attributes(Q, 'position')
    Device = nx.get_node_attributes(Q, 'device_reference')
    Polygon = nx.get_node_attributes(Q, 'process_polygon')
    Branches = nx.get_node_attributes(Q, 'branch_node')
    Display = nx.get_node_attributes(Q, 'display')

    Edges = nx.get_edge_attributes(Q, 'weight')

    g1 = nx.Graph()

    for key, value in Edges.items():
        n1, n2 = list(key[0]), list(key[1])
        g1.add_edge(n1[0], n2[0])

    for n in g1.nodes():
        for key, value in Pos.items():
            if n == list(key)[0]:
                g1.node[n]['position'] = [value[0], value[1]]

        for key, value in Device.items():
            if n == list(key)[0]:
                if n in value:
                    g1.node[n]['device_reference'] = value[n]

        for key, value in Branches.items():
            if n == list(key)[0]:
                if n in value:
                    g1.node[n]['branch_node'] = value[n]

        for key, value in Polygon.items():
            if n == list(key)[0]:
                if n in value:
                    g1.node[n]['process_polygon'] = value[n]

        for key, value in Display.items():
            if n == list(key)[0]:
                if n in value:
                    g1.node[n]['display'] = value[n]

    g = g1

    return g1


from spira.core.parameters.initializer import ParameterInitializer
class CombineNetNodes(ParameterInitializer):
    pass


def combine_net_nodes(net, algorithm=[]):
    # net = CombineNetNodes()
    g = net.g
    for a in algorithm:
        g = _combine_nodes(g, algorithm=a)
    net.g = g
    return net


