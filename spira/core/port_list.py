# from spira.core import param
from spira.core.param.field.typed_list import TypedList
# from spira.core.transformable import Transformable
from spira.core.param.variables import FloatField
from spira.core.descriptor import DataFieldDescriptor
from spira.core.param.restrictions import RestrictType


# class PortList(TypedList, Transformable):
class PortList(TypedList):

    port_angle_decision = FloatField(default = 90.0)

    def __repr__(self):
        if len(self._list) == 0:
            print('PortList is empty')
        return '\n'.join('{}'.format(k) for k in enumerate(self._list))

    def __str__(self):
        return self.__repr__()

    def __getitem__(self, key):
        from spira.yevon.geometry.ports.base import __Port__
        if isinstance(key, int):
            return self._list[key]
        elif isinstance(key, str):
            for p in self._list:
                if p.name == key:
                    return p
        elif issubclass(type(key), __Port__):
            for p in self._list:
                if p == key:
                    return p
        else:
            return self.get_from_label(key)

    def __contains__(self, item):
        # print(item)
        for p in self._list:
            # if p.name == item.name:
            if p == item:
                # print('TRUE')
                return True
        return False

    def __delitem__(self, key):
        for i in range(0, len(self._list)):
            if self._list[i] is key:
                return list.__delitem__(self._list, i)

    def flat_copy(self, level = -1):
        el = PortList()
        for e in self._list:
            el += e.flat_copy(level)
        return el

    # def move(self, position):
    #     for c in self._list:
    #         c.move(position)
    #     return self

    # def move_copy(self, position):
    #     T = self.__class__()
    #     for c in self._list:
    #         T.append(c.move_copy(position))
    #     return T

    def transform_copy(self, transformation):
        T = self.__class__()
        for c in self._list:
            T.append(c.transform_copy(transformation))
        return T

    def transform(self, transformation):
        for c in self._list:
            c.transform(transformation)
        return self

    def invert(self):
        for c in self._list:
            c.invert()
        return self

    def invert_copy(self):
        L = self.__class__()
        for c in self._list:
            L += c.invert_copy()
        return L

    def x_sorted(self):
        """return a copy of the list sorted on the x position"""
        return self.__class__(sorted(self._list, key=lambda f: f.position[0]))

    def x_sorted_backward(self):
        """return a copy of the list reverse sorted on the x position"""
        return self.__class__(sorted(self._list, key=lambda f: (-f.position[0])))

    def y_sorted(self):
        """return a copy of the list sorted on the y position"""
        return self.__class__(sorted(self._list, key=lambda f: f.position[1]))

    def y_sorted_backward(self):
        """return a copy of the list reverse sorted on the y position"""
        return self.__class__(sorted(self._list, key=lambda f: (-f.position[1])))

    def sorted_in_direction(self, direction):
        if direction == NORTH:
            return self.y_sorted()
        elif direction == SOUTH:
            return self.y_sorted_backward()
        elif direction == EAST:
            return self.x_sorted()
        elif direction == WEST:
            return self.x_sorted_backward()
        else:
            raise AttributeError("direction in OpticalPortList.sorted_in_direction() should be NORTH, EAST, SOUTH or WEST")

    def angle_sorted(self, reference_angle=0.0):
        """ sorts ports by angle, using angles between the reference_angle and reference_angle+360 """
        return self.__class__(sorted(self._list, key=lambda f: ((f.angle_deg - reference_angle) % 360.0)))

    def angle_sorted_backward(self, reference_angle=0.0):
        """ sorts ports by angle, using angles between the reference_angle and reference_angle+360 """
        return self.__class__(sorted(self._list, key=lambda f: (-(f.angle_deg - reference_angle) % 360.0)))

    @property
    def terminal_ports(self):
        from spira.yevon.gdsii.term import Term
        pl = self.__class__()
        for p in self._list:
            if isinstance(p, Term):
                pl.append(p)
        return pl

    def get_names(self):
        names = []
        for p in self._list:
            names.append(p.name)
        return names

    def get_ports_within_angles(self, start_angle, end_angle):
        pl = self.__class__()
        aspread = (end_angle - start_angle) % 360.0
        sa = start_angle % 360.0
        ea = sa + aspread
        for p in self:
            if isinstance(p, __OutOfPlanePort__):
                continue
            a = (p.angle_deg - sa) % 360.0
            if a <= aspread: pl.append(p)
        return pl    

    def get_ports_on_process(self, process):
        pl = self.__class__()
        for p in self._list:
            if p.process == process: 
                pl.append(p)
        return pl

    def get_ports_from_labels(self, labels):
        P = self.__class__()
        for i in labels:
            P += self.get_from_label(i)
        return P

    def get_from_label(self, label):
        D = label[0]
        if D == "I":
            portl = self.in_ports
        elif D == "O":
            portl = self.out_ports
        elif D == "N":
            portl = self.north_ports.x_sorted()
        elif D == "S":
            portl = self.south_ports.x_sorted()
        elif D == "W":
            portl = self.west_ports.y_sorted()
        elif D == "E":
            portl = self.east_ports.y_sorted()
        else:
            raise AttributeError("Invalid Port label: %s" % label)
        if label[1:] == "*":
            port = portl
        else:
            N = int(label[1:])
            port = portl[N] 
        return port

    @property
    def west_ports(self):
        return self.get_ports_within_angles(180.0 - 0.5 * self.port_angle_decision, 180.0 + 0.5 * self.port_angle_decision)

    @property
    def east_ports(self):
        return self.get_ports_within_angles(-0.5 * self.port_angle_decision, +0.5 * self.port_angle_decision)

    @property
    def north_ports(self):
        return self.get_ports_within_angles(90.0 - 0.5 * self.port_angle_decision, 90.0 + 0.5 * self.port_angle_decision)

    @property
    def south_ports(self):
        return self.get_ports_within_angles(270.0 - 0.5 * self.port_angle_decision, 270.0 + 0.5 * self.port_angle_decision)


class PortListField(DataFieldDescriptor):
    from spira.core.port_list import PortList
    __type__ = PortList

    def __init__(self, default=[], **kwargs):
        kwargs['default'] = self.__type__(default)
        kwargs['restrictions'] = RestrictType([self.__type__])
        super().__init__(**kwargs)

    def __repr__(self):
        return ''

    def __str__(self):
        return ''

    def call_param_function(self, obj):
        f = self.get_param_function(obj)
        value = f(self.__type__())
        if value is None:
            value = self.__type__()
        obj.__store__[self.__name__] = value
        return value
