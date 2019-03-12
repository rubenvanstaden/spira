import spira
from spira import param, shapes


if __name__ == '__main__':

    poly_cell = spira.Cell(name='POLYGONS')

    points = [[(0, 0), (2, 2), (2, 6), (-6, 6), (-6, -6), (-4, -4), (-4, 4), (0, 4)]]
    poly1 = spira.Polygons(shape=points)
    poly_cell += poly1

    poly2 = spira.Polygons(shape=points).rotate(angle=90)
    poly2.move(destination=(10, 0))
    poly_cell += poly2

    poly_cell.output()
    # poly_cell.writer()

