from spira.core.typed_list import TypedList
from spira.core.transformable import Transformable
from spira.core.parameters.variables import FloatParameter
from spira.core.parameters.descriptor import ParameterDescriptor
from spira.core.parameters.restrictions import RestrictType
from spira.yevon.geometry.ports.base import __Port__


__all__ = ['PortList', 'PortListParameter']


class PortList(TypedList, Transformable):
    __item_type__ = __Port__

    # port_angle_decision = FloatParameter(default=0.0)
    port_angle_decision = FloatParameter(default=90.0)

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
            return self.get_port_from_label(key)

    def __contains__(self, item):
        for p in self._list:
            # if p.name == item.name:
            if p == item:
                return True
        return False

    def __delitem__(self, key):
        for i in range(0, len(self._list)):
            if self._list[i] is key:
                return list.__delitem__(self._list, i)

    def __sub__(self, other):
        pass

    def __or__(self, other):
        pass

    def union(self, other):
        return self.__or__(self, other)

    def intersection(self, other):
        return self.__and__(self, other)

    def difference(self, other):
        return self.__sub__(self, other)

    def update_layercopy(self, layer):
        P = self.__class__()
        for p in self._list:
            p.edgelayer = layer
            P.append(p)
        return P

    def flat_copy(self, level=-1):
        el = PortList()
        for e in self._list:
            el += e.flat_copy(level)
        return el

    def move(self, position):
        for c in self._list:
            c.move(position)
        return self

    def move_copy(self, position):
        T = self.__class__()
        for c in self._list:
            T.append(c.movecopy(position))
        return T

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
            L += c.invertcopy()
        return L

    def x_sorted(self):
        return self.__class__(sorted(self._list, key=lambda f: f.position[0]))

    def x_sorted_backward(self):
        return self.__class__(sorted(self._list, key=lambda f: (-f.position[0])))

    def y_sorted(self):
        return self.__class__(sorted(self._list, key=lambda f: f.position[1]))

    def y_sorted_backward(self):
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
            raise AttributeError("Direction should be NORTH, EAST, SOUTH or WEST")

    def angle_sorted(self, reference_angle=0.0):
        """ sorts ports by angle, using angles between the reference_angle and reference_angle+360 """
        return self.__class__(sorted(self._list, key=lambda f: ((f.orientation - reference_angle) % 360.0)))

    def angle_sorted_backward(self, reference_angle=0.0):
        """ sorts ports by angle, using angles between the reference_angle and reference_angle+360 """
        return self.__class__(sorted(self._list, key=lambda f: (-(f.orientation - reference_angle) % 360.0)))

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
        for p in self._list:
            a = (p.orientation - sa) % 360.0
            if a <= aspread: pl.append(p)
        return pl    

    def get_ports_on_process(self, process):
        pl = self.__class__()
        for p in self._list:
            if p.process == process: 
                pl.append(p)
        return pl
        
    def get_ports_by_purpose(self, purpose):
        pl = self.__class__()
        for p in self._list:
            if p.purpose == purpose: 
                pl.append(p)
        return pl
        
    def get_ports_by_type(self, port_type):
        pl = self.__class__()
        if port_type == 'D':
            for p in self._list:
                if p.name[0] == 'D':
                    pl.append()
        return pl

    @property
    def west_ports(self):
        start_angle = 180.0 - 0.5 * self.port_angle_decision
        end_angle = 180.0 + 0.5 * self.port_angle_decision
        return self.get_ports_within_angles(start_angle, end_angle)

    @property
    def east_ports(self):
        start_angle = -0.5 * self.port_angle_decision
        end_angle = +0.5 * self.port_angle_decision
        return self.get_ports_within_angles(start_angle, end_angle)

    @property
    def north_ports(self):
        start_angle = 90.0 - 0.5 * self.port_angle_decision
        end_angle = 90.0 + 0.5 * self.port_angle_decision
        return self.get_ports_within_angles(start_angle, end_angle)

    @property
    def south_ports(self):
        start_angle = 270.0 - 0.5 * self.port_angle_decision
        end_angle = 270.0 + 0.5 * self.port_angle_decision
        return self.get_ports_within_angles(start_angle, end_angle)

    @property
    def unlock(self):
        """ Unlock the edge and convert it to a port. """
        for i, p in enumerate(self._list):
            name = p.name.replace('E', 'P')
            self._list[i] = p.copy(name=name)
        return self


class PortListParameter(ParameterDescriptor):
    from spira.yevon.geometry.ports.port_list import PortList
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
        self.__cache_parameter_value__(obj, value)
        new_value = self.__get_parameter_value__(obj)
        return new_value

    def __cache_parameter_value__(self, obj, ports):
        if isinstance(ports, self.__type__):
            super().__cache_parameter_value__(obj, ports)
        elif isinstance(ports, list):
            super().__cache_parameter_value__(obj, self.__type__(ports))           
        else:
            raise TypeError("Invalid type in setting value of PortListParameter: " + str(type(ports)))

    def __set__(self, obj, ports):
        if isinstance(ports, self.__type__):
            self.__externally_set_parameter_value__(obj, ports)
        elif isinstance(ports, list):
            self.__externally_set_parameter_value__(obj, self.__type__(ports))            
        else:
            raise TypeError("Invalid type in setting value of PortListParameter: " + str(type(ports)))
        return


