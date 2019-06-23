import gdspy
import numpy as np
import spira.all as spira
from spira.yevon.geometry import shapes
from spira.yevon.utils.geometry import distance
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


# class Route(spira.Polygon):

#     def __init__(self, shape, layer, **kwargs):
#         super().__init__(shape=shape, layer=layer, **kwargs)

#     def __repr__(self):
#         if self is None:
#             return 'Route is None!'
#         layer = RDD.GDSII.IMPORT_LAYER_MAP[self.layer]
#         class_string = "[SPiRA: Route {}] (center {}, vertices {}, process {}, purpose {})"
#         return class_string.format(self.alias, self.center, self.count, self.process, self.purpose)


# --- My own tests ---
points = [(0,0), (10,0), (10,10), (20,10)]
# sp6 = gdspy.FlexPath(points, 0.5, corners='circular bend', bend_radius=2, gdsii_path=True)
sp6 = gdspy.FlexPath(points, 0.5, corners='natural', bend_radius=None, gdsii_path=True)


def Route(port1, port2, width, corners='narutal', bend_radius=None, layer=1):
    
    if port1.orientation==0:
        p2=[port2.midpoint[0],port2.midpoint[1]]
        p1=[port1.midpoint[0],port1.midpoint[1]]
    if port1.orientation==90:
        p2=[port2.midpoint[1],-port2.midpoint[0]]
        p1=[port1.midpoint[1],-port1.midpoint[0]]
    if port1.orientation==180:
        p2=[-port2.midpoint[0],-port2.midpoint[1]]
        p1=[-port1.midpoint[0],-port1.midpoint[1]]
    if port1.orientation==270:
        p2=[-port2.midpoint[1],port2.midpoint[0]]
        p1=[-port1.midpoint[1],port1.midpoint[0]]

    print(p1)
    print(p2)

    # path = gdspy.FlexPath([], width=width, corners='natural', bend_radius=None, gdsii_path=True)
    path = gdspy.Path(width, (0, 0))

    # l = port2.midpoint[0] - port1.midpoint[0]
    l = distance(p2, p1)
    print(l)

    # Q1
    if (p2[1] > p1[1]) & (p2[0] > p1[0]):
        path.segment(l/2, '+x')
        path.turn(1, 'l')
        path.segment(l/2, '+y')

    # # Q2
    # if (p2[1] > p1[1]) & (p2[0] < p1[0]):
    #     path.segment(l/2, '-x')
    #     path.turn(1, 'r')
    #     path.segment(l/2, '+y')

    # # Q3
    # if (p2[1] < p1[1]) & (p2[0] < p1[0]):
    #     path.segment(l/2, '-x')
    #     path.turn(1, 'l')
    #     path.segment(l/2, '-y')

    # Q4
    if (p2[1] < p1[1]) & (p2[0] > p1[0]):
        path.segment(l/2, '+x')
        path.turn(1, 'r')
        path.segment(l/2, '-y')

    return path


    # angle = np.mod(port1.orientation, 360)
    # p1, p2 = port1, port2
    # if angle == 90:
    #     p1 = [p1.midpoint[0], p1.midpoint[1]]
    # if angle == 180:
    #     p1 = [p1.midpoint[1], -p1.midpoint[0]]
    # if angle == 270:
    #     p1 = [-p1.midpoint[0], -p1.midpoint[1]]
    # if angle == 0:
    #     p1 = [-p1.midpoint[1], p1.midpoint[0]]

    # # angle = np.mod(p2.orientation, 360)
    # if angle == 90:
    #     p2 = [p2.midpoint[0], p2.midpoint[1]]
    # if angle == 180:
    #     p2 = [p2.midpoint[1], -p2.midpoint[0]]
    # if angle == 270:
    #     p2 = [-p2.midpoint[0], -p2.midpoint[1]]
    # if angle == 0:
    #     p2 = [-p2.midpoint[1], p2.midpoint[0]]


# # Q1
# port1 = spira.Port(name='P1', midpoint=(0,0), orientation=0)
# port2 = spira.Port(name='P2', midpoint=(10,10), orientation=-90)
port1 = spira.Port(name='P1', midpoint=(0,0), orientation=90)
port2 = spira.Port(name='P2', midpoint=(10,10), orientation=-180)

# # Q2
# port1 = spira.Port(name='P1', midpoint=(0,0), orientation=180)
# port2 = spira.Port(name='P2', midpoint=(-10,10), orientation=-90)

# # Q3
# port1 = spira.Port(name='P1', midpoint=(0,0), orientation=180)
# port2 = spira.Port(name='P2', midpoint=(-10,-10), orientation=90)

# # Q4
# port1 = spira.Port(name='P1', midpoint=(0,0), orientation=90)
# port2 = spira.Port(name='P2', midpoint=(10,10), orientation=180)

from spira.yevon.geometry.vector import *
R = Route(port1, port2, width=1)
T = vector_match_transform(v1=R.ports[0], v2=p1)
R.transform(T)

cell = gdspy.Cell(name='Route')
cell.add(R)

gdspy.LayoutViewer()




