import os
import spira.all as spira
from spira.yevon import io
from copy import copy, deepcopy


from spira.technologies.aist.rdd.database import RDD


if __name__ == '__main__':

    # file_name = '/home/therealtyler/code/phd/spira/spira/technologies/aist/layouts/stable/dff.gds'
    # file_name = '/home/therealtyler/code/phd/spira/spira/technologies/aist/layouts/stable/and.gds'

    file_name = '/home/therealtyler/code/phd/spira/spira/technologies/aist/layouts/stable/jj.gds'
    # file_name = '/home/therealtyler/code/phd/spira/spira/technologies/aist/layouts/stable/jj_rotated.gds'
    # file_name = '/home/therealtyler/code/phd/spira/spira/technologies/aist/layouts/stable/jj_reflected.gds'

    # file_name = '/home/therealtyler/code/phd/spira/spira/technologies/aist/layouts/stable/jj_hierarchy.gds'
    # file_name = '/home/therealtyler/code/phd/spira/spira/technologies/aist/layouts/stable/jj_hierarchy_lvl3.gds'
    # file_name = '/home/therealtyler/code/phd/spira/spira/technologies/aist/layouts/stable/jj_hierarchy_lvl3_rotation.gds'
    # file_name = '/home/therealtyler/code/phd/spira/spira/technologies/aist/layouts/stable/jj_hierarchy_lvl3_reflection.gds'

    # file_name = '/home/therealtyler/code/phd/spira/spira/technologies/aist/layouts/stable/jj_hierarchy_lvl4.gds'
    # file_name = '/home/therealtyler/code/phd/spira/spira/technologies/aist/layouts/stable/jj_hierarchy_lvl4_rotation.gds'
    # file_name = '/home/therealtyler/code/phd/spira/spira/technologies/aist/layouts/stable/jj_hierarchy_lvl4_reflection.gds'

    D = io.import_gds(filename=file_name)
    D.output()

