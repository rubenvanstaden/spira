

class DataTree(object):
    """ A hierarchical tree for storing configuration settings. """

    def __init__(self, overwrite_allowed=[], **kwargs):
        self.__dict__['__config_tree_keys__'] = []

    def __setattr__(self, key, value):
        if (key in self.__dict__) and (key not in ['name', 'desc', '__initialized__']):
            current_value = self.__dict__[key]
            if current_value != value:
                self.__dict__[key] = value
        else:
            self.__dict__[key] = value
            self.__getattribute__('__config_tree_keys__').append(key)

    def __generate_doc__(self, header):
        doc = ''
        keys = self.__dict__.keys()
        for k in keys:
            value = self.__dict__[k]
            if isinstance(value, DataTree):
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
                if isinstance(value, TechnologyTree):
                    items.append(value)
        return items

    def get_key_by_layer(self, layer):
        for k in self.__config_tree_keys__:
            if k in self.__dict__:
                value = self.__dict__[k]
                if isinstance(value, TechnologyTree):
                    if 'LAYER' not in value.keys:
                        raise ValueError('No LAYER in TechnologyTree')
                    if value['LAYER'] == layer.number:
                        return value
        return None

    @property
    def layers(self):
        items = []
        for k in self.__config_tree_keys__:
            if k in self.__dict__:
                value = self.__dict__[k]
                if isinstance(value, TechnologyTree):
                    if 'LAYER' in value.keys:
                        items.append(value['LAYER'])
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
        return self.__dict__[key]


# class FabricationMetaData(DataTree):
class PcellTechnologyTree(DataTree):
    """ TechnologyTree for storing primitive PCell data.
    The tree is initiated when retreiving the data. """
    def __init__(self, **kwargs):
        super(DelayedInitDataTree, self).__init__(**kwargs)
        self.__initialized__ = False

    def __getattr__(self, key):
        if self.__initialized__:
            raise IpcoreAttributeException("No attribute %s of DataTree" % key)
        self.initialize()
        self.__initialized__ = True
        return getattr(self, key)

    def initialize(self):
        raise NotImplementedError()


class TechnologyTree(DataTree):
    """ A hierarchical tree for storing technology settings. """
    pass


class TechnologyLibrary(DataTree):
    """ The fabrication process library """

    def __init__(self, name, description = None, fallback= None, **kwargs):
        super(TechnologyLibrary, self).__init__(fallback = fallback)
        self.name = name
        self.desc = description

    def __repr__(self):
        return "< RDD %s>" % self.name
