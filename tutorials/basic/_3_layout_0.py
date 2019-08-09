import spira.all as spira


class Resistor(spira.PCell):

    width = spira.NumberParameter(default=spira.RDD.R1.MIN_WIDTH, doc='Width of the shunt resistance.')
    length = spira.NumberParameter(default=spira.RDD.R1.MIN_LENGTH, doc='Length of the shunt resistance.')

    def validate_parameters(self):
        if self.width > self.length:
            raise ValueError('`Width` cannot be larger than `length`.')
        return True

    def create_elements(self, elems):
        w, l = self.width, self.length
        # shape = spira.Shape(points=[[0,0], [l,0], [l,w], [0,w]])
        # elems += spira.Polygon(shape=shape, layer=spira.RDD.PLAYER.R1.METAL)
        return elems


if __name__ == '__main__':

    D = Resistor()
    D.gdsii_output()


