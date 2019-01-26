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

    def plot_netlist(self, G, graphname, labeltext):
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
        from spira.lpe.mask import Native

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

            if 'device' in G.node[n]:
                label = G.node[n]['device']
            elif 'surface' in G.node[n]:
                label = G.node[n]['surface']

            if label:
                # nodes['text'].append(G.node[n]['display'])

                if labeltext == 'number':
                    nodes['text'].append(n)
                else:
                    if isinstance(label, (spira.Port, spira.Term)):
                        nodes['text'].append(label.id)
                    else:
                        nodes['text'].append(label.id)

                if isinstance(label, spira.SRef):
                    nodes['color'].append(label.ref.color)
                elif isinstance(label, (spira.Port, spira.Term)):
                    nodes['color'].append(label.label.color)
                else:
                    nodes['color'].append(label.color)

        return nodes

