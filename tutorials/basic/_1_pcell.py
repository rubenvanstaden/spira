import spira.all as spira


class Resistor(spira.PCell):

    width = spira.FloatParameter(default=0.3, doc='Width of the shunt resistance.')
    length = spira.FloatParameter(default=1.0, doc='Length of the shunt resistance.')

    def validate_parameters(self):
        if self.width > self.length:
            raise ValueError('`Width` cannot be larger than `length`.')
        return True


if __name__ == '__main__':

    D = Resistor()

    print(D.width, D.length)

    # Width parameter is valid.
    D.width = 0.5
    print(D.width, D.length)

    # Throws a parameter invalid error.
    D.width = 1.1
    print(D.width, D.length)

