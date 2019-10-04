from spira.core.parameters.initializer import ParameterInitializer
from spira.core.parameters.variables import StringParameter
from spira.log import SPIRA_LOG as LOG


__all__ = ['Filter', 'ToggledCompositeFilter']


# NOTE: Device and Circuit metal labeling can only be done in Mask Filter,
# since we first want to implement ERC with metal, then convert it afterwards.


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

    def __add__(self, other):
        if isinstance(other, Filter):
            return _CompositeFilter(filters=[self, other])
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

    def _filter(self, item):
        import inspect
        T = type(item)
        if inspect.isclass(T):
            for M in inspect.getmro(T):
                N = 'filter_{}'.format(M.__name__)
                if hasattr(self, N):
                    LOG.debug("Applying method %s of %s to %s" %(N,self,item))
                    return getattr(self, N)(item)
            return self._filter_default(item)
        else:
            N = 'filter_{}'.format(T.__name__)
            if hasattr(self, N):
                expr = 'self.{}(item)'.format(N)
                LOG.debug('Executing {}'.format(expr))
                return eval(expr)
            else:
                return self._filter_default(item)

    def _filter_default(self, item):
        return [item]


class _CompositeFilter(Filter):
    """

    """

    def __init__(self, filters=[], **kwargs):
        super().__init__(**kwargs)
        self._sub_filters = filters

    def __call__(self, item):
        LOG.debug("Applying all subfilters. Item = %s" % item)
        v = item
        for R in self._sub_filters:
            LOG.debug("** Applying subfilter %s to %s" % (R, v))
            v = R(v)
            LOG.debug("** Result after filtering = %s\n" % v)
        LOG.debug("Finished applying all subfilters. Item = %s" % item)        
        return v

    def __add__(self, other):
        if isinstance(other, _CompositeFilter):
            return _CompositeFilter(name=self.name, filters=self._sub_filters + other.__sub_filters)
        elif isinstance(other, Filter):
            return _CompositeFilter(name=self.name, filters=self._sub_filters + [other])
        else:
            raise TypeError("Cannot add %s to Filter" % type(other))

    def __iadd__(self, other):
        self.add(other)
        return self

    def __repr__(self):
        S = "< Compound Filter:"
        for i in self._sub_filters:
            S += "   %s" % i.__repr__() 
        S += ">"
        return S

    def add(self, other):
        if isinstance(other, _CompositeFilter):
            self._sub_filters += other._sub_filter
        elif isinstance(other, Filter):
            self._sub_filters += [other]
        else:
            raise TypeError("Cannot add %s to Filter" % type(other))


class ToggledCompositeFilter(_CompositeFilter):
    """
    Compound filter in which filters can be turned on or off
    by doing filter['filter_name'] = True|False
    """

    # FIXME: Have to hard reset filters=[] when instantiating.

    def __init__(self, filters=[], **kwargs):
        _CompositeFilter.__init__(self, filters=filters, **kwargs)
        self._filter_status = dict()

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

    def __setitem__(self, key, item):
        """ dict behaviour: enable or disable a filter based on it's name """
        if not isinstance(key, str):
            raise KeyError("__ToggledCompoundFilter__: key must be of type str, is type %s"%(type(key)))
        if not isinstance(item, bool):
            raise KeyError("__ToggledCompoundFilter__: item must be of type bool, is type %s"%(type(item)))
        self._filter_status[key] = item

    def __getitem__(self, key):
        if not isinstance(key, str):
            raise KeyError("__ToggledCompoundFilter__: key must be of type str, is type %s"%(type(key)))
        if not key in self._filter_status.keys():
            return True
        return self._filter_status[key]

    def __repr__(self):
        S = "< Toggled Compound Filter:"
        for i in self._sub_filters:
            S += "\n  {}".format(i.__repr__())
            if i.name not in self._filter_status.keys() or self._filter_status[i.name]:
                S += "    (enabled)"
            else:
                S += "    (disabled)"
        S += ">"
        return S




