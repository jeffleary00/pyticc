import math
from pyticc.base import CCBase

class CCAddr(object):
    WRITE_SINGLE_BYTE = 0x00
    WRITE_BURST = 0x40
    READ_SINGLE_BYTE = 0x80
    READ_BURST = 0xC0

    # COMMAND STROBE REGISTERS
    # -------------------------------------------
    SRES = 0x30         # Reset chip
    SFSTXON = 0x31
    SXOFF = 0x32        # Turn off crystal oscillator.
    SCAL = 0x33         # Calibrate frequency synthesizer and turn it off.
    SRX = 0x34          # Enable RX.
    STX = 0x35          # In IDLE state: Enable TX. Perform calibration first
    SIDLE = 0x36        # Exit RX / TX, turn off frequency synthesizer and exit Wake-On-Radio mode if applicable.
    SWOR = 0x38         # Start automatic RX polling sequence (Wake-on-Radio)
    SPWD = 0x39         # Enter power down mode when CSn goes high.
    SFRX = 0x3A         # Flush the RX FIFO buffer.
    SFTX = 0x3B         # Flush the TX FIFO buffer.
    SWORRST = 0x3C      # Reset real time clock to Event1 value.
    SNOP = 0x3D         # No op. Used to get access to the chip status byte.
    PATABLE = 0x3E      # PATABLE
    TXFIFO = 0x3F       # TXFIFO
    RXFIFO = 0x3F       # RXFIFO

    # STATUS REGISTERS
    # -------------------------------------------
    PARTNUM = 0xF0      # Chip ID
    VERSION = 0xF1      # Chip ID
    FREQEST = 0xF2      # Frequency Offset Estimate from Demodulator
    LQI = 0xF3          # Demodulator Estimate for Link Quality
    RSSI = 0xF4         # Received Signal Strength Indication
    MARCSTATE = 0xF5    # Main Radio Control State Machine State
    WORTIME1 = 0xF6     # High Byte of WOR Time
    WORTIME0 = 0xF7     # Low Byte of WOR Time
    PKTSTATUS = 0xF8    # Current GDOx Status and Packet Status
    VCO_VC_DAC = 0xF9   # Current Setting from PLL Calibration Module
    TXBYTES = 0xFA      # Underflow and Number of Bytes
    RXBYTES = 0xFB      # Overflow and Number of Bytes
    RCCTRL1_STATUS = 0xFC  # Last RC Oscillator Calibration Result
    RCCTRL0_STATUS = 0xFD  # Last RC Oscillator Calibration Result

    # CONFIGURATION REGISTERS (These preserve in SLEEP)
    # -------------------------------------------
    IOCFG2 = 0x00       # GDO2 Output Pin Configuration
    IOCFG1 = 0x01       # GDO1 Output Pin Configuration
    IOCFG0 = 0x02       # GDO0 Output Pin Configuration
    FIFOTHR = 0x03      # RX FIFO and TX FIFO Thresholds
    SYNC1 = 0x04        # Sync Word, High Byte
    SYNC0 = 0x05        # Sync Word, Low Byte
    PKTLEN = 0x06       # Packet Length
    PKTCTRL1 = 0x07     # Packet Automation Control
    PKTCTRL0 = 0x08     # Packet Automation Control
    ADDR = 0x09         # Device Address
    CHANNR = 0x0A       # Channel Number
    FSCTRL1 = 0x0B      # Frequency Synthesizer Control
    FSCTRL0 = 0x0C      # Frequency Synthesizer Control
    FREQ2 = 0x0D        # Frequency Control Word, High Byte
    FREQ1 = 0x0E        # Frequency Control Word, Middle Byte
    FREQ0 = 0x0F        # Frequency Control Word, Low Byte
    MDMCFG4 = 0x10      # Modem Configuration
    MDMCFG3 = 0x11      # Modem Configuration
    MDMCFG2 = 0x12      # Modem Configuration
    MDMCFG1 = 0x13      # Modem Configuration
    MDMCFG0 = 0x14      # Modem Configuration
    DEVIATN = 0x15      # Modem Deviation Setting
    MCSM2 = 0x16        # Main Radio Control State Machine Configuration
    MCSM1 = 0x17        # Main Radio Control State Machine Configuration
    MCSM0 = 0x18        # Main Radio Control State Machine Configuration
    FOCCFG = 0x19       # Frequency Offset Compensation Configuration
    BSCFG = 0x1A        # Bit Synchronization Configuration
    AGCCTRL2 = 0x1B     # AGC Control
    AGCCTRL1 = 0x1C     # AGC Control
    AGCCTRL0 = 0x1D     # AGC Control
    WOREVT1 = 0x1E      # High Byte Event0 Timeout
    WOREVT0 = 0x1F      # Low Byte Event0 Timeout
    WORCTRL = 0x20      # Wake On Radio Control
    FREND1 = 0x21       # Front End RX Configuration
    FREND0 = 0x22       # Front End TX Configuration
    FSCAL3 = 0x23       # Frequency Synthesizer Calibration
    FSCAL2 = 0x24       # Frequency Synthesizer Calibration
    FSCAL1 = 0x25       # Frequency Synthesizer Calibration
    FSCAL0 = 0x26       # Frequency Synthesizer Calibration
    RCCTRL1 = 0x27      # RC Oscillator Configuration
    RCCTRL0 = 0x28      # RC Oscillator Configuration

    # CONFIGURATION REGISTERS (These are lost in SLEEP)
    # -------------------------------------------
    FSTEST = 0x29       # Frequency Synthesizer Calibration Control
    PTEST = 0x2A        # Production Test
    AGCTEST = 0x2B      # AGC Test
    TEST2 = 0x2C        # Various Test Settings
    TEST1 = 0x2D        # Various Test Settings
    TEST0 = 0x2E        # Various Test Settings


class CC1101(CCAddr, CCBase):
    """
    Class to interface with the TI CC1101 RF transceiver chip over SPI.

    See Texas Instruments data sheet for more details:
    http://www.ti.com/lit/ds/symlink/cc1101.pdf

    """

    def __init__(self, *args, **kwargs):
        """
        Instantiation

        args:
            none

        keyword-args:
            - osc_freq: (freq in hz for crystal osc. default=26Mhz)
        """

        self.osc_freq = 26000000

        super(CC1101, self).__init__(args, kwargs)

        allowed = ['osc_freq']
        for k, v in kwargs.items():
            if k in allowed:
                setattr(self, k, v)

    # basics
    # ---------------------------------
    def sanity_check(self):
        """
        Perform basic sanity check.
        Will throw errors if partnum and version are not correct.

        args: none
        returns: none
        """

        part_num = self.read_byte('PARTNUM')
        component_ver = self.read_byte('VERSION')
        assert part_num == 0x00
        assert component_ver == 0x14
        return {"PARTNUM": part_num, "VERSION": component_ver}

    # config/setup
    # ---------------------------------

    def base_frequency(self, freq=None):
        """
        Get or set CC1101 base carrier freq.

        args: [optional] Mhz = int(315|433|868|915)
        returns:
        """

        if freq is not None and freq not in [315, 433, 868, 915]:
            raise ValueError("Unsupported carrier freq '%d'" % freq)

        if freq is None:
            f2 = self.read_byte(self.FREQ2) << 16
            f1 = self.read_byte(self.FREQ1) << 8
            f0 = self.read_byte(self.FREQ0)
            freq = f2 + f1 + f0
            chan = self.register_value("CHANNR")['CHAN[7:0]']
            chanspc_m = self.register_value("MDMCFG0")['CHANSPC_M[7:0]']
            chanspc_e = self.register_value("MDMCFG1")['CHANSPC_E[1:0]']

            r = (self.osc_freq/math.pow(2, 16)) * (freq + chan * (( 256 + chanspc_m) * math.pow(2,(chanspc_e - 2))))
            return r

        self.sidle()
        carrier = int(0x10000 * (freq * 1000000)/ self.osc_freq)
        data = [hex(carrier >> i & 0xff) for i in (16,8,0)]
        self.write_byte(self.FREQ0, int(data[2], 16))
        self.write_byte(self.FREQ1, int(data[1], 16))
        self.write_byte(self.FREQ2, int(data[0], 16))
        return self.base_frequency()

    def modulation(self, modulation=None):
        """
        Get or set modulation.

        args: [optional] str (2-FSK|GFSK|ASK|OOK|4-FSK|MSK)
        returns: str
        """

        schemes = {
            "2-FSK":    "000",
            "GFSK":     "001",
            "ASK":      "011",
            "OOK":      "011",
            "4-FSK":    "100",
            "MSK":      "111"
        }

        if modulation is not None and modulation not in schemes.keys():
            raise ValueError("Unknown modulation type '%s'" % modulation)

        data = self.register_value("MDMCFG2")
        if not modulation:
            for k, v in schemes.items():
                if data['MOD_FORMAT[2:0]'] == int(v, 2):
                    return k

            return None
        else:
            self.register_write("MDMCFG2", 'MOD_FORMAT[2:0]', schemes[modulation])
            return self.modulation()

    def packet_length(self, mode=None):
        """
        Get or set packet length mode.

        args: [optional] str(PKT_LEN_FIXED|PKT_LEN_VARIABLE)
        returns: str

        note: PKT_LEN_INFINITE is not currently supported
        """

        modes = {
            "PKT_LEN_FIXED": "00",
            "PKT_LEN_VARIABLE": "01",
            "PKT_LEN_INFINITE": "10"
        }
        if mode is not None and mode not in modes.keys():
            raise ValueError("Unknown packet mode '%s'" % mode)

        if not mode:
            data = self.register_value("PKTCTRL0")
            for k, v in modes.items():
                if int(v, 2) == data['LENGTH_CONFIG[1:0]']:
                    return k

            return None
        else:
            self.register_write("PKTCTRL0", 'LENGTH_CONFIG[1:0]', modes[mode])
            return self.packet_length()

    def channel(self, channel=None):
        """
        Get or set CC1101 channel byte

        args: [optional] int(byte-value)
        returns: int byte-value
        """

        if channel is not None and type(channel) is not int:
            raise ValueError("Invalid channel number.")

        if channel is None:
            return self.read_byte('CHANNR')
        else:
            self.write_byte('CHANNR', int(channel))

    def baud_rate(self, rate=None):
        """
        Get or set CC1101 buad rate.

        args: int(baud value)
        returns: int
        """

        # read existing data rate value
        if rate is None:
            drate_e = self.register_value("MDMCFG4")['DRATE_E[3:0]']
            drate_m = self.register_value("MDMCFG3")['DRATE_M[7:0]']
            return int(((256 + drate_m) * math.pow(2,drate_e) / math.pow(2,28)) * self.osc_freq)

        # calculate and set new data rate value
        drate_e = int( math.log(rate * math.pow(2, 20) / self.osc_freq, 2) )
        drate_m = int( (rate * math.pow(2, 28) / ( self.osc_freq * math.pow(2, drate_e))) ) - 256

        if drate_m == 256:
            drate_m = 0
            drate_e += 1

        self.register_write('MDMCFG4', 'DRATE_E[3:0]', drate_e)
        self.register_write('MDMCFG3', 'DRATE_M[7:0]', drate_m)
        return self.baud_rate()

    def rx_bandwidth(self, value=None):
        """
        Get or set receive filter bandwidth.

        args: [optional] (int) [58000|100000|232000|325000|540000|812000] Hz
        returns: int
        """

        def write_this_bw(bw_e, bw_m):
            self.register_write('MDMCFG4', 'CHANBW_M[1:0]', bw_m)
            self.register_write('MDMCFG4', 'CHANBW_E[1:0]', bw_e)

        if value is not None and value not in [58000,100000,232000,325000,540000,812000]:
            raise ValueError("Invalid receive bandwidth setting.")

        if value is None:
            mdmcfg4 = self.register_value('MDMCFG4')
            bwm = mdmcfg4['CHANBW_M[1:0]']
            bwe = mdmcfg4['CHANBW_E[1:0]']
            return int(self.osc_freq / 8 * (4 + bwm) * math.pow(2, bwe))

        if value == 58000:
            write_this_bw(0x03,0x03)
        elif value == 100000:
            write_this_bw(0x03,0x00)
        elif value == 232000:
            write_this_bw(0x01,0x03)
        elif value == 325000:
            write_this_bw(0x01,0x01)
        elif value == 540000:
            write_this_bw(0x00,0x02)
        elif value == 812000:
            write_this_bw(0x00,0x00)

        return self.rx_bandwidth()

    def manchester(self, value=None):
        """
        Get or set manchester encoding

        args: [optional] int-boolean (0|1)
        returns: int-boolean
        """

        if value is None:
            return self.register_value("MDMCFG2")['MANCHESTER_EN']

        self.register_write('MDMCFG2', 'MANCHESTER_EN', value)
        return self.manchester()

    def whitening(self, value=None):
        """
        Get or set data whitening.

        args: [optional] int-boolean (0|1)
        returns: int-boolean
        """

        if value is None:
            return self.register_value('PKTCTRL0')['WHITE_DATA']

        self.register_write('PKTCTRL0', 'WHITE_DATA', value)
        return self.whitening()

    def channel_spacing(self):
        """
        Get channel spacing.
        TODO: Add option to SET channel spacing.

        args: none
        returns: int
        """
        chan = self.register_value("CHANNR")['CHAN']
        if value is None:
            chanspc_m = self.register_value("MDMCFG0")['CHANSPC_M[7:0]']
            chanspc_e = self.register_value("MDMCFG1")['CHANSPC_E[1:0]']
            return (self.osc_freq/math.pow(2,18)) * (256 + chanspc_m) * (math.pow(2, chanspc_e))

    def sync_word(self, value=None):
        """
        Get or set packet sync word

        args: [optional] str (like '0000'|'FAFA', etc)
        returns: str
        """

        if value is None:
            s1 = "{:x}".format(self.read_byte('SYNC1')).zfill(2).upper()
            s0 = "{:x}".format(self.read_byte('SYNC0')).zfill(2).upper()
            return s1 + s0

        if type(value) is str:
            if len(list(value)) != 4:
                raise ValueError("Must be 4 letter sync word like 'FAFA'.")

            s1 = int("".join(list(value)[:2]), 16)
            s0 = int("".join(list(value)[2:]), 16)
        elif type(value) is int:
            s0 = value & 0xFF
            s1 = value >> 8
        else:
            raise ValueError("Unexpected sync word type.")

        self.register_write('SYNC1', 'SYNC[15:8]', s1)
        self.register_write('SYNC0', 'SYNC[7:0]', s0)
        return self.sync_word()

    def rssi_offset(self):
        """
        Get RSSI offset for this product. CC1101 is fixed.

        args: none
        returns: int
        """

        return 74

    def rssi(self):
        """
        Read RSSI dbm signal measurement.

        args: none
        returns: int
        """

        value = self.read_byte(self.RSSI)
        if value >= 128:
            dbm = ((value - 256) /2) - self.rssi_offset()
        else:
            dbm = (value / 2) - self.rssi_offset()

        return dbm


    # config register convenience methods
    # ---------------------------------
    def register_value(self, name):
        """
        Get named register values.

        args: register name
        returns:
            dict, if a register mapping-specification is found.
            Otherwise byte value.
        """

        byte = self.read_byte(name)
        return self._register_value_from_byte(name, byte)

    def register_write(self, name, attr_name, value):
        """
        Update specific attribute in a register.

        Register and Attribute names come from the Ti CC1101 spec sheet.

        args:
            - register name (str)
            - attribute name (str)
            - value (str or int)
                for boolean values, an int of 1 or zero is fine.
                For multi-bit fields it can be easier to enter the bit string.

        Example, to update the MOD_FORMAT field in MDMCFG2:

            register_write('MDMCFG2', 'MOD_FORMAT', '011')
        """

        byte = self.read_byte(name)
        spec = self._register_schema(name)[attr_name]
        if not spec:
            raise ValueError("Register specification for '%s' not found" % name)

        new_value = self._update_val_in_byte(byte, spec, value)
        self.write_byte(name, new_value)

    # read/write data
    # ---------------------------------
    def recv_data(self):
        """Receive FIFO data"""

        self.enable_rx()
        rx_bytes_val = self.read_byte(self.RXBYTES)

        #if rx_bytes_val has something and Underflow bit is not 1
        if (rx_bytes_val & 0x7F and not (rx_bytes_val & 0x80)):
            pkt_len = self.packet_length()

            if pkt_len == "PKT_LEN_FIXED":
                data_len = self.read_byte(self.PKTLEN)

            elif pkt_len == "PKT_LEN_VARIABLE":
                max_len = self.read_byte(self.PKTLEN)
                data_len = self.read_byte(self.RXFIFO)

                if data_len > max_len:
                    return False

            elif pkt_len == "PKT_LEN_INFINITE":
                # ToDo
                raise Exception("MODE NOT IMPLEMENTED")

            data = self.read_burst(self.RXFIFO, data_len)
            self.flush_rx_fifo()
            self.sidle()

            return data

    def send_data(self, bytes):
        """
        Send data to TX FIFO.

        args:
          - list of bytes
        returns:
            none
        """
        self.enable_tx()
        marcstate = self.marcstate()
        payload = []

        if len(bytes) == 0:
            raise ValueError("Must include payload")

        while ((marcstate & 0x1F) != 0x0D):
            if marcstate == 0x11:
                self.flush_rx_fifo()

            marcstate = self.marcstate()


        sending_mode = self.packet_length()
        data_len = len(bytes)

        if sending_mode == "PKT_LEN_FIXED":
            if data_len > self.read_byte(self.PKTLEN):
                raise ValueError("Payload too big.")

            if self.register_value("PKTCTRL1")['APPEND_STATUS']:
                payload.append(self.read_byte(self.ADDR))

            payload.extend(bytes)
            payload.extend([0] * (self.read_byte(self.PKTLEN) - len(payload)))

        elif sending_mode == "PKT_LEN_VARIABLE":
            payload.append(data_len)

            if self.register_value("PKTCTRL1")['APPEND_STATUS']:
                payload.append(self.read_byte(self.ADDR))
                payload[0] += 1

            payload.extend(bytes)

        elif sending_mode == "PKT_LEN_INFINITE":
            # ToDo
            raise Exception("MODE NOT IMPLEMENTED")

        self.write_burst(self.TXFIFO, payload)
        self.cmd_delay(2000)
        self.enable_tx()
        marcstate = self.marcstate()

        if marcstate not in [0x13, 0x14, 0x15]:  # RX, RX_END, RX_RST
            self.sidle()
            self.flush_tx_fifo()
            self.enable_rx()

            return False

        remaining = self.read_byte(self.TXBYTES) & 0x7F
        while remaining != 0:
            self.cmd_delay(100)
            remaining =  self.read_byte(self.TXBYTES) & 0x7F

        if (self.read_byte(self.TXBYTES) & 0x07) == 0:
            return True
        else:
            return False


    # PRIVATE class methods
    # ---------------------------------
    def _register_value_from_byte(self, name, byte):
        """
        Extract config register attributes/values from a byte

        args:
            - register name
            - byte
        """

        data = {}
        spec = self._register_schema(name)
        for attr_name, attr_schema in spec.items():
            value = self._extract_val_from_byte(byte, attr_schema)
            data[attr_name] = value

        return data

    def _register_schema(self, name):
        """
        Get schema for named register.

        Each value (schema) is a tuple or list containing:
            - which index position the attribute starts at.
            - how many bits does it use.

        """

        # Indexing here is opposite of spec sheet.
        # Ti Doc Index 7 => here is 0
        # Ti Doc Index 0 => here is 7
        data = {
            "IOCFG2": {
                "GDO2_INV": [1,1],
                "GDO2_CFG[5:0]": [2,6]
            },
            "IOCFG1": {
                "GDO_DS": [0,1],
                "GDO1_INV": [1,1],
                "GDO1_CFG[5:0]": [2,6]
            },
            "IOCFG0": {
                "TEMP_SENSOR_ENABLE": [0,1],
                "GDO0_INF": [1,1],
                "GDO0_CFG[5:0]": [2,6]
            },
            "FIFOTHR": {
                "ADC_RETENTION": [1,1],
                "CLOSE_IN_RX[1:0]": [2,2],
                "FIFO_THR[3:0]": [4,4]
            },
            "SYNC1": {
                "SYNC[15:8]": [0,8]
            },
            "SYNC0": {
                "SYNC[7:0]": [0,8]
            },
            "PKTLEN": {
                "PACKET_LENGTH": [0,8]
            },
            'PKTCTRL1': {
                "PQT[2:0]": [0,3],
                "CRC_AUTOFLUSH": [4,1],
                "APPEND_STATUS": [5,1],
                "ADR_CHK[1:0]": [6,2]
            },
            'PKTCTRL0': {
                "WHITE_DATA": [1,1],
                "PKT_FORMAT[1:0]": [2,2],
                "CRC_EN": [5,1],
                "LENGTH_CONFIG[1:0]": [6,2]
            },
            'ADDR': {
                'DEVICE_ADDR[7:0]': [0,8]
            },
            'CHANNR': {
                'CHAN[7:0]': [0,8]
            },
            "FSCTRL1": {
                "FREQ_IF[4:0]": [3,5]
            },
            "FSCTRL0": {
                "FREQOFF[7:0]": [0,8]
            },
            'FREQ2': {
                'FREQ[23:22]': [0,2],
                'FREQ[21:16]': [2,6]
            },
            'FREQ1': {
                'FREQ[15:8]': [0,8]
            },
            'FREQ0': {
                'FREQ[7:0]': [0,8]
            },
            "MDMCFG4": {
                "CHANBW_E[1:0]": [0,2],
                "CHANBW_M[1:0]": [2,2],
                "DRATE_E[3:0]": [4, 4]
            },
            "MDMCFG3": {
                "DRATE_M[7:0]": [0,8]
            },
            "MDMCFG2": {
                "DEM_DCFILT_OFF": [0,1],
                "MOD_FORMAT[2:0]": [1,3],
                "MANCHESTER_EN": [4,1],
                "SYNC_MODE[2:0]": [5,3]
            },
            "MDMCFG1": {
                "FEC_EN": [0,1],
                "NUM_PREAMBLE[2:0]": [1,3],
                "CHANSPC_E[1:0]": [6,1]
            },
            "MDMCFG0": {
                "CHANSPC_M[7:0]": [0,8]
            },
            "DEVIATN": {
                "DEVIATION_E[2:0]": [1,3],
                "DEVIATION_M[2:0]": [5,3]
            },
            "MCSM2": {
                "RX_TIME_RSSI": [3,1],
                "RX_TIME_QUAL": [4,1],
                "RX_TIME[2:0]": [5,3]
            },
            "MCSM1": {
                "CCA_MODE[1:0]": [2,2],
                "RXOFF_MODE[1:0]": [4,2],
                "TXOFF_MODE[1:0]": [6,2]
            },
            "MCSM0": {
                "FS_AUTOCAL[1:0]": [2,2],
                "PO_TIMEOUT": [4,2],
                "PIN_CTRL_EN": [6,1],
                "XOSC_FORCE_ON": [7,1]
            },
            "FOCCFG": {
                "FOC_BS_CS_GATE": [2,1],
                "FOC_PRE_K[1:0]": [3,2],
                "FOC_POST_K": [5,1],
                "FOC_LIMIT[1:0]": [6,2]
            },
            "BSCFG": {
                "BS_PRE_K[1:0]": [0,2],
                "BS_PRE_KP[1:0]": [2,2],
                "BS_POST_KI": [4,1],
                "BS_POST_KP": [5,1],
                "BS_LIMIT[1:0]": [6,2]
            },
            "AGCCTRL2": {
                "MAX_DVGA_GAIN[1:0]": [0,2],
                "MAX_LNA_GAIN[2:0]": [2,3],
                "MAGN_TARGET[2:0]": [5,3]
            },
            "AGCCTRL1": {
                "AGC_LNA_PRIORITY": [1,1],
                "CARRIER_SENSE_REL_THR[1:0]": [2,2],
                "CARRIER_SENSE_ABS_THR[3:0]": [4,4]
            },
            "AGCCTRL0": {
                "HYST_LEVEL[1:0]": [0,2],
                "WAIT_TIME[1:0]": [2,2],
                "AGC_FREEZE[1:0]": [4,2],
                "FILTER_LENGTH[1:0]": [6,2]
            },
            "WOREVT1": {
                "EVENT0[15:8]": [0,8]
            },
            "WOREVT0": {
                "EVENT0[7:0]": [0,8]
            },
            "WORCTRL": {
                "RC_PD": [0,1],
                "EVENT1[2:0]": [1,3],
                "RC_CAL": [4,1],
                "WOR_RES": [6,2]
            },
            "FREND1": {
                "LNA_CURRENT[1:0]": [0, 2],
                "LNA2MIX_CURRENT[1:0]": [2, 2],
                "LODIV_BUF_CURRENT_RX[1:0]": [4,2],
                "MIX_CURRENT[1:0]": [6,2]
            },
            "FREND0": {
                "LODIV_BUF_CURRENT_TX[1:0]": [2, 2],
                "PA_POWER[2:0]": [5,3]
            },
            "FSCAL3": {
                "FSCAL3[7:6]": [0,2],
                "CHP_CURR_CAL_EN[1:0]": [2,2],
                "FSCAL3[3:0]": [4,4],
            },
            "FSCAL2": {
                "VCO_CORE_H_EN": [2,1],
                "FSCAL2[4:0]": [3,5]
            },
            "FSCAL1": {
                "FSCAL1[5:0]": [2,6]
            },
            "FSCAL0": {
                "FSCAL0[6:0]": [1,7]
            },
            "RCCTRL1": {
                "RCCTRL1[6:0]": [1,7]
            },
            "RCCTRL0": {
                "RCCTRL0[6:0]": [1,7]
            },
            "FSTEST": {
                "FSTEST[7:0]": [0,8]
            },
            "PTEST": {
                "PTEST[7:0]": [0,8]
            },
            "AGCTEST": {
                "AGCTEST[7:0]": [0,8]
            },
            "TEST2": {
                "TEST2[7:0]": [0,8]
            },
            "TEST1": {
                "TEST1[7:0]": [0,8]
            },
            "TEST0": {
                "TEST0[7:2]": [0,6],
                "VCO_SEL_CAL_EN": [6,1],
                "TEST0[0]": [7,1]
            },
            "PARTNUM": {
                "PARTNUM[7:0]": [0,8]
            },
            "PARTNUM": {
                "VERSION[7:0]": [0,8]
            },
            "FREQEST": {
                "FREQOSS_EST": [0,8]
            },
            "LQI": {
                "CRC_OK": [0,1],
                "LQI_EST[6:0]": [1,7]
            },
            "RSSI": {
                "RSSI": [0,8]
            },
            "MARCSTATE": {
                "MARC_STATE[4:0]": [3,5]
            },
            "WORTIME1": {
                "TIME[15:8]": [0,8]
            },
            "WORTIME0": {
                "TIME[7:0]": [0,8]
            },
            'PKTSTATUS': {
                "CRC_OK": [0,1],
                "CS": [1,1],
                "PQT_REACHED": [2,1],
                "CCA": [3,1],
                "SFD": [4,1],
                "GDO2": [5,1],
                "GDO0": [7,1]
            },
            "VCO_VC_DAC": {
                "VCO_VC_DAC[7:0]": [0,8]
            },
            "TXBYTES": {
                "TXFIFO_UNDERFLOW": [0,1],
                "NUM_TXBYTES": [1,7]
            },
            "RXBYTES": {
                "RXFIFO_UNDERFLOW": [0,1],
                "NUM_TXBYTES": [1,7]
            },
            "RCCTRL1_STATUS": {
                "RCCTRL1_STATUS[6:0]": [1,7]
            },
            "RCCTRL0_STATUS": {
                "RCCTRL0_STATUS[6:0]": [1,7]
            }
        }

        if name not in data:
            raise ValueError("Register name '%s' not found" % name)

        return data[name]
