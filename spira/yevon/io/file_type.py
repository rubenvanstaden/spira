from spira.core.parameters.initializer import ParameterInitializer
from spira.core.parameters.variables import StringParameter


class FileType(ParameterInitializer):
    """  """

    name = StringParameter(default='')
    doc = StringParameter(default='')
    
    def __str__(self):
        return self.name


GDSII = FileType(name='GDSII', doc='GDSII file format.')
SPICE = FileType(name='SPICE', doc='JoSIM file format.')
LEFDEF = FileType(name='LEFDEF', doc='LEF and DEF file format.')



