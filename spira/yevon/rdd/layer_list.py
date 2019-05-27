from spira.core.typed_list import TypedList
from spira.yevon.rdd.gdsii_layer import __Layer__, Layer


__all__ = ['LayerList']


class LayerList(TypedList):
    """
    Overload acces routines to get dictionary behaviour 
    but without using the name as primary key.
    """

    __item_type__ = __Layer__

    def __getitem__(self, key):
        if isinstance(key, int):
            for i in self._list:
                if i.id() == key: 
                    return i
            raise IndexError("layer " + str(key) + " cannot be found in LayerList.")
        elif isinstance(key, str):
            for i in self._list:
                if i.name == key: 
                    return i
            raise IndexError("layer " + str(key) + " cannot be found in LayerList.")
        else:
            raise TypeError("Index is wrong type " + str(type(key)) + " in LayerList")

    def __setitem__(self, key, value):
        if isinstance(key, int):
            for i in range(0, len(self)):
                if self._list[i].id() == key: 
                    return list.__setitem__(self, i, value)
            list.append(self, value)
        elif isinstance(key, str):
            for i in range(0, len(self)):
                if self._list[i].name == key: 
                    return list.__setitem__(self, i, value)
            list.append(self, value)
        else:
            raise TypeError("Index is wrong type " + str(type(key)) + " in LayerList")

    def __delitem__(self, key):
        if isinstance(key, int):
            for i in range(0, len(self)):
                if list.__getitem__(self,i).id() == key: 
                    return list.__delitem__(self,i)
                return
            return list.__delitem__(self,key)
        if isinstance(key, str):
            for i in range(0, len(self)):
                if list.__getitem__(self,i).name == key: 
                    return list.__delitem__(self,i)
                return
            return list.__delitem__(self,key)
        else:
            raise TypeError("Index is wrong type " + str(type(key)) + " in LayerList")

    def __contains__(self, item):
        if isinstance(item, Layer):
            id = item.id()
        elif isinstance(item, int):
            id = item
        elif isinstance(item, str):
            for i in self._list:
                if i.name == name: 
                    return True
            return False

        if isinstance(id, int):
            for i in self._list:
                if i.id() == id: 
                    return True
            return False

    def __fast_get_layer__(self, key):
        for L in self._list:
            if L.key == key:
                return L
        return None

    def index(self, item):
        if isinstance(item, Layer):
            id = item.id()
        elif isinstance(item, int):
            id = item

        if isinstance(id, int):
            for i in range(0, len(self)):
                if list.__getitem__(self, i).id() == id:
                    return i
            raise ValueError("layer " + id + " is not in LayerList")
        if isinstance(item, str):
            for i in range(0, len(self)):
                if list.__getitem__(self, i).name == item:
                    return i
            raise ValueError("layer " + item + " is not in LayerList")
        else:
            raise ValueError("layer " + item + " is not in LayerList")

    def add(self, item, overwrite=False):
        if isinstance(item, Layer):
            if not item in self._list:
                list.append(self,item)
            elif overwrite:
                self._list[item.id()] = item
                return
        elif isinstance(item, LayerList) or isinstance(item, list):
            for s in item:
                self.add(s, overwrite)
        elif isinstance(item, int):
            if overwrite or (not item in self):
                self.add(Layer(item), overwrite)
        else:
            raise ValueError('Invalid layer list item type.')

    def append(self, other, overwrite = False):
        return self.add(other, overwrite)

    def extend(self, other, overwrite = False):
        return self.add(other, overwrite)

    def clear(self):
        del self._list[:]

    def __eq__(self, other):
        return set(self) == set(other)

    def __hash__(self):
        return do_hash(self)


LAYER_LIST = LayerList()



