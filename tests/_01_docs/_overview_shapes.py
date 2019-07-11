import spira.all as spira


class ShapeExample(spira.Shape): 

    def create_points(self, points):
        points = [[0, 0], [2, 2], [2, 6], [-6, 6], [-6, -6], [-4, -4], [-4, 4], [0, 4]]
        return points


shape = ShapeExample()
print(shape.points)
print(shape.area)
shape.move((10, 0))
print([list([c[0], c[1]]) for c in shape.points])
print(shape.x_coords)


