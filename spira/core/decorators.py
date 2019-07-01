import hashlib


__all__ = ['cache', 'parameter']


def cache():
    """ Caching decorator for caching the result of a 
    function called on an object. If not in cache call 
    the underlying function, then case the result """
    def _cache(function):
        def __cache(*args, **kw):
            fstring = function.__name__.encode('utf-8')
            key = hashlib.sha1(fstring).hexdigest()
            obj = args[0]
            if not hasattr(obj, '__SPIRA_CACHE__'):
                obj.__SPIRA_CACHE__ = dict()

            if key in obj.__SPIRA_CACHE__:
                return obj.__SPIRA_CACHE__[key]

            result = function(*args, **kw)
            obj.__SPIRA_CACHE__[key] = result
            return result
        return __cache
    return _cache


def parameter(object):
    """ Parameter decorator for getter and setter methods. """
    pass


