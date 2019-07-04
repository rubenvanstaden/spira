import spira.all as spira


class Resistor(spira.PCell):

    width = spira.NumberParameter(default=spira.RDD.R1.MIN_WIDTH, doc='Width of the shunt resistance.')
    length = spira.NumberParameter(default=spira.RDD.R1.MIN_LENGTH, doc='Length of the shunt resistance.')

    def validate_parameters(self):
        if self.width > self.length:
            raise ValueError('`Width` cannot be larger than `length`.')
        return True

    def create_elements(self, elems):
        elems += spira.Box(alias='ply1', width=self.length, height=self.width, center=(0,0), layer=spira.RDD.PLAYER.R1.METAL)
        return elems

    def create_ports(self, ports):
        # Process symbol will automatically be added to the port name.
        ports += self.elements['ply1'].ports['E1_R1'].copy(name='P1')
        ports += self.elements['ply1'].ports['E3_R1'].copy(name='P2')
        return ports


if __name__ == '__main__':

    D = Resistor()
    D.gdsii_output(name='Resistor')


