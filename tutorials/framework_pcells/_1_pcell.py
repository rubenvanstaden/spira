import spira.all as spira


class Junction(spira.PCell):

    width = spira.NumberParameter(default=0.3, doc='Width of the shunt resistance.')
    length = spira.NumberParameter(default=1, doc='Length of the shunt resistance.')

    def validate_parameters(self):
        if self.width > self.length:
            raise ValueError('`Width` cannot be larger than `length`.')
        return True


if __name__ == '__main__':

    D = Junction()

    print(D.width, D.length)

    # Width parameter is valid.
    D.width = 0.5
    print(D.width, D.length)

    # Throws a parameter invalid error.
    D.width = 1.1
    print(D.width, D.length)

