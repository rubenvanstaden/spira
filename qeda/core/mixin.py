

class MetaMixinBowl(type):
    """ Base SPiRA metaclass. """
    def mixin(cls, mixin_class):
        if not mixin_class in cls.__bases__:
            if cls.__bases__ == (object,):
                cls.__bases__ = (mixin_class,)
            else:
                cls.__bases__ = (mixin_class,) + cls.__bases__


class MixinBowl(metaclass=MetaMixinBowl):
    """ Base mixin class for the SPiRA framework. """
    pass
