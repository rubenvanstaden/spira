import spira.all as spira


class ResistorManhattan(spira.PCell):

    width = spira.NumberParameter(default=spira.RDD.R1.MIN_WIDTH, doc='Width of the shunt resistance.')
    length = spira.NumberParameter(default=spira.RDD.R1.MIN_LENGTH, doc='Length of the shunt resistance.')

    p1 = spira.Parameter(fdef_name='create_p1')
    p2 = spira.Parameter(fdef_name='create_p2')

    def validate_parameters(self):
        if self.width > self.length:
            raise ValueError('`Width` cannot be larger than `length`.')
        return True

    def create_p1(self):
        return spira.Port(name='P1', midpoint=(-self.length/2,0), orientation=180, width=self.width, process=spira.RDD.PROCESS.R1)

    def create_p2(self):
        return spira.Port(name='P2', midpoint=(self.length/2,2), orientation=0, width=self.width, process=spira.RDD.PROCESS.R1)

    def create_elements(self, elems):
        elems += spira.RouteManhattan(ports=[self.p1, self.p2], layer=spira.RDD.PLAYER.R1.METAL)
        return elems

    def create_ports(self, ports):
        ports += [self.p1, self.p2]
        return ports


class ResistorStraight(spira.PCell):

    width = spira.NumberParameter(default=spira.RDD.R1.MIN_WIDTH, doc='Width of the shunt resistance.')
    length = spira.NumberParameter(default=spira.RDD.R1.MIN_LENGTH, doc='Length of the shunt resistance.')

    p1 = spira.Parameter(fdef_name='create_p1')
    p2 = spira.Parameter(fdef_name='create_p2')

    def validate_parameters(self):
        if self.width > self.length:
            raise ValueError('`Width` cannot be larger than `length`.')
        return True

    def create_p1(self):
        return spira.Port(name='P1', midpoint=(-self.length/2,0), orientation=180, width=self.width, process=spira.RDD.PROCESS.R1)

    def create_p2(self):
        return spira.Port(name='P2', midpoint=(self.length/2,0), orientation=0, width=self.width, process=spira.RDD.PROCESS.R1)

    def create_elements(self, elems):
        elems += spira.RouteStraight(p1=self.p1, p2=self.p2, layer=spira.RDD.PLAYER.R1.METAL)
        return elems

    def create_ports(self, ports):
        ports += [self.p1, self.p2]
        return ports


class ResistorConnect(spira.PCell):

    res0 = spira.CellParameter(default=ResistorManhattan)
    res1 = spira.CellParameter(default=ResistorStraight)

    def create_elements(self, elems):
        s1 = spira.SRef(reference=self.res0())
        s2 = spira.SRef(reference=self.res1())
        # s2.connect(port=s2.ports['P1_R1'], destination=s1.ports['P2_R1'])
        elems += [s1, s2]
        return elems


if __name__ == '__main__':

    D = ResistorConnect()
    D.gdsii_view()


