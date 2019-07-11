import spira.all as spira


class PolygonExample(spira.Cell):

    def create_elements(self, elems):
        pts = [[0, 0], [2, 2], [2, 6], [-6, 6], [-6, -6], [-4, -4], [-4, 4], [0, 4]]
        shape = spira.Shape(points=pts)
        elems += spira.Polygon(shape=shape, layer=spira.Layer(1))
        return elems


D = PolygonExample()
D.gdsii_output(name='Element')