import spira
from spira import LOG
from spira import param


RDD = spira.get_rule_deck()


class PCell(spira.Cell):

    layer = param.LayerField(number=RDD.BAS.LAYER.number, doc='Layer for the first polygon.')
    width = param.FloatField(default=RDD.BAS.WIDTH, doc='Box shape width.')


# -------------------------------------------------------------------------


if __name__  == '__main__':

    LOG.section('PCell paramters')
    pcell = PCell()
    print(pcell.layer)
    print('width: {}'.format(pcell.width))

    LOG.section('Update parameters')
    pcell = PCell(width=3.4)
    print('width: {}'.format(pcell.width))

    LOG.section('Switch to different RDD')
    print(RDD)
    from demo.pdks.process.aist_pdk import database
    print(RDD)

    print('\n--- Documentation ---')
    print(PCell.layer.__doc__)
    print(PCell.width.__doc__)


