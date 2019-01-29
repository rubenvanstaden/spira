import spira 
from spira import param
from spira.lpe.mask import Metal, Native


RDD = spira.get_rule_deck()


class Device(spira.Cell):
    """ A Cell encapsulates a set of elementals that
    describes the layout being generated. """

    metals = param.ElementalListField()
    contacts = param.ElementalListField()

    def __repr__(self):
        if hasattr(self, 'elementals'):
            elems = self.elementals
            return ("[SPiRA: Device(\'{}\')] " +
                    "({} elementals: {} sref, {} cells, {} polygons, " +
                    "{} labels, {} ports)").format(
                        self.name,
                        elems.__len__(),
                        elems.sref.__len__(),
                        elems.cells.__len__(),
                        elems.polygons.__len__(),
                        elems.labels.__len__(),
                        self.ports.__len__()
                    )
        else:
            return "[SPiRA: Device(\'{}\')]".format(self.__class__.__name__)

    # FIXME: Has to be placed here for deepcopy().
    def __str__(self):
        return self.__repr__()

    def _copy(self):
        cell = Device(
            name=self.name,
            elementals=deepcopy(self.elementals),
            ports=deepcopy(self.ports),
            nets=self.nets
        )
        return cell

    def create_metals(self, elems):
        return elems

    def create_contacts(self, elems):
        return elems

    def create_elementals(self, elems):
        if len(elems) == 0:
            metals = Metal(elementals=self.metals, level=1)
            natives = Native(elementals=self.contacts, level=1)

            elems += spira.SRef(metals)
            elems += spira.SRef(natives)

            for key in RDD.VIAS.keys:
                RDD.VIAS[key].PCELL.create_elementals(elems)
        else:
            for key in RDD.VIAS.keys:
                elems += spira.SRef(RDD.VIAS[key].PCELL, midpoint=(0,0))
        return elems
