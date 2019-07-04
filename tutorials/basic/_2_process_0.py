import spira.all as spira


class Resistor(spira.PCell):

    width = spira.NumberParameter(default=spira.RDD.R1.MIN_WIDTH, doc='Width of the shunt resistance.')
    length = spira.NumberParameter(default=spira.RDD.R1.MIN_LENGTH, doc='Length of the shunt resistance.')

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

