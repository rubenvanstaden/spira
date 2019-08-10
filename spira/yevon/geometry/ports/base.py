import gdspy
import pyclipper
import numpy as np
import spira.all as spira

from numpy.linalg import norm
from spira.core.parameters.variables import *
from spira.core.parameters.initializer import ParameterInitializer, MetaInitializer
from spira.core.parameters.descriptor import Parameter
from spira.yevon.geometry.coord import Coord
from spira.yevon.process.process_layer import ProcessParameter
from spira.yevon.process.purpose_layer import PurposeLayerParameter
from spira.yevon.process.physical_layer import PLayer
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


class MetaPort(MetaInitializer):
    """ Called when an instance of a SPiRA Port is created. """

    def get_port_data(self, kwargs):

        if 'name' in kwargs:
            if (kwargs['name'] is None) or (kwargs['name'] == ''):
                raise ValueError('Port name cannot be generated.')

            name = kwargs['name']
            name_list = name.split(':')

            port_data = {}
            port_data['name'] = name
            port_data['purpose_symbol'] = name_list[-1][0]
    
            if len(name_list) == 1:
                port_data['process_symbol'] = None
            elif len(name_list) > 1:
                port_data['process_symbol'] = name_list[-2]
        else: 
            error_message = "Port name format must be: \'port_data_Process\' or \'port_data\'"
            raise ValueError(error_message)

        return port_data

    def _bind_purpose(self, kwargs):
        """
        The purpose of a port is automatically extracted from the name.

        Examples
        --------
        >>> port = spira.Port(name='E1', process=RDD.PROCESS.R1)
        >>> port.purpose
        EdgePort

        >>> port = spira.Port(name='P1', process=RDD.PROCESS.R1)
        >>> port.purpose
        PinPort
        """
        port_data = self.get_port_data(kwargs)
        pr = port_data['purpose_symbol']
        if pr not in RDD.PURPOSE.PORT.symbols:
            error_message = "Port name, \'{}\', not supported. Has to start with {}"
            raise ValueError(error_message.format(pr, RDD.PURPOSE.PORT.symbols))
        purpose = RDD.PURPOSE.PORT[pr]
        return purpose

    def _bind_process_to_name(self, kwargs):
        """
        Add process symbol to port name. If no process
        parameter is given, throw an error. 

        Example
        -------
        >>> port = spira.Port(name='P1')
        Value Error: Process not defined.
        >>> port = spira.Port(name='P1', process=RDD.PROCESS.R1)
        >>> (port.name, port.process)
        (P1_R1, R1)
        """
        port_data = self.get_port_data(kwargs)
        if 'process' not in kwargs:
            error_message = "Cannot connect port \'{}\' to a process."
            raise ValueError(error_message.format(port_data['name']))
        process = kwargs['process']
        name = '{}:{}'.format(process.symbol, port_data['name'])
        return name, process

    def _bind_name_to_process(self, kwargs):
        """
        Automatically extract the process from the port name.

        Example
        -------
        >>> port = spira.Port(name='P1_M1')
        >>> (port.name, port.process)
        (P1_M1, M1)
        """

        port_data = self.get_port_data(kwargs)
        pc = port_data['process_symbol']
        if 'process' in kwargs:
            if pc != kwargs['process'].symbol:
                error_message = "Port name \'{}\' does not connect to the correct process \'{}\'."
                raise ValueError(error_message.format(pc, kwargs['process'].symbol))
            process = kwargs['process']
        else:
            if pc not in RDD.PROCESS.keys:
                error_message = "Process not found in database \'{}\'."
                raise ValueError(error_message.format(RDD.name))
            process = RDD.PROCESS[pc]
        name = kwargs['name']
        return name, process

    def __call__(cls, *params, **keyword_params):

        kwargs = cls.__map_parameters__(*params, **keyword_params)

        port_data = cls.get_port_data(kwargs)

        purpose = cls._bind_purpose(kwargs)

        if port_data['process_symbol'] is None:
            name, process = cls._bind_process_to_name(kwargs)
        else:
            name, process = cls._bind_name_to_process(kwargs)

        if name is not None:
            kwargs['name'] = name
        if process is not None:
            kwargs['process'] = process
        if purpose is not None:
            kwargs['purpose'] = purpose
        kwargs['alias'] = name.split(':')[-1]

        cls = super().__call__(**kwargs)
        cls.__keywords__ = kwargs

        return cls


class __Port__(ParameterInitializer, metaclass=MetaPort):
    """  """

    doc = StringParameter()
    name = StringParameter(doc='The full name tree of the port.')
    alias = StringParameter(doc='The name of the port without the tree hierarchy.')
    process = ProcessParameter(allow_none=True, default=None)
    purpose = PurposeLayerParameter(allow_none=True, default=None)
    text_type = NumberParameter(default=RDD.GDSII.TEXT)
    local_pid = StringParameter(default='none_local_pid')

    def __add__(self, other):
        """
        >>> midpoint = self.jj1.ports['P2'] + [-5, 0]
        """
        if other is None: return self
        p1 = Coord(self.midpoint[0], self.midpoint[1]) + Coord(other[0], other[1])
        return p1

    def __sub__(self, other):
        """
        >>> midpoint = self.jj1.ports['P2'] - [-5, 0]
        """
        if other is None: return self
        p1 = Coord(self.midpoint[0], self.midpoint[1]) - Coord(other[0], other[1])
        return p1

    # TODO: Maybe make this a getter and setter?
    @property
    def layer(self):
        return PLayer(self.process, self.purpose)

    def flat_copy(self, level=-1):
        """ Return a flattened copy of the port. """
        port = self.copy(transformation=self.transformation)
        port.transform_copy(self.transformation)
        return port

    def encloses(self, points):
        """ Return `True` if the port is inside the shape. """
        from spira.yevon.utils import clipping
        return clipping.encloses(coord=self.midpoint.snap_to_grid(), points=points)

    def move(self, coordinate):
        """ Move the port midpoint to coordinate. """
        self.midpoint.move(coordinate)
        return self

    def distance(self, other):
        """ Get the absolute distance between two ports. """
        return norm(np.array(self.midpoint) - np.array(other.midpoint))



