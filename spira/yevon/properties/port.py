from spira.yevon.properties.base import __Properties__
from spira.core.port_list import PortListField


class PortProperties(__Properties__):
    """ Port properties that connects to layout structures. """

    ports = PortListField(fdef_name='create_ports', doc='List of ports to be added to the cell instance.')

    def create_ports(self, ports):
        return ports

    @property
    def terms(self):
        from spira.yevon.geometry.ports.term import Term
        from spira.core.elem_list import ElementList
        terms = ElementList()
        for p in self.ports:
            if isinstance(p, Term):
                terms += p
        return terms

    @property
    def term_ports(self):
        from spira.yevon.geometry.ports.term import Term
        terms = {}
        for p in self.ports:
            if isinstance(p, Term):
                terms[p.name] = p
        return terms


 

