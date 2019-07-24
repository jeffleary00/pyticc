#!/usr/bin/env python

from pyticc.cc1101 import CC1101

cc = CC1101()
cc.reset()

cc.base_frequency(433)
cc.baud_rate(4800)
cc.modulation("OOK")
cc.packet_length("PKT_LEN_FIXED")
cc.rx_bandwidth(232000)
cc.manchester(1)
cc.whitening(0)


# ask/ook specific params (Ti DN022)
cc.write_byte("AGCCTRL2", 0x03)
cc.write_byte("AGCCTRL1", 0x00)
cc.write_byte("AGCCTRL0", 0x91)
cc.write_byte("FREND1", 0xB6)
cc.write_byte("TEST2", 0x81)
cc.write_byte("TEST1", 0x35)
cc.write_byte("FIFOTHR", 0x47)

# sync mode
cc.sync_word('0000')
cc.register_write('MDMCFG2', 'SYNC_MODE[2:0]', '000')

# rx gain settings
cc.register_write('AGCCTRL2', 'MAGN_TARGET[2:0]', 0x03)
cc.register_write('AGCCTRL2', 'MAX_LNA_GAIN[2:0]', '000')
cc.register_write('AGCCTRL2', 'MAX_DVGA_GAIN[1:0]', '10')
cc.register_write('AGCCTRL1', 'CARRIER_SENSE_ABS_THR[3:0]', 0x0)
## cc.register_write('FSCTRL1', 'FREQ_IF[4:0]', 0x06)

# cc.register_write('AGCCTRL0', 'FILTER_LENGTH[1:0]', 0x02)



while True:
    data = cc.recv_data()
    if data is not None:
        print("\nRSSI: %d" % cc.rssi())
        print(data)
