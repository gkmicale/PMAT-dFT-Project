'''

'''

# LUNA import block:
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# from pyluna import Luna

# XDAC import block:
# import zmq
# from time import sleep
# import csv
# import numpy as np
from time import sleep
from xdac import XDAC

XDAC_IP = "192.168.18.159"


def main():
    # luna = Luna()
    # luna.configure_scan_parameters(center_wl=1550.0, scan_range=80.0)

    xdac = XDAC()
    xdac.unlock()  # change key to 'USMIT120c001'?

    xdac.set_channel_voltage_range(channel=1, _range=0)
    xdac.set_channel_current(channel=1, current_val=10)
    xdac.set_channel_voltage(channel=1, voltage_val=2.0)
    sleep(3)

    print(xdac.read_single_channel_voltage(1))

    # xdac.set_channel_current(channel=1, current_val=10)
    xdac.set_channel_voltage(channel=1, voltage_val=4.0)
    sleep(3)

    print(xdac.read_single_channel_voltage(1))

    xdac.set_off(1)

    xdac.lock()
    xdac.shutdown()


if __name__ == '__main__':
    main()
