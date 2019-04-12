import spira


class __DataTree__(object):
    """ A hierarchical tree for storing configuration settings. """

    def __init__(self, overwrite_allowed=[], **kwargs):
        self.__dict__['__config_tree_keys__'] = []

    def __setattr__(self, key, value):
        if (key in self.__dict__) and (key not in ['name', 'desc', '__initialized__']):
            current_value = self.__dict__[key]
            if current_value != value:
                self.__dict__[key] = value
        elif (key == 'name') and (value != 'EMPTY'):
            # spira.LOG.rdd(text=value)
            self.__dict__[key] = value
            self.__getattribute__('__config_tree_keys__').append(key)
        else:
            self.__dict__[key] = value
            self.__getattribute__('__config_tree_keys__').append(key)

    def __generate_doc__(self, header):
        doc = ''
        keys = self.__dict__.keys()
        for k in keys:
            value = self.__dict__[k]
            if isinstance(value, __DataTree__):
                child_doc = value.__generate_doc__(header.upper() + "." + k.upper())
                doc = doc + child_doc + '\n'
            else:
                if not (k.startswith('__')):
                    doc = doc + header.upper() + '.' + k.upper() + ' = ' + str(value) + '\n'
        return doc

    @property
    def values(self):
        items = []
        for k in self.__config_tree_keys__:
            if k in self.__dict__:
                value = self.__dict__[k]
                items.append(value)
        return items

    @property
    def keys(self):
        keys = []
        for k in self.__config_tree_keys__:
            if k in self.__dict__:
                keys.append(k)
        self.__config_tree_keys__ = keys
        return self.__config_tree_keys__

    @property
    def items(self):
        items = []
        for k in self.__config_tree_keys__:
            if k in self.__dict__:
                # TODO: use namespace tuple
                items.append((k, self.__dict__[k]))
        return items

    def find_item_key(self, item):
        for k in self.__config_tree_keys__:
            if k in self.__dict__:
                if self.__dict__[k] == item:
                    return k

    def __getitem__(self, key):
        value = self.__dict__[key]
        if key == 'LAYER':
            value = spira.Layer(name='M4', number=value)
        return value


class DataTree(__DataTree__):
    """ A hierarchical tree for storing fabrication data. """

    def __repr__(self):
        return '[DataTree] ({} keys)'.format(len(self.keys))


class PhysicalTree(__DataTree__):
    """ A hierarchical tree for storing process layer settings. """

    # def __repr__(self):
    #     return '[PhysicalTree] ({} keys, {} layers)'.format(len(self.keys), len(self.layers))

    def get_physical_layers(self, purposes):
        plist = []
        for k in self.__config_tree_keys__:
            if k in self.__dict__:
                value = self.__dict__[k]
                if isinstance(purposes, list):
                    for purpose in purposes:
                        if value.purpose.symbol == purpose:
                            plist.append(value)
                else:
                    if value.purpose.symbol == purposes:
                        plist.append(value)
        return plist


class ProcessTree(__DataTree__):
    """ A hierarchical tree for storing process layer settings. """

    def __repr__(self):
        return '[ProcessTree] ({} keys, {} layers)'.format(len(self.keys), len(self.layers))

    def get_key_by_layer(self, layer):
        for k in self.__config_tree_keys__:
            if k in self.__dict__:
                value = self.__dict__[k]
                if isinstance(value, ProcessTree):
                    if 'LAYER' not in value.keys:
                        raise ValueError('No LAYER in ProcessTree')
                    if value['LAYER'] == layer.number:
                        return value
        return None

    @property
    def layers(self):
        items = []
        for k in self.__config_tree_keys__:
            if k in self.__dict__:
                value = self.__dict__[k]
                if isinstance(value, ProcessTree):
                    if 'LAYER' in value.keys:
                        items.append(value['LAYER'])
        return items


# from spira.core.descriptor import DataFieldDescriptor
# def ProcessTreeField(name='', datatype=0, symbol=''):
#     F = ProcessTree(name=name, datatype=datatype, symbol='')
#     return DataFieldDescriptor(default=F)


class TechnologyLibrary(__DataTree__):
    """ The fabrication process library """

    def __init__(self, name, description = None, fallback= None, **kwargs):
        super(TechnologyLibrary, self).__init__(fallback = fallback)
        self.name = name
        self.desc = description

    def __repr__(self):
        return '<RDD {}>'.format(self.name)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        else:
            raise ValueError('Not Implemented!')

    def __neq__(self, other):
        if isinstance(other, str):
            return self.name != other
        else:
            raise ValueError('Not Implemented!')


class DynamicDataTree(__DataTree__):
    """
    A hierarchical tree for storing configuration settings,
    but with delayed initialisation : the initialize-function
    is called only at the moment a value is actually retrieved.
    """
    def __init__(self, **kwargs):
        super(DynamicDataTree, self).__init__(**kwargs)
        self.__initialized__ = False

    def __getattr__(self, key):
        if self.__initialized__:
            raise ValueError('Alread initialized')
        self.initialize()
        self.__initialized__ = True
        return getattr(self, key)

    def initialize(self):
        raise NotImplementedError()





