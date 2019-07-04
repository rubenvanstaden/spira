

class NameGenerator(object):
    """ Generate a unique name based on a counter for every prefix. """

    def __init__(self, prefix_attribute='__name_prefix__', process_name='DEFAULT', counter=0):
        self.prefix_attribute = prefix_attribute
        self.counter = counter
        self.process_name = process_name
        self.names_counters = {}

    def __call__(self, obj):
        if hasattr(obj, self.prefix_attribute):
            prefix = getattr(obj, self.prefix_attribute)
        else:
            prefix = ''
        prefix = '{}_{}'.format(prefix, self.process_name)
        c = self.names_counters.get(prefix, self.counter)
        c += 1
        self.names_counters[prefix] = c
        c = self.names_counters[prefix]
        return '{}_{}'.format(prefix, c)
    
    def reset(self):
        self.prefix_attribute = '__name_prefix__'
        self.counter = 0
        self.names_counters = {}


class PortGenerator(object):
    """ 
    Generate a port name that contains the process to which it connects.
    Syntax: Pname_Process
    """

    def __init__(self, port_name, process=None):
        super().__init__(self, **kwargs)
        self.name_list = port_name.split('_')
        self.ps = self.process.symbol

    @property
    def name(self):
        from spira.yevon.geometry.ports.port import PORT_TYPES
        if len(self.name_list) == 1:
            if self.name_list[0][0] in PORT_TYPES.keys():
                name_string = '{}_{}'.format(self.name_list[0], self.ps)
            else:
                raise ValueError('Port name, \'{}\', not supported'.format(name))

    def _bind_process(self):
        extracted_process = self.original_name.split('_')

        if self.name_list[0] != self.process.symbol:
            error_message = "Port name \'{}\' does not connect to the correct process \'{}\'."
            raise ValueError(error_message.format(name, self.process.symbol))
        
        elif name.split('_')[0] != self.process.symbol:
            error_message = "Port name \'{}\' does not connect to the correct process \'{}\'."
            raise ValueError(error_message.format(name, self.process.symbol))
        else:
            n = name.split('_')[1]
            if n[0] in ['P', 'e', 'c', 'r', 'd']:
                self.name = name
            else:
                raise ValueError('Port name must start with P,e,c,r,d {}'.format(name))

    # def create_name(self):

        



