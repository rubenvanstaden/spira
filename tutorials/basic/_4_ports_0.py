import spira.all as spira


class Resistor(spira.PCell):

    width = spira.NumberParameter(default=spira.RDD.R1.MIN_WIDTH, doc='Width of the shunt resistance.')
    length = spira.NumberParameter(default=spira.RDD.R1.MIN_LENGTH, doc='Length of the shunt resistance.')

    def validate_parameters(self):
        if self.width > self.length:
            raise ValueError('`Width` cannot be larger than `length`.')
        return True

    def create_elements(self, elems):
        elems += spira.Box(width=self.length, height=self.width, center=(0,0), layer=spira.RDD.PLAYER.R1.METAL)
        return elems

    def create_ports(self, ports):
        w, l = self.width, self.length
        ports += spira.Port(name='P1_R1', midpoint=(-l/2,0), orientation=180, width=self.width)
        ports += spira.Port(name='P2', midpoint=(l/2,0), orientation=0, width=self.width, process=spira.RDD.PROCESS.R1)
        return ports


if __name__ == '__main__':

    D = Resistor()
    D.gdsii_output(name='Resistor')


