from typing import Iterable

import zmq
import csv
from time import sleep


class XDAC:
    # class variables

    def __init__(self, xdac_ip='169.254.57.13'):
        # Connect to Req Server on XDAC via ZMQ
        # self.number_of_channels = None
        context = zmq.Context()
        self.req_socket = context.socket(zmq.REQ)
        self.req_socket.connect("tcp://%s:5555" % xdac_ip)

        self.sub_socket = context.socket(zmq.SUB)
        self.sub_socket.connect("tcp://%s:5556" % xdac_ip)

        self.subV_socket = context.socket(zmq.SUB)
        self.subV_socket.connect("tcp://%s:5556" % xdac_ip)

        self.subC_socket = context.socket(zmq.SUB)
        self.subC_socket.connect("tcp://%s:5556" % xdac_ip)

        # edit channel maximum of XDAC
        self.number_of_channels = 120

        # default range array for all channel
        self.channel_voltage_range_key = [3] * self.number_of_channels

        # Voltage Range Dictionary
        self.VOLTAGE_RANGE_DICT = {
            0: (0, 5),
            1: (0, 10),
            2: (0, 20),
            3: (0, 40)
        }

    def unlock(self, key='USMIT120c001'):
        # Send Request to XDAC (Server)
        msg = "GETINFO:" + key
        self.req_socket.send(msg.encode('utf-8'))
        message = self.req_socket.recv()

        return message.decode('utf-8')

    def lock(self):
        # Send Request to XDAC (Server)
        msg = "LOCK"
        self.req_socket.send(msg.encode('utf-8'))
        message = self.req_socket.recv()

        return message.decode('utf-8')

    def shutdown(self):
        # Send Request to XDAC (Server)
        msg = "EXIT"
        self.req_socket.send(msg.encode('utf-8'))
        message = self.req_socket.recv()

        return message.decode('utf-8')

    def set_channel_voltage(self, channel: int, voltage_val: float):
        """
        Set voltage of each channel
        If voltage_val > MaxVoltage,, voltage is set to MaxVoltage.
        Args:
            channel (int): channel number, starting at 1
            voltage_val (float): voltage value in V

        Returns:
            0 if successful
            1 if channel is outside accepted range
            TODO: change to return nothing and raise exception
        """

        if channel > self.number_of_channels:
            print("Channel exceeds the limit")
            return 1

        # Set threshold fo Current and Voltage
        MinVoltage, MaxVoltage = self.VOLTAGE_RANGE_DICT[self.channel_voltage_range_key[channel - 1]]

        if voltage_val > MaxVoltage:
            voltage_val = MaxVoltage
        elif voltage_val < MinVoltage:
            voltage_val = MinVoltage

        # Send Request to XDAC (Server)
        msgV = "SETV:" + ("%d" % channel) + ":" + ("%.3f" % voltage_val)
        self.req_socket.send(msgV.encode('utf-8'))
        message = self.req_socket.recv()

        return 0

    def set_channel_current(self, channel: int, current_val: float):
        """
        Set current of each channel.
        If user input current exceeds maximum current, current is set to the maximum.

        Args:
            channel (int): channel number, starting at 1
            current_val (float): current value between 0.0 and 300.0 in mA

        Returns:
            0 if successful
            1 if channel is outside accepted range
            TODO: change to return nothing and raise exception
        """

        if channel > self.number_of_channels:
            print("Channel exceeds the limit")
            return 1

        # Set threshold fo Current and Voltage
        MaxCurrent = 300.

        if current_val > MaxCurrent:
            current_val = MaxCurrent
        elif current_val < 0.0:
            current_val = 0.0

        # Send Request to XDAC (Server)
        msgC = "SETC:" + ("%d" % channel) + ":" + ("%.3f" % current_val)
        self.req_socket.send(msgC.encode('utf-8'))
        message = self.req_socket.recv()

        return 0

    def set_channel_current_byte(self, channel: int, current_byte: int):
        """
        Set current of each channel with byte input.

        Args:
            channel (int): channel number, starting at 1
            current_byte (int): byte value of current between 0 and 65535, corresponding to 0-300 mA

        Returns:
            0 if successful
            1 if channel is outside accepted range
            TODO: change to return None and raise exception
        """

        if channel > self.number_of_channels:
            print("Channel exceeds the limit")
            return 1

        # Send Request to XDAC (Server)
        msgC = "BITC:" + ("%d" % channel) + ":" + ("%d" % current_byte)
        self.req_socket.send(msgC.encode('utf-8'))
        message = self.req_socket.recv()

        return 0

    def set_channel_voltage_range(self, channel: int, _range):
        """
        Set the voltage range of a single channel.
        range 0 corresponds to voltage = [0,5]  V
        range 1 corresponds to voltage = [0,10] V
        range 2 corresponds to voltage = [0,20] V
        range 3 corresponds to voltage = [0,40] V

        Args:
            channel (int): channel number, starting at 1
            _range (int): integer between 0-3 indicating the desired voltage range based on VOLTAGE_RANGE_DICT

        Returns:
            0 if successful
            1 if channel is outside accepted range
            TODO: change to return None and raise exception
        """

        if channel > self.number_of_channels:
            print("Channel exceeds the limit")
            return 1

        if _range not in range(0, 4):
            print("Wrong Channel Range, please look at Range Dictionary")
            return 1

        self.channel_voltage_range_key[channel - 1] = _range

        # Send Request to XDAC (Server)
        msg = "SETR:" + ("%d" % channel) + ":" + str(_range)
        self.req_socket.send(msg.encode('utf-8'))
        message = self.req_socket.recv()

        return 0

    def set_voltage_all_channels(self, all_v_values: Iterable):
        """
        Set voltage of all channels.

        Examples:
            >>> xdac = XDAC()
            ... voltages = [8, 8, -1, 2, 3, 4, 5, 7]
            ... xdac.set_voltage_all_channels(voltages)

        Args:
            all_v_values (Iterable): list of voltages in V for each channel in order,
                                     expected size is the number of channels used

        Returns:
            0 if successful
        """
        # TODO: check if len(all_v_vals) < number_of_channels OR use set_channel_voltage
        # TODO add start value = 1 to enum
        msg = "SETMULTIA;:" + ":".join([f"V{i + 1}:{v:.3f}" for i, v in enumerate(all_v_values)]) + ";"
        self.req_socket.send(msg.encode('utf-8'))
        message = self.req_socket.recv()

        return 0

    def set_current_all_channels(self, all_c_values: Iterable):
        """
        Set current of all channels.

        Examples:
            >>> xdac = XDAC()
            ... currents = [200, 200, 300, 50, 300, 400, 450, 250]
            ... xdac.set_current_all_channels(currents)

        Args:
            all_c_values (Iterable): list of currents in mA for each channel in order,
                                     expected size is the number of channels used

        Returns:
            0 if successful
        """
        # TODO: check if len(all_c_vals) < number_of_channels OR use set_channel_current
        # TODO add start value = 1 to enum
        msg = "SETMULTIA;;:" + ":".join([f"C{i + 1}:{c:.3f}" for i, c in enumerate(all_c_values)])
        self.req_socket.send(msg.encode('utf-8'))
        message = self.req_socket.recv()

        return 0

    def set_range_all_channels(self, all_r_values: Iterable):
        """
        Set voltage range for all channels.

        Examples:
            >>> xdac = XDAC()
            ... v_ranges = [5, 5, 5, 5, 5, 5, 5, 5]
            ... xdac.set_range_all_channels(v_ranges)

        Args:
            all_r_values (Iterable): list of voltage ranges for each channel in order,
                                     expected size is the number of channels used

        Returns:
            None
        """
        # TODO: check if len(all_r_vals) < number_of_channels OR use set_channel_range
        for channel, value in enumerate(all_r_values):  # TODO add start value = 1
            channel = channel + 1  # Channel start from 1
            self.set_channel_voltage_range(channel, value)

        return

    def set_off_all_channel(self):
        """
        Zeros all channels to 0 V, 0 mA

        Returns:
            0 if successful
        """

        # Send Request to XDAC (Server)
        msg = "ZERO:ALL"
        self.req_socket.send(msg.encode('utf-8'))
        message = self.req_socket.recv()

        return 0

    def set_off(self, channel: int):
        """
        Sets one channel to zero.

        Examples:
            >>> xdac = XDAC()
            ... xdac.set_off(channel= 1) # sets channel 1 to 0 V, 0 mA

        Args:
            channel (int): channel number, starting at 1

        Returns:
            0 if successful
        """

        # Channel Validation
        if channel > self.number_of_channels:
            print("Channel exceeds the limit")
            return 1

        # Send Request to XDAC (Server)
        msg = "ZERO:" + ("%d" % channel)
        self.req_socket.send(msg.encode('utf-8'))
        message = self.req_socket.recv()

        return 0

    def read_single_channel_current(self, channel: int):
        """
        Read current in mA from a single channel.

        Args:
            channel (int): channel number, starting at 1

        Returns:
            TODO: what is the returned message?
        """

        # Send Request to XDAC (Server)
        msg = "MEASC:" + ("%d" % channel)
        self.req_socket.send(msg.encode('utf-8'))
        message = self.req_socket.recv()

        return (message.decode('utf-8'))

    def read_single_channel_voltage(self, channel: int):
        """
        Read voltage in V from a single channel.

        Args:
            channel (int): channel number, starting at 1

        Returns:
            TODO: what is the returned message?
        """

        # Send Request to XDAC (Server)
        msg = "MEASV:" + ("%d" % channel)
        self.req_socket.send(msg.encode('utf-8'))
        message = self.req_socket.recv()

        return (message.decode('utf-8'))

    def read_all_channels_current(self):
        """
        Reads currents in mA from all channels.

        Returns:
            TODO: what is the return?
        """

        self.subC_socket.setsockopt(zmq.SUBSCRIBE, b'C')

        string = self.subC_socket.recv()
        # print(string)
        msg = string.decode('utf-8')
        value = msg[1:-1].split(",")

        return value[0:-1:2]

    def read_all_channels_voltage(self):
        """
        Reads voltages in V of all channels.

        Returns:
            TODO: what is the return?
        """

        self.subV_socket.setsockopt(zmq.SUBSCRIBE, b'V')

        string = self.subV_socket.recv()
        # print(string)
        msg = string.decode('utf-8')
        value = msg[1:-1].split(",")

        return value[0:-1:2]

    def measurement_config(self, averaging_sample: int, voltage_conversion_time: int, current_conversion_time: int):
        """
        Sets measurement configuration with the averaging sample and current and voltage conversion times.

        Args:
            averaging_sample (int):
            voltage_conversion_time (int): voltage conversion time in μs
            current_conversion_time (int): current conversion time in μs

        Returns:
            0 if successful
            TODO: change to return None
        """

        # Send Request to XDAC (Server)
        msg = ("CONFIG:" +
               str(averaging_sample) + ":" +
               str(voltage_conversion_time) + ":" +
               str(current_conversion_time))

        self.req_socket.send(msg.encode('utf-8'))
        message = self.req_socket.recv()

        return 0

    def sweep_one(self, channel: int, voltage_sequence: Iterable[float],
                  current_sequence: Iterable[float], duration: int, output_file: str):
        """
        Set one channel to run automatically and record it.

        Examples:
            >>> xdac = XDAC()
            ... voltages = [1, 2, 3, 4, 5, 6, 7, 8]
            ... currents = = [10, 10, 10, 10, 10, 10, 10, 10]
            ... xdac.sweep_one(1, voltages, currents, 5, 'channel_1.csv')

        Args:
            channel (int):
            voltage_sequence (Iterable[float]): list of voltages in V for each state
            current_sequence (Iterable[float]): list of currents in mA for each state
            duration (int): time to hold each state in seconds
            output_file (str): csv file name to record measured voltages and currents for each state.

        Returns:
            None
        """

        read_voltages = []
        read_currents = []

        for voltage, current in zip(voltage_sequence, current_sequence):
            self.set_channel_voltage(channel, voltage)
            self.set_channel_current(channel, current)
            sleep(duration)
            read_voltages.append(self.read_single_channel_voltage(channel))
            read_currents.append(self.read_single_channel_current(channel))

        with open(output_file, mode='w') as csv_file:
            fieldnames = ['setV(v)', 'voltage(v)', 'current(mA)']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            for value in range(len(read_voltages)):
                writer.writerow({'setV(v)': voltage_sequence[value], 'voltage(v)': float(read_voltages[value]),
                                 'current(mA)': read_currents[value]})

        print("sweep done")

        return
