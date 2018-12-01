import os
import gdspy
import spira

from spira import log as LOG

from spira.kernel.io import *
from spira.kernel.utils import scale_coord_down as scd

from spira.kernel.parameters.field.typed_graph import EdgeCapacitor
from spira.kernel.parameters.field.typed_graph import EdgeInductor

import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.offline as offline

from spira import settings


class TranformationMixin(object):

    def _rotate_points(self, points, angle = 45, center = (0,0)):
        """
        Rotates points around a centerpoint defined by `center`.
        `points` may be input as either single points [1,2]
        or array-like[N][2], and will return in kind
        """
        angle = angle*np.pi/180
        ca = np.cos(angle)
        sa = np.sin(angle)
        sa = np.array((-sa, sa))
        c0 = np.array(center)
        if np.asarray(points).ndim == 2:
            return (points - c0) * ca + (points - c0)[:,::-1] * sa + c0
        if np.asarray(points).ndim == 1:
            return (points - c0) * ca + (points - c0)[::-1] * sa + c0


    def _reflect_points(self, points, p1=(0,0), p2=(1,0)):
        """
        Reflects points across the line formed by p1 and
        p2. `points` may be input as either single points
        [1,2] or array-like[N][2], and will return in kind
        """
        # From http://math.stackexchange.com/questions/11515/point-reflection-across-a-line
        points = np.array(points); p1 = np.array(p1); p2 = np.array(p2);
        if np.asarray(points).ndim == 1:
            return 2*(p1 + (p2-p1)*np.dot((p2-p1),(points-p1))/norm(p2-p1)**2) - points
        if np.asarray(points).ndim == 2:
            return np.array([2*(p1 + (p2-p1)*np.dot((p2-p1),(p-p1))/norm(p2-p1)**2) - p for p in points])


class DrawGraphAbstract(object):
    def abstract_collector(self):
        from spira.kernel.elemental.port import PortAbstract

        for p in self.get_ports():
            p.add_to_gdspycell(cell=self)

        for e in self.elementals.flat_copy(level=-1):
            if not issubclass(type(e), PortAbstract):
                e.add_to_gdspycell(cell=self)
        return self

    def plot_subgraphs(self, combine=False):
        cell = self.abstract_collector()

        for name, g in cell.subgraphs.items():
            self._plotly_graph(g, name, labeltext='id')

    def write_graph(self, graphname=None, labeltext='id'):
        if isinstance(self, spira.Cell):
            cell = self.abstract_collector()

            import networkx as nx
            from spira.kernel.elemental.graph import GraphAbstract
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


class DrawLayoutAbstract(object):
    import spira

    def output(self, name=None, path='current'):
        if name is None:
            raise ValueError('GDS file not named.')

        write_path = None
        if path == 'current':
            write_path = current_path(name)
        elif path == 'debug':
            write_path = debug_path(name)
        else:
            raise ValueError('`path` variable not implemented!')

        library = settings.get_library()
        # # library.single_cell(self)

        # if isinstance(self, spira.Cell):
        #     for p in self.get_ports():
        #         p.add_to_gdspycell(cell=self)

        library += self
        library.to_gdspy

        # writer = gdspy.GdsWriter('out-file.gds', unit=1.0e-6, precision=1.0e-9)
        # cell = self.gdspycell
        # writer.write_cell(cell)
        # del cell
        # writer.close()

        # print(library)
        # print(gdspy.current_library)
        # print('Writting GDS file to path: {}'.format(write_path))
        #
        # print('')
        # cell = gdspy.current_library.cell_dict['Ruben']
        # print(cell)
        # print('')

        # gdspy.write_gds(outfile=write_path, name=name, unit=1.0e-6)
        gdspy.LayoutViewer(library=library)
        # gdspy.LayoutViewer(library=library, cells=cell)


class OutputMixin(DrawLayoutAbstract, DrawGraphAbstract):
    pass
