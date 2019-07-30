import spira.all as spira


class Resistor(spira.PCell):

    width = spira.NumberParameter(default=spira.RDD.R1.MIN_WIDTH, doc='Width of the shunt resistance.')
    length = spira.NumberParameter(default=spira.RDD.R1.MIN_LENGTH, doc='Length of the shunt resistance.')

    def validate_parameters(self):
        if self.width > self.length:
            raise ValueError('`Width` cannot be larger than `length`.')
        return True

    @spira.cache()
    def get_ports(self):
        p1 = spira.Port(name='P1', midpoint=(-self.length/2,0), orientation=180, width=self.width, process=spira.RDD.PROCESS.R1)
        p2 = spira.Port(name='P2', midpoint=(self.length/2,0), orientation=0, width=self.width, process=spira.RDD.PROCESS.R1)
        return [p1, p2]

    def create_elements(self, elems):
        p1, p2 = self.get_ports()
        elems += spira.RouteStraight(p1=p1, p2=p2, layer=spira.RDD.PLAYER.R1.METAL)
        return elems

    def create_ports(self, ports):
        ports += self.get_ports()
        return ports


if __name__ == '__main__':

    D = Resistor()
    D.gdsii_output(file_name='Resistor')


