

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
        prefix = '{}{}'.format(prefix, self.process_name)
        c = self.names_counters.get(prefix, self.counter)
        c += 1
        self.names_counters[prefix] = c
        c = self.names_counters[prefix]
        return '{}_{}'.format(prefix, c)

    def reset(self):
        self.prefix_attribute = '__name_prefix__'
        self.counter = 0
        self.names_counters = {}

