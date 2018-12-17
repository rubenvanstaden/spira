import os
import gdspy
import spira

from spira import log as LOG

from spira.gdsii.io import *
from spira.gdsii.utils import scale_coord_down as scd

from spira.param.field.typed_graph import EdgeCapacitor
from spira.param.field.typed_graph import EdgeInductor

import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.offline as offline

from spira import settings


class DrawGraphAbstract(object):
    def abstract_collector(self):
        from spira.gdsii.elemental.port import __Port__

        for p in self.get_ports():
            p.commit_to_gdspy(cell=self)

        for e in self.elementals.flat_copy(level=-1):
            if not issubclass(type(e), __Port__):
                e.commit_to_gdspy(cell=self)
        return self

    def plot_subgraphs(self, combine=False):
        cell = self.abstract_collector()

        for name, g in cell.subgraphs.items():
            self._plotly_graph(g, name, labeltext='id')

    def write_graph(self, graphname=None, labeltext='id'):
        if isinstance(self, spira.Cell):
            cell = self.abstract_collector()

            import networkx as nx
            from spira.gdsii.elemental.graph import GraphAbstract
            def graph(cell):
                for geom in cell.elementals:
                    if issubclass(type(geom), GraphAbstract):
                        return geom.g
                return None

            g = graph(cell)

            if graphname is not None:
                if name == graphname:
                    self._plotly_graph(g, graphname, labeltext)
            else:
                self._plotly_graph(g, self.name, labeltext)
        elif isinstance(self, spira.Graph):
            self._plotly_graph(self.g, graphname, labeltext)

    def _plotly_graph(self, G, graphname, labeltext):
        edges = self._create_edges(G)
        nodes = self._create_nodes(G, labeltext)

        edge_trace = go.Scatter(
            x=edges['x_pos'],
            y=edges['y_pos'],
            line=dict(width=1.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        node_trace = go.Scatter(
            x=nodes['x_pos'],
            y=nodes['y_pos'],
            text=nodes['text'],
            name='markers',
            mode='markers',
            hoverinfo='text',
            marker=dict(
                color=nodes['color'],
                size=30,
                line=dict(width=2)))

        edge_label_trace = go.Scatter(
            x=edges['x_labels'],
            y=edges['y_labels'],
            text=edges['text'],
            mode='markers',
            hoverinfo='text',
            marker=dict(
                color='#6666FF',
                size=2,
                line=dict(width=4)))

        fig = go.Figure(data=[edge_trace, node_trace, edge_label_trace],
                    layout=go.Layout(
                    title='<br>' + graphname,
                    titlefont=dict(size=24),
                    showlegend=False,
                    width=1200,
                    height=1200,
                    hovermode='closest',
                    margin=dict(b=20,l=5,r=5,t=40),
                    xaxis=go.layout.XAxis(showgrid=False,
                        zeroline=False,
                        showticklabels=False),
                    yaxis=go.layout.YAxis(showgrid=False,
                        zeroline=False,
                        showticklabels=False)))

        directory = os.getcwd() + '/debug/'
        file_name = directory + str(graphname) + '.html'

        if not os.path.exists(directory):
            os.makedirs(directory)

        offline.plot(fig, filename=file_name)

    def _create_edges(self, G):

        edges = {}

        edges['x_pos'] = []
        edges['y_pos'] = []

        edges['x_labels'] = []
        edges['y_labels'] = []

        edges['text'] = []

        for e in G.edges():
            x0, y0 = G.node[e[0]]['pos']
            x1, y1 = G.node[e[1]]['pos']

            edges['x_pos'] += [x0, x1, None]
            edges['y_pos'] += [y0, y1, None]

            x = x0 + (x1-x0)/2.0
            y = y0 + (y1-y0)/2.0

            edges['x_labels'].append(x)
            edges['y_labels'].append(y)

            edge = G[e[0]][e[1]]

            if 'surface' in edge:
                if isinstance(edge['surface'], EdgeCapacitor):
                    edges['text'].append(edge['surface'].id)
                if isinstance(edge['surface'], EdgeInductor):
                    edges['text'].append(edge['surface'].id)

        return edges

    def _create_nodes(self, G, labeltext):
        import spira

        nodes = {}

        nodes['x_pos'] = []
        nodes['y_pos'] = []
        nodes['text'] = []
        nodes['color'] = []

        for n in G.nodes():
            x, y = G.node[n]['pos']

            nodes['x_pos'].append(x)
            nodes['y_pos'].append(y)

            label = None

            if 'pin' in G.node[n]:
                label = G.node[n]['pin']
            elif 'surface' in G.node[n]:
                label = G.node[n]['surface']

            if label:
                if labeltext == 'number':
                    nodes['text'].append(n)
                else:
                    if issubclass(type(label), spira.Cell):
                        nodes['text'].append(label.name)
                    elif isinstance(label, spira.SRef):
                        nodes['text'].append(label.ref.name)
                    else:
                        nodes['text'].append(label.id)

                if isinstance(label, spira.SRef):
                    nodes['color'].append(label.ref.color)
                else:
                    nodes['color'].append(label.color)

        return nodes

