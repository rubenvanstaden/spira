import spira
import pytest
from spira import param
from spira import shapes
from spira.rdd.layer import PurposeLayer

UM = 1e6

# -------------------------------------------- spira.Library ----------------------------------------

def test_library():
    l1 = spira.Library()
    l2 = spira.Library(name='library')
    l3 = spira.Library()

    assert l1.is_empty() == True

    cell = spira.Cell(name='C1')
    l1 += cell
    l3 += cell

    assert l1 == l3
    assert l1 != l2
    assert len(l1) == 1
    assert l1.name == 'spira_library'
    assert l2.name == 'library'
    assert (cell in l1) == True
    assert l1['C1'] == cell

    l1.clear()

    assert len(l1) == 0
    assert l1 == l2

# -------------------------------------------- spira.CellList ---------------------------------------

def test_cell_list():
    cl = spira.CellList()
    assert cl.is_empty() == True

    c1 = spira.Cell('C1')
    c2 = spira.Cell('C2')
    c3 = spira.Cell('C3')

    cl += c1
    cl += [c2, c3]

    assert len(cl) == 3
    assert cl['C2'] == c2
    assert cl.index('C2') == 1
    assert cl.index(c2) == 1

    del cl['C1']

    assert cl[0] == c2
    assert len(cl) == 2

    del cl[c3]

    assert len(cl) == 1

# ----------------------------------------- spira.ElementalList ------------------------------------

def test_elemental_list():
    el = spira.ElementList()
    assert len(el) == 0

# -------------------------------------------- spira.Shapes ----------------------------------------

def test_shapes():
    pass

# -------------------------------------------- spira.Polygon ----------------------------------------

def test_elem_polygon():
    p1 = [[[0,0], [3,0], [3,1], [0,1]]]
    p2 = [[[4,0], [7,0], [7,1], [4,1]]]
    p3 = [[[8,0], [11,0], [11,1], [8,1]]]

    # Create polygon using class parameters.
    ply1 = spira.Polygons(p1)
    assert issubclass(type(ply1.shape), shapes.Shape)
    assert ply1.gdslayer.number == 0
    assert ply1.gdslayer.datatype == 0

    # Create polygon using new layer number.
    ply2 = spira.Polygons(
        shape=p2,
        gdslayer=spira.Layer(number=77)
    )
    assert issubclass(type(ply2.shape), shapes.Shape)
    assert ply2.gdslayer.number == 77
    assert ply2.gdslayer.datatype == 0

    # Create polygon using new shape, number and datatype.
    ply3 = spira.Polygons(
        shape=shapes.Shape(points=p3),
        gdslayer=spira.Layer(number=51, datatype=1)
    )
    assert issubclass(type(ply3.shape), shapes.Shape)
    assert ply3.gdslayer.number == 51
    assert ply3.gdslayer.datatype == 1

# -------------------------------------------- spira.Label ------------------------------------------

def test_elem_label():
    l1 = spira.Label(position=(0,0), text='L1')
    assert all([a == b for a, b in zip(l1.position, [0,0])])
    assert l1.text == 'L1'
    assert l1.rotation == 0
    assert l1.magnification == 1
    assert l1.reflection == False
    assert l1.texttype == 0

# -------------------------------------------- spira.Cell -------------------------------------------

def test_elem_cell():
    c1 = spira.Cell(name='CellA')
    assert c1.name == 'CellA'
    assert len(c1.ports) == 0
    assert len(c1.elementals) == 0

    c1.ports += spira.Port(name='P1')
    assert len(c1.ports) == 1

    c1.elementals += spira.Polygons(shape=[[[0,0], [1,0], [1,1], [0,1]]])
    assert len(c1.elementals) == 1
    # assert c1.elementals[0].center == (0,0)

    # c1.move(destination=)

    class CellB(spira.Cell):

        def create_elementals(self, elems):

            elems += spira.Polygons(
                shape=[[[0,0], [3,0], [3,1], [0,1]]],
                gdslayer=spira.Layer(number=77)
            )

            return elems

    c2 = CellB()
    assert c2.name == 'CellB-0'
    assert len(c1.elementals) == 1
    assert isinstance(c2.elementals[0], spira.Polygons)

# -------------------------------------------- spira.SRef -------------------------------------------

def test_elem_sref():
    class CellB(spira.Cell):

        def create_elementals(self, elems):

            elems += spira.Polygons(
                shape=[[[0,0], [3,0], [3,1], [0,1]]],
                gdslayer=spira.Layer(number=77)
            )

            return elems

    c2 = CellB()

    s1 = spira.SRef(structure=c2)
    assert all([a == b for a, b in zip(s1.midpoint, [0,0])])
    assert s1.rotation == 0
    assert s1.magnification == 1
    assert s1.reflection == False

# -------------------------------------------- spira.Port -------------------------------------------

def test_elem_port():
    class PortExample(spira.Cell):

        def create_ports(self, ports):
            ports += spira.Port(name='P1', midpoint=(-1,2))
            ports += spira.Port(name='P2', midpoint=(0,3))
            return ports

    cell = PortExample()

    p1 = cell.ports[0]
    p2 = cell.ports[1]

#     assert repr(p1) == '[SPiRA: Port] (name P1, midpoint (-1, 2))'

    assert p1.midpoint == [-1,2]
    assert p1.orientation == 0
    p1.reflect()
    assert p1.midpoint == [-1,-2]
    assert p1.orientation == 0
    p1.rotate(angle=90)
    assert p1.midpoint == [2,-1]
    assert p1.orientation == 90
    p1.translate(dx=10, dy=5)
    assert p1.midpoint == [12, 4]

# -------------------------------------------- spira.Term -------------------------------------------

def test_elem_terminal():
    class TerminalExample(spira.Cell):

        width = param.FloatField(default=10)
        height = param.FloatField(default=1)

        def create_ports(self, ports):
            ports += spira.Term(name='P1', midpoint=(10,0), width=self.height, orientation=180)
            return ports

    cell = TerminalExample()

    terms = cell.term_ports
    assert isinstance(terms['P1'], spira.Term)
    assert isinstance(cell.ports[0], spira.Term)
    assert isinstance(cell.terms[0], spira.Term)

# -------------------------------------------- spira.Layer -------------------------------------------

def test_elem_layer():
    l1 = spira.Layer()
    l2 = spira.Layer(number=18, datatype=3)
    l3 = spira.Layer(number=18, datatype=3)
    assert l1.key == (0,0)
    assert l2.key == (18,3)
    assert l2.key != (18,0)
    assert l1 != l2
    assert l2 == l3

    p1 = PurposeLayer(name='Metals')
    p2 = PurposeLayer(name='Ground')
    p3 = PurposeLayer(name='Skyplane', datatype=3)
    p4 = PurposeLayer(name='Skyplane', datatype=2)
    assert p1.name == 'Metals'
    assert p1 == p2
    assert p1 != p3

    p5 = p3 + p4
    assert p5.datatype == 5
    assert p3.datatype == 3
    p6 = p3 + 6
    assert p6.datatype == 9
    p6 += p3
    assert p6.datatype == 12





