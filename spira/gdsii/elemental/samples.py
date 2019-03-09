import spira
from spira import param, shapes


if __name__ == '__main__':

    poly_cell = spira.Cell(name='POLYGONS')

    points = [[(0, 0), (2, 2), (2, 6), (-6, 6), (-6, -6), (-4, -4), (-4, 4), (0, 4)]]
    poly_cell += spira.Polygons(shape=points)

    poly_cell.output()

