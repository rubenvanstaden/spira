import spira.all as spira
from spira.all import RDD


class Resistor(spira.PCell):

    width = spira.NumberParameter(default=RDD.R1.MIN_WIDTH, doc='Width of the shunt resistance.')
    length = spira.NumberParameter(default=RDD.R1.MIN_LENGTH, doc='Length of the shunt resistance.')

    def validate_parameters(self):
        if self.width > self.length:
            raise ValueError('`Width` cannot be larger than `length`.')
        return True

    def create_elements(self, elems):
        elems += spira.Box(width=self.length, height=self.width, layer=spira.RDD.PLAYER.R1.METAL)
        return elems


if __name__ == '__main__':

    D = Resistor()
    D.gdsii_output(file_name='Resistor')


