
__all__ = [
    'Database',
    'ParameterDatabase',
    'TechnologyLibrary',
    'ProcessLayerDatabase',
    'PurposeLayerDatabase',
    'PhysicalLayerDatabase',
    'LazyDatabase'
]


class __Database__(object):
    """ A hierarchical tree for storing configuration settings. """

    def __init__(self, overwrite_allowed=[], **kwargs):
        self.__dict__['__config_tree_keys__'] = []

    # def __getitem__(self, key):
    #     value = self.__dict__[key]
    #     return value
        
    def __getitem__(self, key):
        value = None
        if key in self.__dict__:
            value = self.__dict__[key]
        else:
            for v in self.values:
                if v.symbol == key:
                    value = v
        return value

    def __setattr__(self, key, value):
        if (key in self.__dict__) and (key not in ['name', 'desc', '__initialized__']):
            current_value = self.__dict__[key]
            if current_value != value:
                self.__dict__[key] = value
        elif (key == 'name') and (value != 'EMPTY'):
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
            if isinstance(value, __Database__):
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


class Database(__Database__):
    """ A hierarchical tree for storing fabrication data. """

    def _get_process_symbol(self, obj):
        from spira.yevon.process.process_layer import ProcessLayer
        if isinstance(obj, ProcessLayer):
            symbol = obj.symbol
        elif isinstance(obj, str):
            symbol = obj
        else:
            raise ValueError('Processes has to be a process symbol or a process object.')
        return symbol

    def get_physical_layers_by_purpose(self, purposes):
        plist = []
        for key in self['PLAYER'].keys:
            if isinstance(self['PLAYER'][key], PhysicalLayerDatabase):
                for value in self['PLAYER'][key].values:
                    if hasattr(value, 'purpose'):
                        if isinstance(purposes, list):
                            for s in purposes:
                                if value.purpose.symbol == s:
                                    plist.append(value)
                        else:
                            if value.purpose.symbol == purposes:
                                plist.append(value)
        # if len(plist) == 0:
        #     raise ValueError('No physical layer with purpose {} found.'.format(purposes))
        return plist

    def get_physical_layers_by_process(self, processes):

        symbols = []
        if isinstance(processes, list):
            for s in processes:
                symbol = self._get_process_symbol(s)
                symbols.append(symbol)
        else:
            symbol = self._get_process_symbol(processes)
            symbols.append(symbol)

        plist = []
        for key in self['PLAYER'].keys:
            if isinstance(self['PLAYER'][key], PhysicalLayerDatabase):
                for value in self['PLAYER'][key].values:
                    for s in symbols:
                        if hasattr(value, 'process'):
                            if value.process.symbol == s:
                                plist.append(value)
        # if len(plist) == 0:
        #     raise ValueError('No physical layer with purpose {} found.'.format(processes))
        return plist


class ParameterDatabase(__Database__):
    """ A hierarchical tree for storing fabrication data. """

    def __repr__(self):
        return '[ParameterDatabase] ({} keys)'.format(len(self.keys))


class TechnologyLibrary(Database):
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


class ProcessLayerDatabase(__Database__):
    """ A hierarchical tree for storing process layer settings. """

    def __repr__(self):
        return '[ProcessLayerDatabase] ({} keys)'.format(len(self.keys))

    def get_process_layers(self):
        from spira.yevon.process.process_layer import ProcessLayer
        pl = []
        for k, v in self.__dict__.items():
            if isinstance(v, ProcessLayer):
                pl.append(v)
        return pl

    def get_key_from_process_layer(self, layer):
        from spira.yevon.process.process_layer import ProcessLayer
        for k, v in self.__dict__.items():
            if isinstance(v, ProcessLayer) and (v == layer):
                return k
        return None


class PurposeLayerDatabase(__Database__):
    """ A hierarchical tree for storing process layer settings. """

    def __repr__(self):
        return '[PurposeLayerDatabase] ({} keys)'.format(len(self.keys))
        
    # def __getitem__(self, key):
    #     if key in self.__dict__:
    #         value = self.__dict__[key]
    #     else:
    #         for v in self.values:
    #             if v.symbol == key:
    #                 value = v
    #     return value

    @property
    def symbols(self):
        symbols = []
        for v in self.values:
            symbols.append(v.symbol)
        return symbols


class PhysicalLayerDatabase(__Database__):
    """ A hierarchical tree for storing process layer settings. """

    def __repr__(self):
        return '[PhysicalLayerDatabase] ({} keys)'.format(len(self.keys))

    def get_physical_layers(self):
        from spira.yevon.process.physical_layer import PhysicalLayer
        pl = []
        for k, v in self.__dict__.items():
            if isinstance(v, PhysicalLayer):
                pl.append(v)
        return pl

    def get_key_from_physical_layer(self, layer):
        from spira.yevon.process.physical_layer import PhysicalLayer
        for k, v in self.__dict__.items():
            if isinstance(v, PhysicalLayer) and (v == layer):
                return k
        return None


class LazyDatabase(__Database__):
    """
    A hierarchical tree for storing configuration settings,
    but with delayed initialisation : the initialize-function
    is called only at the moment a value is actually retrieved.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__initialized__ = False

    def __getattr__(self, key):
        if self.__initialized__:
            raise ValueError('Alread initialized')
        self.initialize()
        self.__initialized__ = True
        return getattr(self, key)

    def initialize(self):
        raise NotImplementedError()





