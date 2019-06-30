from spira.core.parameters.initializer import ParameterInitializer
from spira.core.parameters.variables import StringParameter
from spira.log import SPIRA_LOG as LOG


__all__ = ['Filter', 'ToggledCompoundFilter']


class Filter(ParameterInitializer):
    """

    """

    name = StringParameter(allow_none=True)

    def __call__(self, item):
        if isinstance(item, list):
            L = []
            for v in item: 
                L += self.__call__(v)
            return L
        else:
            return self._filter(item)

    def _filter(self, item):
        import inspect
        T = type(item)
        if inspect.isclass(T):
            for M in inspect.getmro(T):
                N = '__filter_{}__'.format(M.__name__)
                if hasattr(self, N):
                    LOG.debug("Applying method %s of %s to %s" %(N,self,item))
                    return getattr(self, N)(item)
            return self.__filter_default__(item)
        else:
            N = '__filter_{}'.format(T.__name__)
            if hasattr(self, N):
                expr = 'self.{}(item)'.format(N)
                LOG.debug('Executing {}'.format(expr))
                return eval(expr)
            else:
                return self.__filter_default__(item)

    def __filter_default__(self, item):
        return [item]

    def __add__(self, other):
        if isinstance(other, Filter):
            return __CompoundFilter__(filters = [self, other])
        elif other is None:
            return self
        else:
            raise TypeError("Cannot add %s to filter " % type(other))

    def __iadd__(self, other):
        C = self.__add__(other)
        self = C
        return self

    def __repr__(self):
        return "<GDS Primitive Filter>"


class __CompoundFilter__(Filter):
    """

    """

    def __init__(self, filters = [], **kwargs):
        super(__CompoundFilter__,self).__init__(**kwargs)
        self._sub_filters = filters

    def __add__(self, other):
        if isinstance(other, __CompoundFilter__):
            return __CompoundFilter__(name=self.name, filters=self._sub_filters + other.__sub_filters)
        elif isinstance(other, Filter):
            return __CompoundFilter__(name=self.name, filters=self._sub_filters + [other])
        else:
            raise TypeError("Cannot add %s to Filter" % type(other))

    def __iadd__(self, other):
        self.add(other)
        return self

    def add(self, other):
        if isinstance(other, __CompoundFilter__):
            self._sub_filters += other._sub_filter
        elif isinstance(other, Filter):
            self._sub_filters += [other]
        else:
            raise TypeError("Cannot add %s to Filter" % type(other))

    def __call__(self, item):
        LOG.debug("Applying all subfilters. Item = %s" % item)
        v = item
        for R in self._sub_filters:
            LOG.debug("** Applying subfilter %s to %s" % (R, v))
            v = R(v)
            LOG.debug("** Result after filtering = %s\n" % v)
        LOG.debug("Finished applying all subfilters. Item = %s" % item)        
        return v

    def __repr__(self):
        S = "< Compound Filter:"
        for i in self._sub_filters:
            S += "   %s" % i.__repr__() 
        S += ">"
        return S


class ToggledCompoundFilter(__CompoundFilter__):
    """
    Compound filter in which filters can be turned on or off
    by doing filter['filter_name'] = True|False
    """

    def __init__(self, filters=[], **kwargs):
        super().__init__(filters=filters, **kwargs)
        self._filter_status = dict()

    def __setitem__(self, key, item):
        """ dict behaviour: enable or disable a filter based on it's name """
        if not isinstance(key,str):
            raise KeyError("__ToggledCompoundFilter__: key must be of type str, is type %s"%(type(key)))
        if not isinstance(item, bool):
            raise KeyError("__ToggledCompoundFilter__: item must be of type bool, is type %s"%(type(item)))
        self._filter_status[key]=item

    def __getitem__(self, key):
        if not isinstance(key, str):
            raise KeyError("__ToggledCompoundFilter__: key must be of type str, is type %s"%(type(key)))
        if not key in self._filter_status.keys():
            return True
        return self._filter_status[key]

    def __call__(self, item):
        LOG.debug("Applying all subfilters. Item = %s" % item)
        v = item
        k = self._filter_status.keys()
        for R in self._sub_filters:
            if R.name not in k or self._filter_status[R.name]:
                LOG.debug("** Applying subfilter %s to %s"  % (R, v))
                v = R(v)
                LOG.debug("** Result after filtering = %s\n" % v)
        LOG.debug("Finished applying all subfilters. Item = %s" % item)        
        return v

    def __repr__(self):
        S = "< Toggled Compound Filter:"
        for i in self._sub_filters:
            S += "   %s" % i.__repr__() 
            if i.name not in self._filter_status.keys() or self._filter_status[i.name]:
                S += "(enabled)"
            else:
                S += "(disabled)"
        S += ">"
        return S




