import spira
from spira import LOG
from spira import param
from spira import settings


class PCell(spira.Cell):

    layer = param.LayerField(number=4)
    width = param.FloatField(default=1)
    point = param.PointArrayField(default=1)
    coord = param.PointField()
    iscell = param.BoolField()
    number = param.IntegerField()


# -------------------------------------------------------------------------


if __name__ == '__main__':

    LOG.section('PCell instance')
    pcell = PCell()
    print(pcell)

    LOG.section("When a cell is created it is automatically " +
                "added to SPiRA default library class. " +
                "The currently set library can be " +
                "retrieved and analyzed.")
    lib_default = settings.get_library()
    print(lib_default)

    LOG.section('Create and add to new library')
    lib_new = spira.Library(name='New Lib')
    lib_new += pcell
    print(lib_new)





