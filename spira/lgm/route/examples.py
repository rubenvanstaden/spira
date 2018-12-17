import spira


class RouteCurve(spira.Route):
    """
    Create a path elemental by extending gdspy.Path 
    to include dynamic parameter bindings.
    """

    def create_points(self, points):
        import numpy

        spec = {'layer': 1, 'datatype': 1}
        self.segment(3, '+x', **spec)
        self.arc(2, -numpy.pi / 2.0, numpy.pi / 6.0, **spec)
        self.segment(4, **spec)
        self.turn(2, -2.0 * numpy.pi / 3.0, **spec)

        points = self.polygons

        return points

    def create_ports(self, ports):

        # TODO: Define the ports connected 
        # to the points here.

        return ports


if __name__ == '__main__':

    curve = RouteCurve(width=2, initial_point=(0,0))
    cell = spira.RouteToCell(shape=curve)
    cell.construct_gdspy_tree()
