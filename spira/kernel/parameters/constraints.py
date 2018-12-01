# from spira.kernel.parameters.descriptor import DataFieldDescriptor


# class BaseConstraint(DataFieldDescriptor):

#     def __init__(self, default, **kwargs):
#         kwargs['default'] = default
#         super().__init__(**kwargs)


# class CheckConstraint(BaseConstraint):

#     def __init__(self, default, **kwargs):
#         __type__ = type(default)
#         self.allowed = set()
#         self.allowed.add(__type__)
#         super().__init__(default=default, **kwargs)


