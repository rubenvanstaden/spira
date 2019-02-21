import spira
import time
from spira.gdsii.io import current_path
from spira.lpe.circuits import Circuit
from demo.pdks.process.mitll_pdk.database import RDD


# from halo import Halo
 
# success_message = 'Loading success'
# failed_message = 'Loading failed'
# unicorn_message = 'Loading unicorn'

# spinner = Halo(text=success_message, spinner='dots')

# try:
#     spinner.start()
#     time.sleep(1)
#     spinner.succeed()
#     spinner.start(failed_message)
#     time.sleep(1)
#     spinner.fail()
#     spinner.start(unicorn_message)
#     time.sleep(1)
#     spinner.stop_and_persist(symbol='🦄'.encode('utf-8'), text=unicorn_message)
# except (KeyboardInterrupt, SystemExit):
#     spinner.stop()


if __name__ == '__main__':

    start = time.time()

    # name = 'LSmitll_DCSFQ_new'
    # name = 'LSmitll_jtlt_new'
    # name = 'LSmitll_NOT_new'
    # name = 'LSmitll_SFQDC1_new'
    # name = 'LSmitll_SPLITT_new'
    name = 'LSmitll_DFFT_new'
    # name = 'LSmitll_MERGET_new'

    filename = current_path(name)
    cell = spira.import_gds(filename=filename)
    # cell.output()

    layout = Circuit(cell=cell, level=2)
    layout.netlist
    layout.mask.output()

    # try:
    #     spinner.start()

    #     # name = 'jj_mitll_2'
    #     # name = 'mitll_jtl_double'
    #     # name = 'mitll_dsndo_xic'
    #     # name = 'mitll_SFQDC_draft'
    #     # name = 'LSmitll_SFQDC'
    #     # name = 'splitt_v0.3'
    #     name = 'LSmitll_jtlt_new'

    #     filename = current_path(name)
    #     cell = spira.import_gds(filename=filename)
    #     # cell.output()

    #     layout = Circuit(cell=cell, level=2)
    #     layout.netlist
    #     # layout.mask.output()

    #     spinner.succeed()
    #     spinner.stop()
    # except (KeyboardInterrupt, SystemExit):
    #     spinner.stop()

    end = time.time()
    print(end - start)

