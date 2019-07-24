import spira.all as spira
import spira.core.parameters.processors as processors


class Resistor(spira.PCell):

    width = spira.NumberParameter(default=spira.RDD.R1.MIN_WIDTH, doc='Width of the shunt resistance.')
    length = spira.NumberParameter(default=spira.RDD.R1.MIN_LENGTH, doc='Length of the shunt resistance.')

    def validate_parameters(self):
        if self.width > self.length:
            raise ValueError('`Width` cannot be larger than `length`.')
        return True


def test_type_float():
    D = Resistor()
    print(processors.ProcessorInt())

test_type_float()