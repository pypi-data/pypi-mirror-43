"""
Implements some of the functionality of the DATAQ DI-2008 data acquisition module.
"""

import logging
import threading
from time import sleep

from serial import Serial
from serial.tools import list_ports


class Port:
    _mode_bit = 12
    _range_bit = 11
    _scale_bit = 8

    def __init__(self, callback: callable=None, loglevel=logging.DEBUG):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(loglevel)

        self._callback = callback

        self.value = None
        self.configuration = 0
        self.commands = []

    def parse(self, value):
        raise NotImplementedError


class AnalogPort(Port):
    def __init__(self, channel: int, analog_range: float=None, thermocouple_type: str=None,
                 filter: str='last point', filter_decimation: int=10, loglevel=logging.INFO):
        """
        Analog input

        :param channel: integer, the channel number
        :param analog_range: float, the expected range when configurated as an analog input
        :param thermocouple_type: string, a single letter denoting the thermocouple type
        :param filter: string, a string containing 'last point', 'average', 'maximum' or 'minimum'
        :param filter_decimation: int, an integer containing the number of samples over which to filter
        :param loglevel: the logging level
        """
        super().__init__(loglevel=loglevel)

        if channel not in range(0, 8):
            self._logger.warning(f'analog channel "{channel}" not valid')
            return

        configuration = channel

        if analog_range is not None and thermocouple_type is not None:
            raise ValueError(f'analog range and thermocouple type are both specified for analog channel {channel}')

        if analog_range is not None:
            valid_ranges = [0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, 25.0, 50.0]
            if analog_range not in valid_ranges:
                raise ValueError(f'valid values for analog range: {", ".join(valid_ranges)}')

            if analog_range >= 1.0:
                configuration |= (1 << self._range_bit)  # set the range bit
                analog_range /= 100         # change the range to make lookup easier

            range_lookup = {
                0.5: 0, 0.25: 1, 0.1: 2, 0.05: 3, 0.025: 4, 0.01: 5
            }
            configuration |= (range_lookup[analog_range] << self._scale_bit)

        if thermocouple_type is not None:
            if thermocouple_type.lower() not in 'bejknrst':
                self._logger.warning(f'thermocouple type must be valid')
                return
            configuration |= 1 << self._mode_bit  # set the mode bit
            thermo_lookup = {
                'b': 0, 'e': 1, 'j': 2, 'k': 3, 'n': 4, 'r': 5, 's': 6, 't': 7
            }

            configuration |= (thermo_lookup[thermocouple_type.lower()] << self._scale_bit)

        filter_types = ['last point', 'average', 'maximum', 'minimum']
        if filter.lower() not in filter_types:
            raise ValueError(f'the "filter" must be one of the following: {", ".join(filter_types)}')
        if filter_decimation < 1 or filter_decimation > 32767:
            raise ValueError('the "filter_decimation" parameter must be between 1 and 32767, inclusive')

        filter_value = filter_types.index(filter.lower())

        self.configuration = configuration
        self.commands += [f'filter {channel} {filter_value}', f'dec {filter_decimation}']

    @property
    def _is_tc(self):
        """
        Return 'True' if is a thermocouple, else 'False'
        """
        return (self.configuration & (1 << self._mode_bit)) > 0

    def __str__(self):
        channel = self.configuration & 0xf

        string = f'analog input, channel {channel} '
        if self._is_tc:
            # string construction for thermocouple type
            string += 'thermocouple '

            tc_ranges = {
                0: 'B', 1: 'E', 2: 'J', 3: 'K', 4: 'N', 5: 'R', 6: 'S', 7: 'T'
            }
            tc_type = tc_ranges[(self.configuration & (0x7 << self._scale_bit)) >> self._scale_bit]

            string += f'type {tc_type}'

        else:
            string += 'range '

            ranges = [0.5, 0.25, 0.1, 0.05, 0.025, 0.01]
            range_bit = self.configuration & (1 << self._range_bit)
            if range_bit:
                ranges = [r * 100 for r in ranges]
            scale_factor = (self.configuration & (0x7 << self._scale_bit)) >> self._scale_bit
            range_value = ranges[scale_factor]
            string += f'+/-{range_value}V'

        return string

    def parse(self, input):
        if self._is_tc:
            if input == 32767:
                self.value = None
                self._logger.warning(f'!!! TC Error, cannot communicate with sensor or the reading '
                                     f'is outside the sensor\'s measurement range on "{str(self)}"')
                return
            elif input == -32768:
                self.value = None
                self._logger.warning(f'!!! TC Error, thermocouple open or not connected on "{str(self)}"')
                return

            # from datasheet...
            m_lookup = {
                'j': 0.021515, 'k': 0.023987, 't': 0.009155, 'b': 0.023956,
                'r': 0.02774, 's': 0.02774, 'e': 0.018311, 'n': 0.022888
            }
            b_lookup = {
                'j': 495, 'k': 586, 't': 100, 'b': 1035,
                'r': 859, 's': 859, 'e': 400, 'n': 550
            }

            tc_ranges = {
                0: 'b', 1: 'e', 2: 'j', 3: 'k', 4: 'n', 5: 'r', 6: 's', 7: 't'
            }
            tc_type = tc_ranges[(self.configuration & (0x7 << self._scale_bit)) >> self._scale_bit]

            m = m_lookup[tc_type]
            b = b_lookup[tc_type]

            self.value = input * m + b
            self._logger.debug(f'input value "{input}" converted for "{str(self)}" is "{self.value:.2f}°C"')

            if self._callback:
                self._callback(self.value)

            return self.value

        ranges = [0.5, 0.25, 0.1, 0.05, 0.025, 0.01]
        range_bit = self.configuration & (1 << self._range_bit)
        if range_bit:
            ranges = [r * 100 for r in ranges]
        scale_factor = (self.configuration & (0x7 << self._scale_bit)) >> self._scale_bit
        range_value = ranges[scale_factor]

        self.value = range_value * float(input) / 32768.0
        self._logger.debug(f'input value "{input}" converted for "{str(self)}" is "{self.value:.4f}V"')

        if self._callback:
            self._callback(self.value)

        return self.value


class RatePort(Port):
    def __init__(self, range_hz=50000, filter_samples: int=32, loglevel=logging.INFO):
        super().__init__(loglevel=loglevel)

        rates_lookup = {
            50000: 1, 20000: 2, 10000: 3, 5000: 4, 2000: 5, 1000: 6, 500: 7, 200: 8, 100: 9, 50: 10, 20: 11, 10: 12
        }
        valid_rates = [r for r in rates_lookup.keys()]
        if range_hz not in valid_rates:
            raise ValueError(f'rate not valid, please choose a valid rate from the following: {", ".join(valid_rates)}')

        if not 1 <= filter_samples <= 64:
            raise ValueError(f'filter_samples not valid, must be between 1 and 64, inclusive')

        self.configuration = (rates_lookup[range_hz] << self._scale_bit) + 0x9
        self.commands += [f'ffl {filter_samples}']
        self._range = range_hz

    def __str__(self):
        return f'rate input, {self._range}Hz'

    def parse(self, input):
        self.value = self._range * (input + 32768) / 65536
        self._logger.debug(f'input value "{input}" converted for "{str(self)}" is "{self.value:.4f}Hz"')

        if self._callback:
            self._callback(self.value)

        return self.value


class CountPort(Port):
    def __init__(self, loglevel=logging.DEBUG):
        super().__init__(loglevel=loglevel)

        self.configuration = 0xa
        raise NotImplementedError


class DigitalPort(Port):
    def __init__(self, output: bool=True, loglevel=logging.DEBUG):
        super().__init__(loglevel=loglevel)

        self.configuration = 0x8
        raise NotImplementedError


class Di2008:
    def __init__(self, port_name=None, timeout=0.05, loglevel=logging.INFO):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.setLevel(loglevel)

        self._timeout = timeout
        self._scanning = False
        self._scan_index = 0
        self._serial_port = None
        self._ports = []
        self._raw = []

        self._manufacturer = None
        self._pid = None
        self._firmware = None
        self._esn = None

        # initialize the command queue with basic information requests
        self._command_queue = [
            'stop', 'info 0', 'info 1', 'info 2', 'info 6', 'srate 10'
        ]

        success = self._discover(port_name)

        if success:
            self._thread = threading.Thread(target=self._run)
            self._thread.start()

    def __str__(self):
        return f'{self._manufacturer} DI-{self._pid}, serial number {self._esn}, firmware {self._firmware}'

    def change_led_color(self, color: 'str'):
        colors_lookup = {
            'black': 0, 'blue': 1, 'green': 2, 'cyan': 3,
            'red': 4, 'magenta': 5, 'yellow': 6, 'white': 7
        }
        valid_colors = [c for c in colors_lookup.keys()]

        if color.lower() not in valid_colors:
            raise ValueError(f'color not valid, should be one of {", ".join(valid_colors)}')

        self._command_queue.append(f'led {colors_lookup[color.lower()]}')

    def create_scan_list(self, scan_list: list):
        # create a scan list based on the provided list
        for port in scan_list:
            if not isinstance(port, Port):
                raise ValueError(f'"{port}" is not an instance of Port class')

        if len(scan_list) > 11:
            raise ValueError('scan list may only be a maximum of 11 elements long')

        # todo: check for duplicates and raise ValueError if duplicate detected

        self._ports = scan_list

        # change the packet size based on the scan list length
        if len(scan_list) < 8:
            packet_size_id = 0
        elif len(scan_list) < 16:
            packet_size_id = 1
        elif len(scan_list) < 32:
            packet_size_id = 2
        else:
            packet_size_id = 3
        self._command_queue.append(f'ps {packet_size_id}')

        # create the scan list
        commands = [f'slist {offset} {port.configuration}' for offset, port in enumerate(self._ports)]

        # add any other port-specific commands
        for port in self._ports:
            for command in port.commands:
                commands.append(command)

        commands.append('info 9')

        # shift the entire command list into the transmit queue
        [self._command_queue.append(c) for c in commands]

        return True

    def start(self):
        self._command_queue.append('start')

    def stop(self):
        self._command_queue.append('stop')

    def close(self):
        self._logger.warning('closing port')
        if self._serial_port:
            self._serial_port.close()
            self._serial_port = None

    def _discover(self, port_name=None):
        if not port_name:
            available_ports = list(list_ports.comports())
            for p in available_ports:
                # Do we have a DATAQ Instruments device?
                if "VID:PID=0683" in p.hwid:
                    # Yes!  Detect and assign the hooked com port
                    port_name = p.device
                    break

        if port_name:
            self._logger.info(f'Found a DATAQ Instruments device on {port_name}')
            self._serial_port = Serial()
            self._serial_port.timeout = 0
            self._serial_port.port = port_name
            self._serial_port.baudrate = '115200'
            self._serial_port.open()

            return True

        raise ValueError('DI-2008 not found on bus')

    def _send_cmd(self, command: str):
        self._logger.debug(f'sending "{command}"')
        self._serial_port.write(f'{command}\r'.encode())

    def _parse_received(self, received):
        self._logger.debug(f'received from unit: "{received}"')

        if self._scanning:
            for i in range(len(received) >> 1):
                int_value = received[i*2] + received[i*2+1] * 256
                if int_value > 32767:
                    int_value = int_value - 65536

                self._ports[self._scan_index].parse(int_value)
                self._scan_index += 1
                self._scan_index %= len(self._ports)

        else:
            # strip the '0x00' from the received data in non-scan mode - it only causes problems
            self._raw += [chr(b) for b in received if b != 0]

            messages = []
            while '\r' in self._raw:
                self._logger.debug('"\\r" detected, decoding message...')

                end_index = self._raw.index('\r')
                message = ''.join(self._raw[:end_index])

                messages.append(message)
                self._logger.debug(f'message received: "{message}"')

                self._raw = self._raw[end_index:]
                if self._raw[0] == '\r':
                    self._raw.pop(0)

            for message in messages:
                if 'info' in message:
                    self._parse_info(message)
                else:
                    self._logger.info(f'message could not be parsed: "{message}"')

    def _parse_info(self, message):
        if 'info' not in message:
            return

        # make numbers to data
        if 'info 0' in message:
            self._manufacturer = message.split('info 0')[-1].strip()
            if self._manufacturer != 'DATAQ':
                self.close()

        elif 'info 1' in message:
            self._pid = message.split('info 1')[-1].strip()
            if self._pid != '2008':
                self.close()

        elif 'info 2' in message:
            self._firmware = message.split('info 2')[-1].strip()

        elif 'info 6' in message:
            self._esn = message.split('info 6')[-1].strip()

        else:
            self._logger.warning(f'message not understood: "{message}"')

    def _maintain_send_queue(self):
        if len(self._command_queue) > 0:
            command = self._command_queue.pop(0)

            if 'start' in command:
                self._scanning = True
                self._scan_index = 0
            elif 'stop' in command:
                self._scanning = False

            self._send_cmd(command)

    def _run(self):
        while self._serial_port:
            waiting = self._serial_port.in_waiting
            if waiting > 0:
                raw = self._serial_port.read(waiting)
                self._parse_received(raw)

            self._maintain_send_queue()

            sleep(self._timeout)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    daq = Di2008(loglevel=logging.DEBUG)
    sleep(0.5)

    daq.create_scan_list(
        [
            AnalogPort(0, analog_range=10.0, filter='average'),
            AnalogPort(1, thermocouple_type='j'),
            AnalogPort(2, thermocouple_type='j'),
            RatePort(5000)
        ]
    )
    daq.start()

    sleep(2.5)
    daq.stop()
    sleep(0.5)
    daq.close()
