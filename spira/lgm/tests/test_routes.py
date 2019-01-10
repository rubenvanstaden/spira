import spira
import pytest
from spira import param
from spira import shapes
from spira.lgm.route.manhattan import RouteManhattan180
from spira.lgm.route.manhattan90 import RouteManhattan90


# ----------------------------------- 180 degrees ------------------------------


def test_routes_q1_180():

    p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2)
    p2 = spira.Term(name='P2', midpoint=(50,25), orientation=90, width=1.5)
    rm = RouteManhattan180(port1=p1, port2=p2, radius=10)


def test_routes_q2_180():
    p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2)
    p2 = spira.Term(name='P2', midpoint=(-50,25), orientation=180, width=1.5)
    rm = RouteManhattan180(port1=p1, port2=p2, radius=10)


def test_routes_q3_180():
    p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2)
    p2 = spira.Term(name='P2', midpoint=(-50,-25), orientation=0, width=2)
    rm = RouteManhattan180(port1=p1, port2=p2, radius=10)


def test_routes_q4_180():
    p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2)
    p2 = spira.Term(name='P2', midpoint=(50,-25), orientation=0, width=2)
    rm = RouteManhattan180(port1=p1, port2=p2, radius=10)


# ----------------------------------- 180 degrees ------------------------------


def test_routes_q1_90():
    p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2)
    p2 = spira.Term(name='P2', midpoint=(50,25), orientation=90, width=1.5)
    rm = RouteManhattan90(port1=p1, port2=p2, radius=10)
    return spira.SRef(rm, midpoint=(50,50))


def test_routes_q2_90():
    p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2)
    p2 = spira.Term(name='P2', midpoint=(-50,25), orientation=180, width=1.5)
    rm = RouteManhattan90(port1=p1, port2=p2, radius=10)
    return spira.SRef(rm, midpoint=(-50,50))


def test_routes_q3_90():
    p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2)
    p2 = spira.Term(name='P2', midpoint=(-50,-25), orientation=0, width=2)
    rm = RouteManhattan90(port1=p1, port2=p2, radius=10)
    return spira.SRef(rm, midpoint=(-50,-50))


def test_routes_q4_90():
    p1 = spira.Term(name='P1', midpoint=(0,0), orientation=0, width=2)
    p2 = spira.Term(name='P2', midpoint=(50,-25), orientation=0, width=2)
    rm = RouteManhattan90(port1=p1, port2=p2, radius=10)
    return spira.SRef(rm, midpoint=(50,-50))


