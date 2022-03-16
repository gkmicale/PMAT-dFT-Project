'''

'''

# LUNA import block:
import matplotlib as plt
from pyluna import Luna

# XDAC import block:
from time import sleep
from xdac import XDAC

def main():
    #initialize luna and xdac objects
    luna = Luna()
    xdac = XDAC()

    # GPIB = 'GPIB0::8::INSTR'
    # luna.startup_luna()

    def sweep_and_plot(start_wavelength, stop_wavelength, num_points):
        step = (stop_wavelength - start_wavelength) / num_points

        wavelengths = []
        data = []

        for i in range(num_points):
            wavelength = start_wavelength + i * step
            luna.set_source_wavelength(wavelength=wavelength)
            luna.turnon_light_source()

            current = float(xdac.read_single_channel_current(1))
            voltage = float(xdac.read_single_channel_voltage(1))

            wavelengths.append(wavelength)
            data.append( current * voltage )

        plt.figure()
        plt.plot(wavelengths, data)
        plt.xlabel("wavelength [nm]")
        plt.ylabel("power [mW?]")
        plt.show()


    luna.find_DUT()

    xdac.unlock()  # change key to 'USMIT120c001'?

    xdac.set_channel_voltage_range(channel=1, _range=0)
    xdac.set_channel_current(channel=1, current_val=10)
    xdac.set_channel_voltage(channel=1, voltage_val=2.0)
    sleep(3)

    print('Channel 1 Voltage = ', xdac.read_single_channel_voltage(1))

    sleep(2)

    sweep_and_plot(1530., 1570., 100)

    xdac.set_off(1)

    xdac.lock()
    # xdac.shutdown()
    luna.close()


if __name__ == '__main__':
    main()
