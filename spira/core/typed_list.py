from spira.core.parameters.initializer import FieldInitializer


class TypedList(FieldInitializer, list):
    """

    """

    __item_type__ = object

    def __init__(self, items=[]):
        self._list = []
        if isinstance(items, list) or isinstance(items, set):
            self.extend(items)
        else:
            self.append(items)
        super().__init__()

    def __repr__(self):
        return '\n'.join('{}'.format(k) for k in enumerate(self._list))

    def __str__(self):
        return str(self._list)

    def __getitem__(self, i):
        return self._list[i]

    def __setitem__(self, i, v):
        self._list[i] = v

    def __iter__(self):
        for i in self._list:
            yield i

    def __len__(self):
        return len(self._list)

    def __add__(self, other):
        L = self.__class__(self._list)
        if isinstance(other, list):
            L.extend(other)
        else:
            L.append(other)
        return L

    def __radd__(self, other):
        if isinstance(other, self.__item_type__):
            L = self.__class__([other])
            L.extend(self._list)
        elif isinstance(other, list):
            L = self.__class__(other)
            L.extend(self._list)
        return L

    def __iadd__(self, other):
        if isinstance(other, list):
            self.extend(other)
        else:
            self.append(other)
        return self

    def clear(self):
        del self._list[:]

    # def insert(self, i, v):
    #     self._list.insert(i, v)

    # # def append(self, val):
    # #     self.insert(len(self._list), val)
        
    # # def append(self, item):
    # #     self._list.append(item)

    # def extend(self, items):
    #     self._list.extend(items)
        
    # def append(self, val):
    #     print('jwefbwejfkbk')
    #     print(self._list)
    #     print(type(val))
    #     # self.insert(len(self._list), val)
    #     self._list.append(val)
    #     print(self._list)

    def append(self, item):
        if isinstance(item, self.__item_type__):
            # list.append(self, item)
            self._list.append(item)
        else:
            raise ValueError("You are trying to add an element of type {} to {}. " + 
                "You can only add elements of type {}.".format(str(type(item)), str(self.__class__), str(self.__item_type__)))

    def extend(self, items):
        if type(self) == type(items):
            # list.extend(self, items)
            self._list.extend(items)
        elif isinstance(items, list) or isinstance(items, set):
            for i in items:
                # list.append(self, i)  # type will be checked in the 'append' function
                self._list.append(i)  # type will be checked in the 'append' function
        else:
            raise Exception("TypedList::extend should be used with a list as argument. Current argument if of type %s, which is not a list." % str(type(item)))

    def __deepcopy__(self, memo):
        from copy import deepcopy
        L = self.__class__()
        for item in self._list:
            L.append(deepcopy(item))
        return L


class TypedListField(FieldInitializer):
    """ Parameter type for storing a typed list. """

    __list_type__ = TypedList

    def __init__(self, internal_member_name=None, **kwargs):
        kwargs["restriction"] = RestrictType(allowed_types=[self.__list_type__])
        super(TypedListProperty, self).__init__(internal_member_name=internal_member_name, **kwargs)

    def __call_getter_function__(self, obj):
        f = self.__get_getter_function__(obj)
        value = f(self.__list_type__())
        if (value is None):
            value = self.__list_type__()
        self.__cache_property_value_on_object__(obj, value)
        value = self.__get_property_value_of_object__(obj)
        return value

    def __cache_property_value_on_object__(self, obj, objects):
        if isinstance(objects, self.__list_type__):
            super(TypedListProperty, self).__cache_property_value_on_object__(obj, objects)
        elif isinstance(objects, list):
            super(TypedListProperty, self).__cache_property_value_on_object__(obj, self.__list_type__(objects))
        else:
            raise TypeError("Invalid type in setting value of %s (expected %s), but generated : %s" % (self.__class__, self.__list_type__, str(type(objects))))

    def __set__(self, obj, objects):
        if isinstance(objects, self.__list_type__):
            self.__externally_set_property_value_on_object__(obj, objects)
        elif isinstance(objects, list):
            self.__externally_set_property_value_on_object__(obj, self.__list_type__(objects))
        else:
            raise TypeError("Invalid type in setting value of %s (expected %s): %s" % (self.__class_, self.__list_type__, str(type(objects))))
        return





# import collections
# # from spira.core.parameters.initializer import FieldInitializer


# # class TypedList(FieldInitializer, collections.abc.MutableSequence):
# class TypedList(collections.abc.MutableSequence):
# # class TypedList(list):
#     __item_type__ = object

#     def __init__(self, items=[]):
#         super().__init__()
#         self._list = list(items)

#     def __repr__(self):
#         return '\n'.join('{}'.format(k) for k in enumerate(self._list))

#     def __str__(self):
#         return str(self._list)

#     def __add__(self, other):
#         L = self.__class__(self)
#         if other:
#             if isinstance(other, list):
#                 L.extend(other)
#             else:
#                 L.append(other)
#         return L

#     def __radd__(self, other):
#         L = self.__class__(other)
#         if other:
#             if isinstance(other, self.__item_type__):
#                 L = self.__class__([other])
#                 L.extend(self)
#             elif isinstance(other, list):
#                 L.extend(self)
#         return L

#     def __iadd__(self, other):
#         if other:
#             if isinstance(other, list):
#                 self.extend(other)
#             else:
#                 self.append(other)
#         return self

#     def __len__(self):
#         return len(self._list)

#     def __getitem__(self, i):
#         return self._list[i]

#     def __setitem__(self, i, v):
#         self._list[i] = v

#     def __deepcopy__(self, memo):
#         from copy import deepcopy
#         L = self.__class__()
#         for item in self._list:
#             L.append(deepcopy(item))
#         return L

#     def check(self, v):
#         if not isinstance(v, self.oktypes):
#             raise TypeError('Invalid type')

#     def insert(self, i, v):
#         self._list.insert(i, v)

#     def append(self, val):
#         self.insert(len(self._list), val)
#         # self._list.append(val)

#     @property
#     def value(self):
#         value_list = []
#         for i in self._list:
#             if isinstance(i, float):
#                 value_list.append(i._val)
#         return value_list

#     def clear(self):
#         del self[:]


# from spira.core.parameters.descriptor import DataFieldDescriptor
# class ListField(DataFieldDescriptor):
#     __type__ = TypedList

#     def __init__(self, default=[], **kwargs):
#         kwargs['default'] = self.__type__(default)
#         super().__init__(**kwargs)

#     def __get_parameter_value__(self, obj):
#         value = obj.__store__[self.__name__]
#         return list(value)

#     def __set__(self, obj, value):
#         if isinstance(value, self.__type__):
#             obj.__store__[self.__name__] = value
#         elif isinstance(value, list):
#             obj.__store__[self.__name__] = self.__type__(items=value)
#         else:
#             raise TypeError("Invalid type in setting value " + 
#                             "of {} (expected {}): {}"
#                             .format(self.__class_, type(value)))



