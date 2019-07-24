import spidev
import time
from pyticc.utils import byte_bit_value, bit_into_byte

class SPIBase(object):

    def __init__(self, *args, **kwargs):
        """
        Instantiation

        args:
            none
            
        keyword-args:
            - spi_device:
            - spi_bus:
            - spi_speed
        """

        self.spi_device = 0
        self.spi_bus = 0
        self.spi_speed = 50000
        self.spi = None

        allowed = ['spi_device', 'spi_bus', 'spi_speed']
        for k, v in kwargs.items():
            if k in allowed:
                setattr(self, k, v)

        self.spi = spidev.SpiDev()
        self.spi.open(self.spi_bus, self.spi_device)
        self.spi.max_speed_hz = self.spi_speed


class CCBase(SPIBase):
    """
    Base class for all CCxxxx chips.

    This class assumes that any sublass will populate it's own
    register attributes. i.e. "self.SPWD", "self.READ_SINGLE_BYTE"

    """

    def __init__(self, *args, **kwargs):
        super(CCBase, self).__init__(args, kwargs)

    def read_byte(self, name):
        """Read byte at named address."""

        addr = self._get_address(name)
        return self.spi.xfer([self.READ_SINGLE_BYTE | addr, 0x00])[1]

    def write_byte(self, name, byte):
        """write byte to named address."""

        addr = self._get_address(name)
        return self.spi.xfer([self.WRITE_SINGLE_BYTE | addr, byte])

    def read_burst(self, name, length):
        """Burst read from named address"""

        buff = []
        addr = self._get_address(name)
        for x in range(length + 1):
            this_addr = (addr + (x * 8)) | self.READ_BURST
            buff.append(this_addr)

        return self.spi.xfer(buff)[1:]

    def write_burst(self, address, data):
        """Burst write to named address."""

        addr = self._get_address(name)
        data.insert(0, (self.WRITE_BURST | addr))
        return self.spi.xfer(data)

    # strobe and status commands
    # ---------------------------------
    def strobe(self, addr):
        """Strobe value to and address."""

        addr = self._get_address(addr)
        return self.spi.xfer([addr, 0x00])

    def marcstate(self):
        return (self.read_byte(self.MARCSTATE) & 0x1F)

    def flush_rx_fifo(self):
        """Flush RX fifo buffer."""

        self.strobe(self.SFRX)

    def flush_tx_fifo(self):
        """Flush TX fifo buffer."""

        self.strobe(self.SFTX)

    def power_down(self):
        """Power down CC1101."""

        self.sidle()
        self.strobe(self.SPWD)

    def reset(self):
        """Reset CC1101."""

        return self.strobe(self.SRES)

    def sidle(self):
        """Clear command strobes and wait for idle."""

        self.strobe(self.SIDLE)
        while (self.read_byte(self.MARCSTATE) != 0x01):
            self.cmd_delay(10)

        self.strobe(self.SFTX)
        self.cmd_delay(10)

    def enable_tx(self):
        """Switch CC1101 to TX mode."""

        self.strobe(self.STX)
        self.cmd_delay(2)

    def enable_rx(self):
        """Switch CC1101 to RX mode."""

        self.strobe(self.SRX)
        self.cmd_delay(2)

    def wor_on(self):
        """Start Wake On Radio (WOR) polling."""

        self.strobe(self.SWOR)
        self.cmd_delay(2)

    def sx_off(self):
        """Turn off crystal oscillator."""

        self.strobe(self.SXOFF)
        self.cmd_delay(2)

    def calibrate(self):
        """Calibrate frequency synthesizer and turn it off."""

        self.strobe(self.SCAL)
        self.cmd_delay(2)

    def cmd_delay(self, useconds):
        """Sleep for x microseconds."""

        time.sleep(useconds / 1000000.0)

    # Private methods*
    # ---------------------------------
    def _get_address(self, name):
        """Get an address value from named attribute."""

        if type(name) is int:
            return name
        elif type(name) is str:
            return getattr(self, name)
        else:
            raise ValueError("Unexpected address type '%s'" % type(name))

    def _extract_val_from_byte(self, byte, schema):
        return byte_bit_value(byte, schema)

    def _update_val_in_byte(self, byte, schema, value):
        return bit_into_byte(byte, schema, value)
