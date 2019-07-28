import spira.all as spira


class ShapesExample(spira.Cell):
    """  """

    def create_elements(self, elems):

        points = [(10.0, 0.0), (15.0, 10.0), 
                  (0.0, 10.0), (0.0, 5.0), 
                  (-15.0, 5.0), (-5.0, 0.0),
                  (-10.0, -10.0), (-5.0, -15.0),
                  (10.0, -15.0), (5.0, -10.0), (5.0, -5.0)]
        s = spira.Shape(points=points)

        S1 = spira.Cell(name='shape', elements=spira.Polygon(shape=s, layer=spira.Layer(1)))

        # #translate a copy of the shape
        # t = s.move_copy((0.0, 20.0))
        # S2 = Structure("shape_trans", Boundary(Layer(0), t))
        
        # #rotate the shape (angle in degree)
        # t = s.rotate_copy((0.0, 0.0), 50)
        # S3 = Structure("shape_rot", Boundary(Layer(0), t))
        
        # #scale the shape
        # t = s.magnify_copy((0.0, 0.0), 1.2)
        # S4 = Structure("shape_scale", Boundary(Layer(0), t))
        
        # #stretch the shape horizontally and squeeze vertically 
        # t = Stretch(stretch_center = (0.0, 0.0), stretch_factor = (1.5, 0.5))(s)
        # S5 = Structure("shape_stretch", Boundary(Layer(0), t))
        
        # #fit the shape in a box
        # south_west = (-7.0, -7.0)
        # north_east = (7.0, 7.0)
        # t = ShapeFit(s, south_west, north_east)
        # S6 = Structure("shape_fit", Boundary(Layer(0), t))

        # #create a shape which traces the contour with a certain line width
        # t = ShapePath(original_shape = s, path_width = 0.5)
        # S7 = Structure("ShapePath1", Boundary(Layer(0), t))
        
        # t = ShapePathRounded(original_shape = s, path_width = 0.5)
        # S8 = Structure("ShapePath2", Boundary(Layer(0), t))
        
        # #expand the shape with a certain distance
        # t = ShapeGrow(s, 1.0)
        # S9 = Structure("shape_grow", Boundary(Layer(1), t) + Boundary(Layer(0), s))
        
        # #round the shape with a given radius
        # t = ShapeRound(original_shape = s, radius = 2.0)
        # S10 = Structure("shape_round", Boundary(Layer(1), t) + Boundary(Layer(0), s))
        
        elems += [
            spira.SRef(S1, (0.0, 200.0)),
        ]
        
        return elems


if __name__ == '__main__':

    D = ShapesExample()
    D.gdsii_output(file_name='shape_example')
    # lib = Library(name="Shapes", unit=1e-6, grid=1e-9)
    # lib += layout
    # output = OutputGdsii('shape_example')
    # output.write(my_lib)


